"""Generate ROP type curve charts from the built curve CSVs.

Lateral mode (default):
  1. Rotary ROP per group (P10/P50/P90 + individual runs) -- x = distance from BHA start
  2. Slide ROP per group (P10/P50/P90 + individual runs) -- x = distance from lateral start
  3. Head-to-head rotary comparison
  4. Head-to-head slide comparison
  5. TTD ranking bar chart

Vertical mode (--mode vertical):
  1. Rotary ROP per group by formation segment (P10/P50/P90 + individual runs)
  2. Slide ROP per group by formation segment
  3. Head-to-head rotary comparison by formation
  4. Head-to-head slide comparison by formation
  5. TTD ranking bar chart

Usage:
    python plot_type_curves.py                    # lateral (default)
    python plot_type_curves.py --mode vertical    # vertical/formation-based
"""
import csv
import os
import sys
from collections import defaultdict

import pandas as pd

import db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRIPT_DIR, "charts")

# Minimum number of runs for a group to appear in comparison charts
MIN_RUNS_FOR_COMPARISON = 3

COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
    "#9467bd", "#8c564b", "#e377c2", "#7f7f7f",
]

# Corva-inspired chart styling constants
RUN_LINE_COLOR = "#9AA5B1"
RUN_LINE_ALPHA = 0.28
RUN_LINE_WIDTH = 0.8
ROTARY_COLOR = "#0B6E99"
SLIDE_COLOR = "#E67E22"
GRID_COLOR = "#D9E2EC"
AXIS_EDGE_COLOR = "#BCCCDC"
TEXT_COLOR = "#243B53"
BAND_ALPHA = 0.18


def _style_axis(ax):
    """Apply consistent axis styling for all charts."""
    ax.set_facecolor("#FFFFFF")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS_EDGE_COLOR)
        ax.spines[side].set_linewidth(1)
    ax.tick_params(axis="both", colors=TEXT_COLOR, labelsize=10)
    ax.grid(True, color=GRID_COLOR, alpha=0.85, linewidth=0.8)
    ax.grid(which="minor", color=GRID_COLOR, alpha=0.45, linewidth=0.5)
    ax.set_axisbelow(True)


def _finalize_figure(fig, ax):
    """Shared finishing touches before saving."""
    _style_axis(ax)
    fig.patch.set_facecolor("#FFFFFF")
    fig.tight_layout()


def _plot_group_runs(ax, per_run, group_key, curve_key, x_mapper):
    """Plot individual run overlays for a single group."""
    for _, run_data in per_run.items():
        if run_data["meta"]["equiv_bha_key"] != group_key:
            continue
        curve = run_data[curve_key]
        if not curve:
            continue
        bins = sorted(curve.keys())
        x = [x_mapper(b) for b in bins]
        y = [curve[b] for b in bins]
        ax.plot(x, y, color=RUN_LINE_COLOR, linewidth=RUN_LINE_WIDTH, alpha=RUN_LINE_ALPHA)


def load_group_curves(csv_path):
    """Load per-group P10/P50/P90 curve data."""
    groups = defaultdict(lambda: {"rotary": {}, "slide": {}, "meta": {}})
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            gk = row["equiv_bha_key"]
            b = int(row["bin_start_ft"])
            curve_type = row["curve_type"]
            groups[gk]["meta"]["num_runs"] = int(row["num_runs"])
            groups[gk][curve_type][b] = {
                "p10": float(row["p10"]),
                "p50": float(row["p50"]),
                "p90": float(row["p90"]),
                "contributing_runs": int(row["contributing_runs"]),
                "confident": row["confident"] == "True",
            }
    return dict(groups)


def load_per_run_curves(csv_path):
    """Load per-run curve data for overlay."""
    runs = defaultdict(lambda: {"rotary": {}, "slide": {}, "meta": {}})
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            run_key = (row["asset_id"], row["bha_number"])
            b = int(row["bin_start_ft"])
            curve_type = row["curve_type"]
            runs[run_key]["meta"]["equiv_bha_key"] = row["equiv_bha_key"]
            runs[run_key]["meta"]["well_name"] = row["well_name"]
            runs[run_key]["meta"]["has_agitator"] = row.get("has_agitator", "False")
            runs[run_key][curve_type][b] = float(row["median_rop"])
    return dict(runs)


def load_ttd(csv_path):
    """Load TTD ranking."""
    results = []
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            results.append(row)
    return results


def _load_csv_or_parquet(csv_path, section_name, data_type, mode,
                         load_from_csv_fn, run_id=None):
    """Try CSV first, then fall back to Parquet via db module.

    load_from_csv_fn: function that takes csv_path and returns the data.
    For group/per_run, Parquet records are converted to the nested dict structure.
    run_id: analysis run ID for scoped Parquet lookup.
    """
    if os.path.exists(csv_path):
        return load_from_csv_fn(csv_path)
    # Fallback to Parquet (scoped by run_id)
    if data_type == "group":
        df = db.load_rop_curves_by_group(section_name, mode, run_id=run_id)
    elif data_type == "per_run":
        df = db.load_rop_curves_per_run(section_name, mode, run_id=run_id)
    else:
        return None
    if df is None or df.empty:
        return None
    records = df.to_dict("records")
    if data_type == "group":
        return _parquet_records_to_groups(records, mode)
    if data_type == "per_run":
        return _parquet_records_to_per_run(records, mode)
    return None


def _parquet_records_to_groups(records, mode):
    """Convert Parquet group curve records to nested groups dict."""
    groups = defaultdict(lambda: {"rotary": {}, "slide": {}, "meta": {}})
    bin_key = "formation_bin_key" if mode == "vertical" else "bin_start_ft"
    for row in records:
        gk = row["equiv_bha_key"]
        key = row.get(bin_key)
        if key is None:
            continue
        if bin_key == "bin_start_ft":
            key = int(key)
        curve_type = row["curve_type"]
        groups[gk]["meta"]["num_runs"] = int(row["num_runs"])
        groups[gk][curve_type][key] = {
            "p10": float(row["p10"]),
            "p50": float(row["p50"]),
            "p90": float(row["p90"]),
            "contributing_runs": int(row.get("contributing_runs", row.get("num_runs", 0))),
            "confident": str(row.get("confident", "False")).lower() in ("true", "1", "yes"),
        }
    return dict(groups)


def _parquet_records_to_per_run(records, mode):
    """Convert Parquet per-run curve records to nested runs dict."""
    runs = defaultdict(lambda: {"rotary": {}, "slide": {}, "meta": {}})
    bin_key = "formation_bin_key" if mode == "vertical" else "bin_start_ft"
    for row in records:
        run_key = (str(row["asset_id"]), str(row["bha_number"]))
        key = row.get(bin_key)
        if key is None:
            continue
        if bin_key == "bin_start_ft":
            key = int(key)
        curve_type = row["curve_type"]
        runs[run_key]["meta"]["equiv_bha_key"] = row["equiv_bha_key"]
        runs[run_key]["meta"]["well_name"] = row.get("well_name", "N/A")
        runs[run_key]["meta"]["has_agitator"] = row.get("has_agitator", "False")
        runs[run_key][curve_type][key] = float(row["median_rop"])
    return dict(runs)


def plot_group_rotary(group_key, group_data, per_run, out_dir, section_label=None):
    """Chart 1: Rotary ROP for one group with P10/P50/P90 and individual runs."""
    rotary = group_data["rotary"]
    if not rotary:
        return

    bins_sorted = sorted(b for b, d in rotary.items() if d["confident"])
    if not bins_sorted:
        return

    x = [b / 1000 for b in bins_sorted]  # convert to kft
    p10 = [rotary[b]["p10"] for b in bins_sorted]
    p50 = [rotary[b]["p50"] for b in bins_sorted]
    p90 = [rotary[b]["p90"] for b in bins_sorted]

    fig, ax = plt.subplots(figsize=(12, 6))
    _plot_group_runs(ax, per_run, group_key, "rotary", lambda b: b / 1000)
    ax.fill_between(x, p10, p90, alpha=BAND_ALPHA, color=ROTARY_COLOR, label="P10-P90")
    ax.plot(x, p50, color=ROTARY_COLOR, linewidth=2.8, label="P50")

    n_runs = group_data["meta"].get("num_runs", "?")
    label_line = f"\n{section_label}" if section_label else ""
    ax.set_title(f"Rotary ROP Type Curve: {group_key}\n({n_runs} runs){label_line}", fontsize=13, color=TEXT_COLOR)
    ax.set_xlabel("Distance from Lateral Start (kft)", fontsize=11, color=TEXT_COLOR)
    ax.set_ylabel("Rotary ROP (ft/hr)", fontsize=11, color=TEXT_COLOR)
    ax.legend(loc="upper right", frameon=False, fontsize=10)
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:.1f}"))
    ax.xaxis.set_minor_locator(mticker.AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(mticker.AutoMinorLocator(2))

    safe_name = group_key.replace(" ", "_").replace("/", "-").replace("|", "_")
    _finalize_figure(fig, ax)
    fig.savefig(os.path.join(out_dir, f"rotary_{safe_name}.png"), dpi=170)
    plt.close(fig)


def plot_group_slide(group_key, group_data, per_run, out_dir, section_label=None):
    """Chart 2: Slide ROP for one group with P10/P50/P90 and individual runs."""
    slide = group_data["slide"]
    if not slide:
        return

    bins_sorted = sorted(b for b, d in slide.items() if d["confident"])
    if not bins_sorted:
        return

    x = [b / 1000 for b in bins_sorted]
    p10 = [slide[b]["p10"] for b in bins_sorted]
    p50 = [slide[b]["p50"] for b in bins_sorted]
    p90 = [slide[b]["p90"] for b in bins_sorted]

    fig, ax = plt.subplots(figsize=(12, 6))
    _plot_group_runs(ax, per_run, group_key, "slide", lambda b: b / 1000)
    ax.fill_between(x, p10, p90, alpha=BAND_ALPHA, color=SLIDE_COLOR, label="P10-P90")
    ax.plot(x, p50, color=SLIDE_COLOR, linewidth=2.8, label="P50")

    n_runs = group_data["meta"].get("num_runs", "?")
    label_line = f"\n{section_label}" if section_label else ""
    ax.set_title(f"Slide ROP Type Curve: {group_key}\n({n_runs} runs){label_line}", fontsize=13, color=TEXT_COLOR)
    ax.set_xlabel("Distance from Lateral Start (kft)", fontsize=11, color=TEXT_COLOR)
    ax.set_ylabel("Slide ROP (ft/hr)", fontsize=11, color=TEXT_COLOR)
    ax.legend(loc="upper right", frameon=False, fontsize=10)
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:.1f}"))
    ax.xaxis.set_minor_locator(mticker.AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(mticker.AutoMinorLocator(2))

    safe_name = group_key.replace(" ", "_").replace("/", "-").replace("|", "_")
    _finalize_figure(fig, ax)
    fig.savefig(os.path.join(out_dir, f"slide_{safe_name}.png"), dpi=170)
    plt.close(fig)


def plot_rotary_comparison(groups, out_dir, section_label=None):
    """Chart 3: Head-to-head rotary P50 comparison for all groups."""
    fig, ax = plt.subplots(figsize=(14, 7))

    eligible = {gk: gd for gk, gd in groups.items()
                if gd["meta"].get("num_runs", 0) >= MIN_RUNS_FOR_COMPARISON}

    ranked = sorted(eligible.items(), key=lambda x: -x[1]["meta"].get("num_runs", 0))
    for i, (gk, gd) in enumerate(ranked):
        rotary = gd["rotary"]
        bins_sorted = sorted(b for b, d in rotary.items() if d["confident"])
        if not bins_sorted:
            continue

        x = [b / 1000 for b in bins_sorted]
        y = [rotary[b]["p50"] for b in bins_sorted]
        color = COLORS[i % len(COLORS)] if i < 6 else RUN_LINE_COLOR
        lw = 2.6 if i < 3 else 1.8
        alpha = 0.95 if i < 3 else 0.75
        n = gd["meta"].get("num_runs", "?")
        ax.plot(x, y, color=color, linewidth=lw, alpha=alpha, label=f"{gk} ({n} runs)")

    label_line = f"\n{section_label}" if section_label else ""
    ax.set_title(f"Rotary ROP Comparison (P50) by Equivalent BHA{label_line}", fontsize=14, color=TEXT_COLOR)
    ax.set_xlabel("Distance from Lateral Start (kft)", fontsize=12, color=TEXT_COLOR)
    ax.set_ylabel("Rotary ROP (ft/hr)", fontsize=12, color=TEXT_COLOR)
    ax.legend(loc="upper right", fontsize=9, frameon=False)
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:.1f}"))
    ax.xaxis.set_minor_locator(mticker.AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(mticker.AutoMinorLocator(2))

    _finalize_figure(fig, ax)
    fig.savefig(os.path.join(out_dir, "comparison_rotary.png"), dpi=170)
    plt.close(fig)


def plot_slide_comparison(groups, out_dir, section_label=None):
    """Chart 4: Head-to-head slide P50 comparison for all groups."""
    fig, ax = plt.subplots(figsize=(14, 7))

    eligible = {gk: gd for gk, gd in groups.items()
                if gd["meta"].get("num_runs", 0) >= MIN_RUNS_FOR_COMPARISON}

    ranked = sorted(eligible.items(), key=lambda x: -x[1]["meta"].get("num_runs", 0))
    for i, (gk, gd) in enumerate(ranked):
        slide = gd["slide"]
        bins_sorted = sorted(b for b, d in slide.items() if d["confident"])
        if not bins_sorted:
            continue

        x = [b / 1000 for b in bins_sorted]
        y = [slide[b]["p50"] for b in bins_sorted]
        color = COLORS[i % len(COLORS)] if i < 6 else RUN_LINE_COLOR
        lw = 2.6 if i < 3 else 1.8
        alpha = 0.95 if i < 3 else 0.75
        n = gd["meta"].get("num_runs", "?")
        ax.plot(x, y, color=color, linewidth=lw, alpha=alpha, label=f"{gk} ({n} runs)")

    label_line = f"\n{section_label}" if section_label else ""
    ax.set_title(f"Slide ROP Comparison (P50) by Equivalent BHA{label_line}", fontsize=14, color=TEXT_COLOR)
    ax.set_xlabel("Distance from Lateral Start (kft)", fontsize=12, color=TEXT_COLOR)
    ax.set_ylabel("Slide ROP (ft/hr)", fontsize=12, color=TEXT_COLOR)
    ax.legend(loc="upper right", fontsize=9, frameon=False)
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:.1f}"))
    ax.xaxis.set_minor_locator(mticker.AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(mticker.AutoMinorLocator(2))

    _finalize_figure(fig, ax)
    fig.savefig(os.path.join(out_dir, "comparison_slide.png"), dpi=170)
    plt.close(fig)


def plot_ttd_ranking(ttd_data, out_dir, section_label=None):
    """Chart 6: TTD ranking bar chart."""
    valid = [t for t in ttd_data if float(t["ttd_hours"]) > 0]
    if not valid:
        return

    valid.sort(key=lambda t: float(t["ttd_hours"]))

    fig, ax = plt.subplots(figsize=(10, max(4, len(valid) * 0.8)))

    labels = [f"{t['group_key']} ({t['num_runs']} runs)" for t in valid]
    hours = [float(t["ttd_hours"]) for t in valid]
    colors_bar = [COLORS[i % len(COLORS)] for i in range(len(valid))]

    y_pos = range(len(valid))
    bars = ax.barh(y_pos, hours, color=colors_bar, height=0.64, alpha=0.9)

    # Add hour labels on bars
    for bar, h in zip(bars, hours):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{h:.1f} hrs ({h/24:.2f} days)",
                va="center", fontsize=9, color=TEXT_COLOR)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=10)
    ax.set_xlabel("Time to TD (hours)", fontsize=12, color=TEXT_COLOR)
    label_line = f"\n{section_label}" if section_label else "\n(10,000 ft lateral, observed slide %)"
    ax.set_title(f"Estimated Time to TD by Equivalent BHA{label_line}", fontsize=13, color=TEXT_COLOR)
    ax.grid(True, axis="x", color=GRID_COLOR, alpha=0.8)
    ax.invert_yaxis()
    ax.xaxis.set_minor_locator(mticker.AutoMinorLocator(2))

    _finalize_figure(fig, ax)
    fig.savefig(os.path.join(out_dir, "ttd_ranking.png"), dpi=170)
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────
# Vertical / Formation-based chart functions
# ─────────────────────────────────────────────────────────────────────

def load_roadmap(csv_path):
    """Load formation roadmap (ordered list of formation bin keys)."""
    roadmap = []
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            roadmap.append(row["formation_bin_key"])
    return roadmap


def load_group_curves_vertical(csv_path):
    """Load per-group formation-based curve data."""
    groups = defaultdict(lambda: {"rotary": {}, "slide": {}, "meta": {}})
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            gk = row["equiv_bha_key"]
            key = row["formation_bin_key"]
            curve_type = row["curve_type"]
            groups[gk]["meta"]["num_runs"] = int(row["num_runs"])
            groups[gk][curve_type][key] = {
                "p10": float(row["p10"]),
                "p50": float(row["p50"]),
                "p90": float(row["p90"]),
                "contributing_runs": int(row["contributing_runs"]),
                "confident": row["confident"] == "True",
            }
    return dict(groups)


def load_per_run_curves_vertical(csv_path):
    """Load per-run formation-based curve data."""
    runs = defaultdict(lambda: {"rotary": {}, "slide": {}, "meta": {}})
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            run_key = (row["asset_id"], row["bha_number"])
            key = row["formation_bin_key"]
            curve_type = row["curve_type"]
            runs[run_key]["meta"]["equiv_bha_key"] = row["equiv_bha_key"]
            runs[run_key]["meta"]["well_name"] = row["well_name"]
            runs[run_key]["meta"]["has_agitator"] = row.get("has_agitator", "False")
            runs[run_key][curve_type][key] = float(row["median_rop"])
    return dict(runs)


def format_formation_labels(roadmap):
    """Create short labels and formation boundary positions for x-axis.

    Returns (tick_positions, tick_labels, boundary_positions, boundary_labels).
    """
    tick_labels = []
    boundary_positions = []
    boundary_labels = []
    prev_fm = None

    for i, key in enumerate(roadmap):
        parts = key.rsplit("|", 1)
        fm_name = parts[0]
        seg = int(parts[1])

        # Only label every other segment, plus formation transitions
        if fm_name != prev_fm:
            tick_labels.append(f"{seg}%")
            boundary_positions.append(i)
            boundary_labels.append(fm_name)
        elif seg % 20 == 0:
            tick_labels.append(f"{seg}%")
        else:
            tick_labels.append("")

        prev_fm = fm_name

    return list(range(len(roadmap))), tick_labels, boundary_positions, boundary_labels


def plot_group_rotary_vertical(group_key, group_data, per_run, roadmap, out_dir, section_label=None):
    """Rotary ROP by formation segment for one group."""
    rotary = group_data["rotary"]
    if not rotary:
        return

    # Build x positions using roadmap order
    x_pos = []
    p10_vals = []
    p50_vals = []
    p90_vals = []
    for i, key in enumerate(roadmap):
        if key in rotary and rotary[key]["confident"]:
            x_pos.append(i)
            p10_vals.append(rotary[key]["p10"])
            p50_vals.append(rotary[key]["p50"])
            p90_vals.append(rotary[key]["p90"])

    if not x_pos:
        return

    fig, ax = plt.subplots(figsize=(14, 6))

    for _, run_data in per_run.items():
        if run_data["meta"]["equiv_bha_key"] != group_key:
            continue
        rc = run_data["rotary"]
        if not rc:
            continue
        rx = []
        ry = []
        for i, key in enumerate(roadmap):
            if key in rc:
                rx.append(i)
                ry.append(rc[key])
        if rx:
            ax.plot(rx, ry, color=RUN_LINE_COLOR, linewidth=RUN_LINE_WIDTH, alpha=RUN_LINE_ALPHA)

    ax.fill_between(x_pos, p10_vals, p90_vals, alpha=BAND_ALPHA, color=ROTARY_COLOR, label="P10-P90")
    ax.plot(x_pos, p50_vals, color=ROTARY_COLOR, linewidth=2.8, label="P50")

    # Formation boundaries
    ticks, tick_labels, bound_pos, bound_labels = format_formation_labels(roadmap)
    for bp in bound_pos:
        ax.axvline(x=bp, color=AXIS_EDGE_COLOR, linewidth=0.8, linestyle="--", alpha=0.6)

    # Formation name labels at top
    for bp, bl in zip(bound_pos, bound_labels):
        ax.text(bp + 1, ax.get_ylim()[1] * 0.95, bl, fontsize=8, rotation=45,
                va="top", ha="left", color=TEXT_COLOR)

    ax.set_xticks(ticks)
    ax.set_xticklabels(tick_labels, fontsize=7, rotation=45)

    n_runs = group_data["meta"].get("num_runs", "?")
    label_line = f"\n{section_label}" if section_label else ""
    ax.set_title(f"Rotary ROP by Formation: {group_key}\n({n_runs} runs, {FORMATION_SEGMENT_PCT}% segments){label_line}",
                 fontsize=13, color=TEXT_COLOR)
    ax.set_xlabel("Formation Position", fontsize=11, color=TEXT_COLOR)
    ax.set_ylabel("Rotary ROP (ft/hr)", fontsize=11, color=TEXT_COLOR)
    ax.legend(loc="upper right", frameon=False, fontsize=10)
    ax.set_ylim(bottom=0)
    ax.yaxis.set_minor_locator(mticker.AutoMinorLocator(2))

    safe_name = group_key.replace(" ", "_").replace("/", "-").replace("|", "_")
    _finalize_figure(fig, ax)
    fig.savefig(os.path.join(out_dir, f"vert_rotary_{safe_name}.png"), dpi=170)
    plt.close(fig)


def plot_group_slide_vertical(group_key, group_data, per_run, roadmap, out_dir, section_label=None):
    """Slide ROP by formation segment for one group."""
    slide = group_data["slide"]
    if not slide:
        return

    x_pos = []
    p10_vals = []
    p50_vals = []
    p90_vals = []
    for i, key in enumerate(roadmap):
        if key in slide and slide[key]["confident"]:
            x_pos.append(i)
            p10_vals.append(slide[key]["p10"])
            p50_vals.append(slide[key]["p50"])
            p90_vals.append(slide[key]["p90"])

    if not x_pos:
        return

    fig, ax = plt.subplots(figsize=(14, 6))

    for _, run_data in per_run.items():
        if run_data["meta"]["equiv_bha_key"] != group_key:
            continue
        sc = run_data["slide"]
        if not sc:
            continue
        sx = []
        sy = []
        for i, key in enumerate(roadmap):
            if key in sc:
                sx.append(i)
                sy.append(sc[key])
        if sx:
            ax.plot(sx, sy, color=RUN_LINE_COLOR, linewidth=RUN_LINE_WIDTH, alpha=RUN_LINE_ALPHA)

    ax.fill_between(x_pos, p10_vals, p90_vals, alpha=BAND_ALPHA, color=SLIDE_COLOR, label="P10-P90")
    ax.plot(x_pos, p50_vals, color=SLIDE_COLOR, linewidth=2.8, label="P50")

    ticks, tick_labels, bound_pos, bound_labels = format_formation_labels(roadmap)
    for bp in bound_pos:
        ax.axvline(x=bp, color=AXIS_EDGE_COLOR, linewidth=0.8, linestyle="--", alpha=0.6)
    for bp, bl in zip(bound_pos, bound_labels):
        ax.text(bp + 1, ax.get_ylim()[1] * 0.95, bl, fontsize=8, rotation=45,
                va="top", ha="left", color=TEXT_COLOR)

    ax.set_xticks(ticks)
    ax.set_xticklabels(tick_labels, fontsize=7, rotation=45)

    n_runs = group_data["meta"].get("num_runs", "?")
    label_line = f"\n{section_label}" if section_label else ""
    ax.set_title(f"Slide ROP by Formation: {group_key}\n({n_runs} runs, {FORMATION_SEGMENT_PCT}% segments){label_line}",
                 fontsize=13, color=TEXT_COLOR)
    ax.set_xlabel("Formation Position", fontsize=11, color=TEXT_COLOR)
    ax.set_ylabel("Slide ROP (ft/hr)", fontsize=11, color=TEXT_COLOR)
    ax.legend(loc="upper right", frameon=False, fontsize=10)
    ax.set_ylim(bottom=0)
    ax.yaxis.set_minor_locator(mticker.AutoMinorLocator(2))

    safe_name = group_key.replace(" ", "_").replace("/", "-").replace("|", "_")
    _finalize_figure(fig, ax)
    fig.savefig(os.path.join(out_dir, f"vert_slide_{safe_name}.png"), dpi=170)
    plt.close(fig)


def plot_rotary_comparison_vertical(groups, roadmap, out_dir, section_label=None):
    """Head-to-head rotary P50 comparison by formation segment."""
    fig, ax = plt.subplots(figsize=(16, 7))

    eligible = {gk: gd for gk, gd in groups.items()
                if gd["meta"].get("num_runs", 0) >= MIN_RUNS_FOR_COMPARISON}

    ranked = sorted(eligible.items(), key=lambda x: -x[1]["meta"].get("num_runs", 0))
    for ci, (gk, gd) in enumerate(ranked):
        rotary = gd["rotary"]
        x_pos = []
        y_vals = []
        for i, key in enumerate(roadmap):
            if key in rotary and rotary[key]["confident"]:
                x_pos.append(i)
                y_vals.append(rotary[key]["p50"])
        if not x_pos:
            continue
        color = COLORS[ci % len(COLORS)] if ci < 6 else RUN_LINE_COLOR
        lw = 2.6 if ci < 3 else 1.8
        alpha = 0.95 if ci < 3 else 0.75
        n = gd["meta"].get("num_runs", "?")
        ax.plot(x_pos, y_vals, color=color, linewidth=lw, alpha=alpha, label=f"{gk} ({n} runs)")

    ticks, tick_labels, bound_pos, bound_labels = format_formation_labels(roadmap)
    for bp in bound_pos:
        ax.axvline(x=bp, color=AXIS_EDGE_COLOR, linewidth=0.8, linestyle="--", alpha=0.6)
    for bp, bl in zip(bound_pos, bound_labels):
        ax.text(bp + 1, ax.get_ylim()[1] * 0.97, bl, fontsize=8, rotation=45,
                va="top", ha="left", color=TEXT_COLOR)

    ax.set_xticks(ticks)
    ax.set_xticklabels(tick_labels, fontsize=7, rotation=45)

    label_line = f"\n{section_label}" if section_label else ""
    ax.set_title(f"Rotary ROP Comparison (P50) by Formation{label_line}", fontsize=14, color=TEXT_COLOR)
    ax.set_xlabel("Formation Position", fontsize=12, color=TEXT_COLOR)
    ax.set_ylabel("Rotary ROP (ft/hr)", fontsize=12, color=TEXT_COLOR)
    ax.legend(loc="upper right", fontsize=9, frameon=False)
    ax.set_ylim(bottom=0)
    ax.yaxis.set_minor_locator(mticker.AutoMinorLocator(2))

    _finalize_figure(fig, ax)
    fig.savefig(os.path.join(out_dir, "vert_comparison_rotary.png"), dpi=170)
    plt.close(fig)


def plot_slide_comparison_vertical(groups, roadmap, out_dir, section_label=None):
    """Head-to-head slide P50 comparison by formation segment."""
    fig, ax = plt.subplots(figsize=(16, 7))

    eligible = {gk: gd for gk, gd in groups.items()
                if gd["meta"].get("num_runs", 0) >= MIN_RUNS_FOR_COMPARISON}

    ranked = sorted(eligible.items(), key=lambda x: -x[1]["meta"].get("num_runs", 0))
    for ci, (gk, gd) in enumerate(ranked):
        slide = gd["slide"]
        x_pos = []
        y_vals = []
        for i, key in enumerate(roadmap):
            if key in slide and slide[key]["confident"]:
                x_pos.append(i)
                y_vals.append(slide[key]["p50"])
        if not x_pos:
            continue
        color = COLORS[ci % len(COLORS)] if ci < 6 else RUN_LINE_COLOR
        lw = 2.6 if ci < 3 else 1.8
        alpha = 0.95 if ci < 3 else 0.75
        n = gd["meta"].get("num_runs", "?")
        ax.plot(x_pos, y_vals, color=color, linewidth=lw, alpha=alpha, label=f"{gk} ({n} runs)")

    ticks, tick_labels, bound_pos, bound_labels = format_formation_labels(roadmap)
    for bp in bound_pos:
        ax.axvline(x=bp, color=AXIS_EDGE_COLOR, linewidth=0.8, linestyle="--", alpha=0.6)
    for bp, bl in zip(bound_pos, bound_labels):
        ax.text(bp + 1, ax.get_ylim()[1] * 0.97, bl, fontsize=8, rotation=45,
                va="top", ha="left", color=TEXT_COLOR)

    ax.set_xticks(ticks)
    ax.set_xticklabels(tick_labels, fontsize=7, rotation=45)

    label_line = f"\n{section_label}" if section_label else ""
    ax.set_title(f"Slide ROP Comparison (P50) by Formation{label_line}", fontsize=14, color=TEXT_COLOR)
    ax.set_xlabel("Formation Position", fontsize=12, color=TEXT_COLOR)
    ax.set_ylabel("Slide ROP (ft/hr)", fontsize=12, color=TEXT_COLOR)
    ax.legend(loc="upper right", fontsize=9, frameon=False)
    ax.set_ylim(bottom=0)
    ax.yaxis.set_minor_locator(mticker.AutoMinorLocator(2))

    _finalize_figure(fig, ax)
    fig.savefig(os.path.join(out_dir, "vert_comparison_slide.png"), dpi=170)
    plt.close(fig)


def plot_ttd_ranking_vertical(ttd_data, out_dir, section_label=None):
    """TTD ranking bar chart for vertical mode."""
    valid = [t for t in ttd_data if float(t["ttd_hours"]) > 0]
    if not valid:
        return

    valid.sort(key=lambda t: float(t["ttd_hours"]))

    fig, ax = plt.subplots(figsize=(10, max(4, len(valid) * 0.8)))

    labels = [f"{t['group_key']} ({t['num_runs']} runs)" for t in valid]
    hours = [float(t["ttd_hours"]) for t in valid]
    colors_bar = [COLORS[i % len(COLORS)] for i in range(len(valid))]

    y_pos = range(len(valid))
    bars = ax.barh(y_pos, hours, color=colors_bar, height=0.64, alpha=0.9)

    for bar, h in zip(bars, hours):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{h:.1f} hrs ({h/24:.2f} days)",
                va="center", fontsize=9, color=TEXT_COLOR)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=10)
    ax.set_xlabel("Time to TD (hours)", fontsize=12, color=TEXT_COLOR)
    label_line = f"\n{section_label}" if section_label else "\n(Vertical Section, observed slide %)"
    ax.set_title(f"Estimated Time to TD by Equivalent BHA{label_line}", fontsize=13, color=TEXT_COLOR)
    ax.grid(True, axis="x", color=GRID_COLOR, alpha=0.8)
    ax.invert_yaxis()
    ax.xaxis.set_minor_locator(mticker.AutoMinorLocator(2))

    _finalize_figure(fig, ax)
    fig.savefig(os.path.join(out_dir, "vert_ttd_ranking.png"), dpi=170)
    plt.close(fig)


# Import FORMATION_SEGMENT_PCT from build script at module level
FORMATION_SEGMENT_PCT = 10


# ─────────────────────────────────────────────────────────────────────
# Main entry point
# ─────────────────────────────────────────────────────────────────────

def main():
    # Parse arguments
    mode = "lateral"
    data_dir = None
    output_dir = None
    section_label = None
    section_name = None
    export_csv = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--mode" and i + 1 < len(args):
            mode = args[i + 1].lower()
            i += 2
        elif args[i] == "--data-dir" and i + 1 < len(args):
            data_dir = args[i + 1]
            i += 2
        elif args[i] == "--output-dir" and i + 1 < len(args):
            output_dir = args[i + 1]
            i += 2
        elif args[i] == "--section-label" and i + 1 < len(args):
            section_label = args[i + 1]
            i += 2
        elif args[i] == "--section" and i + 1 < len(args):
            section_name = args[i + 1]
            i += 2
        elif args[i] == "--export-csv":
            export_csv = True
            i += 1
        else:
            i += 1

    if data_dir is None:
        data_dir = SCRIPT_DIR
    elif not os.path.isabs(data_dir):
        data_dir = os.path.join(SCRIPT_DIR, data_dir)

    if output_dir is None:
        output_dir = OUT_DIR
    elif not os.path.isabs(output_dir):
        output_dir = os.path.join(SCRIPT_DIR, output_dir)

    os.makedirs(output_dir, exist_ok=True)

    if section_name is None:
        section_name = os.path.basename(data_dir) if data_dir else "bha_selection"

    if mode == "vertical":
        main_vertical(data_dir, output_dir, section_label, section_name, export_csv)
    else:
        main_lateral(data_dir, output_dir, section_label, section_name, export_csv)


def main_lateral(data_dir=None, output_dir=None, section_label=None,
                 section_name=None, export_csv=False):
    """Generate lateral (distance-based) charts."""
    data_dir = data_dir or SCRIPT_DIR
    output_dir = output_dir or OUT_DIR
    section_name = section_name or os.path.basename(data_dir)
    label_suffix = f" - {section_label}" if section_label else ""

    print(f"\n{'=' * 70}")
    print(f"  GENERATING ROP TYPE CURVE CHARTS (LATERAL){label_suffix}")
    print(f"  Data:   {data_dir}")
    print(f"  Output: {output_dir}")
    print(f"{'=' * 70}\n")

    run_info = db.get_latest_run()
    rid = run_info["id"] if run_info else None
    gdf = db.load_rop_curves_by_group(section_name, "lateral", run_id=rid)
    rdf = db.load_rop_curves_per_run(section_name, "lateral", run_id=rid)
    groups = _parquet_records_to_groups(gdf.to_dict("records"), "lateral") if gdf is not None and not gdf.empty else None
    per_run = _parquet_records_to_per_run(rdf.to_dict("records"), "lateral") if rdf is not None and not rdf.empty else None
    ttd_data = db.get_ttd_rankings(run_info["id"], section_name) if run_info else []

    if groups is None or not groups:
        print("ERROR: Could not load group curves from DB/Parquet. Run build_rop_curves.py first.")
        sys.exit(1)
    if per_run is None or not per_run:
        print("ERROR: Could not load per-run curves from DB/Parquet. Run build_rop_curves.py first.")
        sys.exit(1)

    print(f"  Loaded {len(groups)} groups, {len(per_run)} runs")

    for gk, gd in groups.items():
        n = gd["meta"].get("num_runs", 0)
        if n < MIN_RUNS_FOR_COMPARISON:
            continue
        print(f"  Plotting: {gk} ({n} runs)...")
        plot_group_rotary(gk, gd, per_run, output_dir, section_label)
        plot_group_slide(gk, gd, per_run, output_dir, section_label)

    print(f"  Plotting: Rotary comparison...")
    plot_rotary_comparison(groups, output_dir, section_label)

    print(f"  Plotting: Slide comparison...")
    plot_slide_comparison(groups, output_dir, section_label)

    print(f"  Plotting: TTD ranking...")
    plot_ttd_ranking(ttd_data, output_dir, section_label)

    chart_files = [f for f in os.listdir(output_dir) if f.endswith(".png")]
    print(f"\n  Generated {len(chart_files)} charts:")
    for cf in sorted(chart_files):
        print(f"    {cf}")

    print(f"\n  All charts saved to: {output_dir}")


def main_vertical(data_dir=None, output_dir=None, section_label=None,
                  section_name=None, export_csv=False):
    """Generate vertical (formation-based) charts."""
    data_dir = data_dir or SCRIPT_DIR
    output_dir = output_dir or OUT_DIR
    section_name = section_name or os.path.basename(data_dir)
    label_suffix = f" - {section_label}" if section_label else ""

    print(f"\n{'=' * 70}")
    print(f"  GENERATING ROP TYPE CURVE CHARTS (VERTICAL / FORMATION){label_suffix}")
    print(f"  Data:   {data_dir}")
    print(f"  Output: {output_dir}")
    print(f"{'=' * 70}\n")

    run_info = db.get_latest_run()
    rid = run_info["id"] if run_info else None
    roadmap = db.load_formation_roadmap(section_name, mode="vertical", run_id=rid)
    if not roadmap:
        print("ERROR: Formation roadmap not found in DB/Parquet. Run build_rop_curves.py --mode vertical first.")
        sys.exit(1)
    gdf = db.load_rop_curves_by_group(section_name, "vertical", run_id=rid)
    rdf = db.load_rop_curves_per_run(section_name, "vertical", run_id=rid)
    groups = _parquet_records_to_groups(gdf.to_dict("records"), "vertical") if gdf is not None and not gdf.empty else None
    per_run = _parquet_records_to_per_run(rdf.to_dict("records"), "vertical") if rdf is not None and not rdf.empty else None
    ttd_data = db.get_ttd_rankings(run_info["id"], section_name) if run_info else []

    if groups is None or not groups:
        print("ERROR: Could not load group curves from DB/Parquet. Run build_rop_curves.py --mode vertical first.")
        sys.exit(1)
    if per_run is None or not per_run:
        print("ERROR: Could not load per-run curves from DB/Parquet. Run build_rop_curves.py --mode vertical first.")
        sys.exit(1)

    print(f"  Loaded {len(groups)} groups, {len(per_run)} runs, "
          f"{len(roadmap)} formation segments")

    for gk, gd in groups.items():
        n = gd["meta"].get("num_runs", 0)
        if n < MIN_RUNS_FOR_COMPARISON:
            continue
        print(f"  Plotting: {gk} ({n} runs)...")
        plot_group_rotary_vertical(gk, gd, per_run, roadmap, output_dir, section_label)
        plot_group_slide_vertical(gk, gd, per_run, roadmap, output_dir, section_label)

    print(f"  Plotting: Rotary comparison (formation)...")
    plot_rotary_comparison_vertical(groups, roadmap, output_dir, section_label)

    print(f"  Plotting: Slide comparison (formation)...")
    plot_slide_comparison_vertical(groups, roadmap, output_dir, section_label)

    print(f"  Plotting: TTD ranking (vertical)...")
    plot_ttd_ranking_vertical(ttd_data, output_dir, section_label)

    chart_files = [f for f in os.listdir(output_dir) if f.endswith(".png")
                   and f.startswith("vert_")]
    print(f"\n  Generated {len(chart_files)} vertical charts:")
    for cf in sorted(chart_files):
        print(f"    {cf}")

    print(f"\n  All charts saved to: {output_dir}")


if __name__ == "__main__":
    main()
