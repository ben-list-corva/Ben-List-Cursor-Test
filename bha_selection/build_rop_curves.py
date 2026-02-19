"""Build ROP type curves from 1ft data.

Lateral mode (default):
  Dual x-axis approach:
    - Rotary ROP curves binned by distance_from_run_start (bit wear degradation)
    - Slide ROP curves binned by distance_from_lateral_start (friction/drag degradation)
  Slide curves use larger bins (250 ft) than rotary (100 ft).

Vertical mode (--mode vertical):
  Formation-based approach:
    - Both rotary and slide ROP curves binned by 10% formation segments
    - X-axis is "Formation Name + Segment %" (categorical)
    - Captures formation-driven ROP variation

Both modes apply rolling median smoothing and produce per-run curves,
per-group P10/P50/P90 curves, agitator impact, and Time-to-TD ranking.

Usage:
    python build_rop_curves.py [rop_1ft_data.csv] [--bin-size 100] [--lateral-length 10000] [--slide-pct 0.12]
    python build_rop_curves.py rop_1ft_data_vertical.csv --mode vertical --section-length 5000 --slide-pct 0.20
"""
import csv
import json
import os
import re
import sys
import statistics
from collections import defaultdict

import pandas as pd

import db

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_ROTARY_BIN = 100   # ft -- rotary has plenty of data
DEFAULT_SLIDE_BIN = 250    # ft -- slide is sparser, needs larger bins
ROLLING_WINDOW = 5         # bins for rolling median smoothing (lateral)
ROLLING_WINDOW_VERT = 3    # bins for rolling median smoothing (vertical, fewer segments)
FORMATION_SEGMENT_PCT = 10 # % per formation segment
MIN_LATERAL_COVERAGE_PCT = 0.85
MIN_BIT_SUBSET_RUNS = 2


def _clean_text(value, default="N/A"):
    if value is None:
        return default
    text = str(value).strip()
    if not text or text.lower() in {"n/a", "na", "none", "null", "?"}:
        return default
    return text


def _parse_motor_lobes(lobe_config):
    text = _clean_text(lobe_config, default="")
    if "/" not in text:
        return "N/A", "N/A"
    parts = text.split("/", 1)
    rotor = _clean_text(parts[0], default="N/A")
    stator = _clean_text(parts[1], default="N/A")
    return rotor, stator


def _parse_motor_stages(motor_model, motor_stages=None):
    explicit = _clean_text(motor_stages, default="")
    if explicit:
        return explicit
    text = _clean_text(motor_model, default="")
    if not text:
        return "N/A"
    match = re.search(r"(\d+)\s*(?:stage|stages|stg)\b", text, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    return "N/A"


def _build_group_equipment_metadata(run_list):
    motor_counts = defaultdict(lambda: {"num_runs": 0, "total_feet": 0})
    bit_counts = defaultdict(lambda: {"num_runs": 0, "total_feet": 0})

    for run_info in run_list:
        motor_diam = _clean_text(run_info.get("motor_diam"), default="N/A")
        rotor = _clean_text(run_info.get("motor_rotor_lobes"), default="N/A")
        stator = _clean_text(run_info.get("motor_stator_lobes"), default="N/A")
        stages = _clean_text(run_info.get("motor_stages"), default="N/A")
        motor_key = (motor_diam, rotor, stator, stages)
        motor_counts[motor_key]["num_runs"] += 1
        motor_counts[motor_key]["total_feet"] += int(run_info.get("total_feet", 0) or 0)

        bit_mfg = _clean_text(run_info.get("bit_manufacturer"), default="Unknown")
        bit_model = _clean_text(run_info.get("bit_model"), default="Unknown")
        bit_key = (bit_mfg, bit_model)
        bit_counts[bit_key]["num_runs"] += 1
        bit_counts[bit_key]["total_feet"] += int(run_info.get("total_feet", 0) or 0)

    common_motor = {
        "motor_diam": "N/A",
        "rotor_lobes": "N/A",
        "stator_lobes": "N/A",
        "stages": "N/A",
        "label": "N/A",
    }
    if motor_counts:
        ranked_motors = sorted(
            motor_counts.items(),
            key=lambda x: (-x[1]["num_runs"], -x[1]["total_feet"], x[0]),
        )
        best_motor_key, _ = ranked_motors[0]
        motor_diam, rotor, stator, stages = best_motor_key
        common_motor = {
            "motor_diam": motor_diam,
            "rotor_lobes": rotor,
            "stator_lobes": stator,
            "stages": stages,
            "label": f'{motor_diam}", {rotor}/{stator}, {stages} stg',
        }

    bit_usage = []
    for (bit_mfg, bit_model), counts in bit_counts.items():
        bit_usage.append({
            "bit_manufacturer": bit_mfg,
            "bit_model": bit_model,
            "num_runs": counts["num_runs"],
            "total_feet": counts["total_feet"],
        })
    bit_usage.sort(
        key=lambda x: (
            -int(x.get("num_runs", 0)),
            -int(x.get("total_feet", 0)),
            x.get("bit_manufacturer", ""),
            x.get("bit_model", ""),
        )
    )
    return common_motor, bit_usage


def _group_runs_by_bit(run_list):
    grouped = defaultdict(list)
    for run_info in run_list:
        bit_mfg = _clean_text(run_info.get("bit_manufacturer"), default="Unknown")
        bit_model = _clean_text(run_info.get("bit_model"), default="Unknown")
        grouped[(bit_mfg, bit_model)].append(run_info)
    return grouped


def load_1ft_data(csv_path):
    """Load the per-foot drilling data."""
    rows = []
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                row["rop_ft_hr"] = float(row["rop_ft_hr"])
                row["distance_from_run_start"] = float(row["distance_from_run_start"])
                row["distance_from_lateral_start"] = float(row["distance_from_lateral_start"])
            except (ValueError, KeyError):
                continue
            rows.append(row)
    return rows


def percentile(data, pct):
    """Compute percentile from sorted data."""
    if not data:
        return None
    s = sorted(data)
    k = (len(s) - 1) * pct / 100.0
    f = int(k)
    c = f + 1
    if c >= len(s):
        return s[f]
    return s[f] + (k - f) * (s[c] - s[f])


def bin_value(distance, bin_size):
    """Return the bin start for a given distance."""
    return int(distance // bin_size) * bin_size


def rolling_median(values, window):
    """Apply a centered rolling median to a list of values.

    Returns a list of the same length. Edge values use a smaller window.
    None values are passed through unchanged.
    """
    n = len(values)
    if n == 0:
        return []
    result = []
    half = window // 2
    for i in range(n):
        lo = max(0, i - half)
        hi = min(n, i + half + 1)
        neighborhood = [v for v in values[lo:hi] if v is not None]
        if neighborhood:
            result.append(round(statistics.median(neighborhood), 1))
        else:
            result.append(values[i])
    return result


def smooth_group_curve(curve_dict, window):
    """Apply rolling median smoothing to a group-level curve dict.

    curve_dict is {bin_start: {p10, p50, p90, num_runs, confident}}.
    Smooths p10, p50, p90 independently while preserving metadata.
    """
    if not curve_dict:
        return curve_dict
    bins_sorted = sorted(curve_dict.keys())
    p10s = [curve_dict[b]["p10"] for b in bins_sorted]
    p50s = [curve_dict[b]["p50"] for b in bins_sorted]
    p90s = [curve_dict[b]["p90"] for b in bins_sorted]

    p10_smooth = rolling_median(p10s, window)
    p50_smooth = rolling_median(p50s, window)
    p90_smooth = rolling_median(p90s, window)

    smoothed = {}
    for i, b in enumerate(bins_sorted):
        smoothed[b] = {
            "p10": p10_smooth[i],
            "p50": p50_smooth[i],
            "p90": p90_smooth[i],
            "num_runs": curve_dict[b]["num_runs"],
            "confident": curve_dict[b]["confident"],
        }
    return smoothed


def load_1ft_data_vertical(csv_path):
    """Load per-foot data for vertical mode (with formation columns)."""
    rows = []
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                row["rop_ft_hr"] = float(row["rop_ft_hr"])
                row["distance_from_run_start"] = float(row.get("distance_from_run_start", 0))
            except (ValueError, KeyError):
                continue
            # Formation columns are strings; skip rows without formation mapping
            if not row.get("formation_name"):
                continue
            try:
                row["formation_pct"] = float(row["formation_pct"])
                row["formation_segment"] = int(row["formation_segment"])
            except (ValueError, KeyError, TypeError):
                continue
            rows.append(row)
    return rows


def make_formation_bin_key(formation_name, segment):
    """Create a sortable formation bin key like 'Wilcox|50'."""
    return f"{formation_name}|{segment}"


def parse_formation_bin_key(key):
    """Parse a formation bin key back to (formation_name, segment)."""
    parts = key.rsplit("|", 1)
    return parts[0], int(parts[1])


def build_formation_roadmap(rows):
    """Build an ordered list of unique formation segments from the data.

    Returns a list of formation bin keys in stratigraphic order (by the
    minimum TVD/hole_depth seen for each formation).
    """
    # Find median depth for each formation to determine ordering
    fm_depths = defaultdict(list)
    for r in rows:
        fm = r.get("formation_name", "")
        if fm:
            try:
                fm_depths[fm].append(float(r.get("hole_depth", 0)))
            except (ValueError, TypeError):
                pass

    # Order formations by median depth (shallowest first)
    fm_order = sorted(fm_depths.keys(), key=lambda f: statistics.median(fm_depths[f]))

    # Build ordered list of all formation segments
    roadmap = []
    for fm in fm_order:
        for seg in range(0, 100, FORMATION_SEGMENT_PCT):
            key = make_formation_bin_key(fm, seg)
            roadmap.append(key)

    return roadmap, fm_order


def build_per_run_curves_vertical(rows):
    """Build per-run curves for vertical mode, binned by formation segment.

    Each run produces two curve dicts:
      - rotary: {formation_bin_key: {median_rop, count}}
      - slide:  {formation_bin_key: {median_rop, count}}
    """
    run_data = defaultdict(list)
    for r in rows:
        run_key = (r["asset_id"], r["bha_number"])
        run_data[run_key].append(r)

    per_run = {}
    for run_key, feet in run_data.items():
        meta = feet[0]
        run_info = {
            "asset_id": meta["asset_id"],
            "well_name": meta["well_name"],
            "operator": meta.get("operator", ""),
            "bha_number": meta["bha_number"],
            "equiv_bha_key": meta["equiv_bha_key"],
            "has_agitator": meta.get("has_agitator", "False"),
            "bit_manufacturer": meta.get("bit_manufacturer", ""),
            "bit_model": meta.get("bit_model", ""),
            "motor_diam": meta.get("motor_od", ""),
            "motor_model": meta.get("motor_model", ""),
            "motor_lobe_config": meta.get("motor_lobe_config", ""),
            "motor_stages_raw": meta.get("motor_stages", ""),
            "motor_rotor_lobes": "N/A",
            "motor_stator_lobes": "N/A",
            "motor_stages": "N/A",
            "total_feet": len(feet),
        }
        rotor_lobes, stator_lobes = _parse_motor_lobes(run_info["motor_lobe_config"])
        run_info["motor_rotor_lobes"] = rotor_lobes
        run_info["motor_stator_lobes"] = stator_lobes
        run_info["motor_stages"] = _parse_motor_stages(
            run_info["motor_model"],
            run_info.get("motor_stages_raw"),
        )

        # Rotary bins by formation segment
        rotary_bins = defaultdict(list)
        for f in feet:
            if f["state"] == "Rotary Drilling":
                key = make_formation_bin_key(f["formation_name"], f["formation_segment"])
                rotary_bins[key].append(f["rop_ft_hr"])

        # Slide bins by formation segment
        slide_bins = defaultdict(list)
        for f in feet:
            if f["state"] == "Slide Drilling":
                key = make_formation_bin_key(f["formation_name"], f["formation_segment"])
                slide_bins[key].append(f["rop_ft_hr"])

        rotary_curve = {}
        for key, rops in rotary_bins.items():
            rotary_curve[key] = {
                "median_rop": round(statistics.median(rops), 1),
                "count": len(rops),
            }

        slide_curve = {}
        for key, rops in slide_bins.items():
            slide_curve[key] = {
                "median_rop": round(statistics.median(rops), 1),
                "count": len(rops),
            }

        # Slide percentage per formation segment
        all_bins = defaultdict(lambda: {"rotary": 0, "slide": 0})
        for f in feet:
            key = make_formation_bin_key(f["formation_name"], f["formation_segment"])
            if f["state"] == "Rotary Drilling":
                all_bins[key]["rotary"] += 1
            elif f["state"] == "Slide Drilling":
                all_bins[key]["slide"] += 1

        slide_pct_curve = {}
        for key, counts in all_bins.items():
            total = counts["rotary"] + counts["slide"]
            if total > 0:
                slide_pct_curve[key] = round(counts["slide"] / total, 3)

        # Count rotary vs slide feet for per-group slide pct
        rotary_ft = sum(1 for f in feet if f["state"] == "Rotary Drilling")
        slide_ft = sum(1 for f in feet if f["state"] == "Slide Drilling")
        run_info["rotary_feet"] = rotary_ft
        run_info["slide_feet"] = slide_ft

        run_info["rotary_curve"] = rotary_curve
        run_info["slide_curve"] = slide_curve
        run_info["slide_pct_curve"] = slide_pct_curve
        per_run[run_key] = run_info

    return per_run


def build_group_curves_vertical(per_run, roadmap, min_runs_for_confidence=3):
    """Aggregate per-run formation curves into per-group P10/P50/P90.

    Uses the roadmap ordering for smoothing.
    """
    groups = defaultdict(list)
    for run_key, run_info in per_run.items():
        groups[run_info["equiv_bha_key"]].append(run_info)

    group_curves = {}
    for group_key, run_list in groups.items():
        # Collect all runs' median ROPs at each formation bin
        rotary_bin_rops = defaultdict(list)
        slide_bin_rops = defaultdict(list)
        slide_bin_rops_agitator = defaultdict(list)
        slide_bin_rops_no_agitator = defaultdict(list)
        slide_pct_bin = defaultdict(list)

        for run_info in run_list:
            has_agitator = str(run_info.get("has_agitator", "")).lower() in ("true", "1", "yes")

            for key, data in run_info["rotary_curve"].items():
                rotary_bin_rops[key].append(data["median_rop"])

            for key, data in run_info["slide_curve"].items():
                slide_bin_rops[key].append(data["median_rop"])
                if has_agitator:
                    slide_bin_rops_agitator[key].append(data["median_rop"])
                else:
                    slide_bin_rops_no_agitator[key].append(data["median_rop"])

            for key, pct in run_info["slide_pct_curve"].items():
                slide_pct_bin[key].append(pct)

        # Build rotary P10/P50/P90 (ordered by roadmap)
        rotary_group = {}
        for key in roadmap:
            if key in rotary_bin_rops:
                rops = rotary_bin_rops[key]
                n = len(rops)
                rotary_group[key] = {
                    "p10": round(percentile(rops, 10), 1),
                    "p50": round(percentile(rops, 50), 1),
                    "p90": round(percentile(rops, 90), 1),
                    "num_runs": n,
                    "confident": n >= min_runs_for_confidence,
                }

        # Build slide P10/P50/P90
        slide_group = {}
        for key in roadmap:
            if key in slide_bin_rops:
                rops = slide_bin_rops[key]
                n = len(rops)
                slide_group[key] = {
                    "p10": round(percentile(rops, 10), 1),
                    "p50": round(percentile(rops, 50), 1),
                    "p90": round(percentile(rops, 90), 1),
                    "num_runs": n,
                    "confident": n >= min_runs_for_confidence,
                }

        # Agitator impact
        agitator_impact = {}
        all_slide_keys = set(slide_bin_rops_agitator.keys()) | set(slide_bin_rops_no_agitator.keys())
        for key in sorted(all_slide_keys):
            ag = slide_bin_rops_agitator.get(key, [])
            no_ag = slide_bin_rops_no_agitator.get(key, [])
            agitator_impact[key] = {
                "agitator_p50": round(percentile(ag, 50), 1) if ag else None,
                "no_agitator_p50": round(percentile(no_ag, 50), 1) if no_ag else None,
                "agitator_runs": len(ag),
                "no_agitator_runs": len(no_ag),
            }

        # Slide % P50
        slide_pct_group = {}
        for key in roadmap:
            if key in slide_pct_bin:
                pcts = slide_pct_bin[key]
                slide_pct_group[key] = {
                    "p50": round(percentile(pcts, 50), 3),
                    "num_runs": len(pcts),
                }

        # Apply rolling median smoothing using roadmap order
        rotary_smooth = smooth_formation_curves(rotary_group, roadmap, ROLLING_WINDOW_VERT)
        slide_smooth = smooth_formation_curves(slide_group, roadmap, ROLLING_WINDOW_VERT)

        num_agitator = sum(1 for ri in run_list
                          if str(ri.get("has_agitator", "")).lower() in ("true", "1", "yes"))

        # Compute per-group overall slide percentage from actual data
        total_rotary_ft = sum(ri.get("rotary_feet", 0) for ri in run_list)
        total_slide_ft = sum(ri.get("slide_feet", 0) for ri in run_list)
        total_drilling_ft = total_rotary_ft + total_slide_ft
        is_rss = "RSS" in group_key.upper()
        if is_rss:
            grp_slide_pct = 0.0
        elif total_drilling_ft > 0:
            grp_slide_pct = round(total_slide_ft / total_drilling_ft, 4)
        else:
            grp_slide_pct = 0.0
        common_motor, bit_usage = _build_group_equipment_metadata(run_list)

        group_curves[group_key] = {
            "num_runs": len(run_list),
            "num_wells": len(set(ri["asset_id"] for ri in run_list)),
            "num_with_agitator": num_agitator,
            "group_slide_pct": grp_slide_pct,
            "is_rss": is_rss,
            "rotary": rotary_smooth,
            "rotary_raw": rotary_group,
            "slide": slide_smooth,
            "slide_raw": slide_group,
            "slide_pct": slide_pct_group,
            "agitator_impact": agitator_impact,
            "common_motor": common_motor,
            "bit_usage": bit_usage,
            "run_list": list(run_list),
        }

    return group_curves


def smooth_formation_curves(curve_dict, roadmap, window):
    """Apply rolling median smoothing to formation-based curves.

    Uses roadmap ordering so smoothing respects stratigraphic sequence.
    Only smooths bins that exist in curve_dict.
    """
    if not curve_dict:
        return curve_dict

    # Get the ordered keys that exist in both roadmap and curve_dict
    ordered_keys = [k for k in roadmap if k in curve_dict]
    if not ordered_keys:
        return curve_dict

    p10s = [curve_dict[k]["p10"] for k in ordered_keys]
    p50s = [curve_dict[k]["p50"] for k in ordered_keys]
    p90s = [curve_dict[k]["p90"] for k in ordered_keys]

    p10_smooth = rolling_median(p10s, window)
    p50_smooth = rolling_median(p50s, window)
    p90_smooth = rolling_median(p90s, window)

    smoothed = {}
    for i, k in enumerate(ordered_keys):
        smoothed[k] = {
            "p10": p10_smooth[i],
            "p50": p50_smooth[i],
            "p90": p90_smooth[i],
            "num_runs": curve_dict[k]["num_runs"],
            "confident": curve_dict[k]["confident"],
        }
    return smoothed


def filter_groups_by_formation_coverage(group_curves, roadmap, fm_order,
                                        max_missing=1):
    """Exclude groups missing rotary data in too many formations.

    A formation counts as 'covered' if at least one of its segments
    has a confident rotary entry.  Groups missing more than max_missing
    formations are excluded from downstream TTD and charting.

    Returns (passed_dict, excluded_list) where excluded_list contains
    tuples of (group_key, list_of_missing_formation_names).
    """
    passed = {}
    excluded = []
    for gk, gc in group_curves.items():
        missing_fms = []
        for fm in fm_order:
            has_rotary = any(
                gc["rotary"].get(f"{fm}|{seg}", {}).get("confident", False)
                for seg in range(0, 100, FORMATION_SEGMENT_PCT)
            )
            if not has_rotary:
                missing_fms.append(fm)
        if len(missing_fms) > max_missing:
            excluded.append((gk, missing_fms))
        else:
            passed[gk] = gc
    return passed, excluded


def _rebuild_single_lateral_group(run_list, rotary_bin, slide_bin):
    if not run_list:
        return None
    temp = {}
    for idx, ri in enumerate(run_list):
        temp[(ri.get("asset_id", ""), f"{ri.get('bha_number', '')}:{idx}")] = ri
    grouped = build_group_curves(temp, rotary_bin, slide_bin)
    return next(iter(grouped.values()), None) if grouped else None


def _rebuild_single_vertical_group(run_list, roadmap):
    if not run_list:
        return None
    temp = {}
    for idx, ri in enumerate(run_list):
        temp[(ri.get("asset_id", ""), f"{ri.get('bha_number', '')}:{idx}")] = ri
    grouped = build_group_curves_vertical(temp, roadmap)
    return next(iter(grouped.values()), None) if grouped else None


def calculate_ttd_vertical(group_curves, roadmap, fm_order, section_length_ft,
                           expected_slide_pct, formation_md_lengths=None,
                           include_bit_breakdown=True):
    """Calculate Time to TD for vertical sections.

    For each formation segment in the roadmap, computes drilling time
    based on P50 rotary and slide ROP.

    Per-group slide percentage: each group uses its own observed slide %
    (from group_slide_pct). RSS groups always use 0%. The expected_slide_pct
    parameter serves as a fallback for groups with no data.

    Also collects per-segment detail and aggregates into whole-formation
    buckets (canonical formation name) for the breakdown table.

    If formation_md_lengths is not provided, distributes section_length_ft
    equally across the formations in the roadmap.
    """
    # Compute MD length per formation segment
    if formation_md_lengths is None:
        n_formations = len(fm_order) if fm_order else 1
        fm_length = section_length_ft / n_formations
        segment_length = fm_length / (100 / FORMATION_SEGMENT_PCT)
    else:
        segment_length = None

    results = []
    for group_key, gc in group_curves.items():
        total_time_hrs = 0
        segments_covered = 0
        segments_missing = 0

        # Use per-group slide pct; fall back to global if not available
        slide_pct = gc.get("group_slide_pct", expected_slide_pct)

        # Per-formation detail collectors keyed by formation name
        fm_detail = {}  # {fm_name: {rot_ft, rot_time, sli_ft, sli_time, rot_rops, sli_rops, total_len}}

        for fm_key in roadmap:
            fm_name, seg_pct = parse_formation_bin_key(fm_key)

            if formation_md_lengths and fm_name in formation_md_lengths:
                seg_len = formation_md_lengths[fm_name] / (100 / FORMATION_SEGMENT_PCT)
            elif segment_length is not None:
                seg_len = segment_length
            else:
                seg_len = section_length_ft / max(len(roadmap), 1)

            rotary_data = gc["rotary"].get(fm_key)
            rotary_rop = rotary_data["p50"] if rotary_data and rotary_data["confident"] else None

            slide_data = gc["slide"].get(fm_key)
            slide_rop = slide_data["p50"] if slide_data and slide_data["confident"] else None

            if rotary_rop and rotary_rop > 0:
                rotary_time = seg_len * (1 - slide_pct) / rotary_rop
            else:
                all_rotary = [v["p50"] for v in gc["rotary"].values() if v["confident"]]
                fallback = statistics.median(all_rotary) if all_rotary else None
                if fallback and fallback > 0:
                    rotary_time = seg_len * (1 - slide_pct) / fallback
                    rotary_rop = fallback
                else:
                    segments_missing += 1
                    continue

            if slide_rop and slide_rop > 0 and slide_pct > 0:
                slide_time = seg_len * slide_pct / slide_rop
            else:
                all_slide = [v["p50"] for v in gc["slide"].values() if v["confident"]]
                fallback = statistics.median(all_slide) if all_slide else None
                if fallback and fallback > 0:
                    slide_time = seg_len * slide_pct / fallback
                    slide_rop = fallback
                else:
                    slide_time = 0
                    slide_rop = 0

            total_time_hrs += rotary_time + slide_time
            segments_covered += 1

            # Accumulate into formation bucket
            if fm_name not in fm_detail:
                fm_detail[fm_name] = {
                    "rot_ft": 0, "rot_time": 0, "sli_ft": 0, "sli_time": 0,
                    "rot_rops": [], "sli_rops": [], "total_len": 0,
                }
            fd = fm_detail[fm_name]
            rot_ft = seg_len * (1 - slide_pct)
            sli_ft = seg_len * slide_pct
            fd["rot_ft"] += rot_ft
            fd["rot_time"] += rotary_time
            fd["sli_ft"] += sli_ft
            fd["sli_time"] += slide_time
            fd["total_len"] += seg_len
            if rotary_rop and rotary_rop > 0:
                fd["rot_rops"].append((rot_ft, rotary_rop))
            if slide_rop and slide_rop > 0:
                fd["sli_rops"].append((sli_ft, slide_rop))

        # Build bucket breakdown ordered by fm_order
        buckets = []
        ordered_fms = [f for f in fm_order if f in fm_detail]
        for extra in fm_detail:
            if extra not in ordered_fms:
                ordered_fms.append(extra)
        for fm_name in ordered_fms:
            fd = fm_detail[fm_name]
            rot_rop_avg = 0
            if fd["rot_rops"]:
                total_w = sum(w for w, _ in fd["rot_rops"])
                rot_rop_avg = round(sum(w * r for w, r in fd["rot_rops"]) / total_w, 1) if total_w else 0
            sli_rop_avg = 0
            if fd["sli_rops"]:
                total_w = sum(w for w, _ in fd["sli_rops"])
                sli_rop_avg = round(sum(w * r for w, r in fd["sli_rops"]) / total_w, 1) if total_w else 0
            buckets.append({
                "label": fm_name,
                "length_ft": round(fd["total_len"], 1),
                "rotary_rop": rot_rop_avg,
                "rotary_time": round(fd["rot_time"], 3),
                "slide_rop": sli_rop_avg,
                "slide_time": round(fd["sli_time"], 3),
                "total_time": round(fd["rot_time"] + fd["sli_time"], 3),
            })

        bit_ttd_by_mfg_model = []
        fastest_bit = None
        if include_bit_breakdown and gc.get("run_list"):
            for (bit_mfg, bit_model), subset_runs in _group_runs_by_bit(gc.get("run_list", [])).items():
                if len(subset_runs) < MIN_BIT_SUBSET_RUNS:
                    continue
                subset_gc = _rebuild_single_vertical_group(subset_runs, roadmap)
                if not subset_gc:
                    continue
                subset_results = calculate_ttd_vertical(
                    group_curves={"subset": subset_gc},
                    roadmap=roadmap,
                    fm_order=fm_order,
                    section_length_ft=section_length_ft,
                    expected_slide_pct=expected_slide_pct,
                    formation_md_lengths=formation_md_lengths,
                    include_bit_breakdown=False,
                )
                if not subset_results:
                    continue
                subset_best = subset_results[0]
                bit_ttd_by_mfg_model.append({
                    "bit_manufacturer": bit_mfg,
                    "bit_model": bit_model,
                    "num_runs": len(subset_runs),
                    "ttd_hours": subset_best.get("ttd_hours", 0),
                    "ttd_days": subset_best.get("ttd_days", 0),
                })
            bit_ttd_by_mfg_model.sort(
                key=lambda x: (
                    float(x.get("ttd_hours", 0) or 0) if float(x.get("ttd_hours", 0) or 0) > 0 else 999999,
                    -int(x.get("num_runs", 0) or 0),
                    x.get("bit_manufacturer", ""),
                    x.get("bit_model", ""),
                )
            )
            if bit_ttd_by_mfg_model:
                fastest_bit = dict(bit_ttd_by_mfg_model[0])

        results.append({
            "group_key": group_key,
            "num_runs": gc["num_runs"],
            "num_wells": gc["num_wells"],
            "target_section_ft": section_length_ft,
            "expected_slide_pct": round(slide_pct, 4),
            "actual_slide_pct": round(slide_pct, 4),
            "is_rss": gc.get("is_rss", False),
            "ttd_hours": round(total_time_hrs, 1),
            "ttd_days": round(total_time_hrs / 24, 2),
            "segments_with_data": segments_covered,
            "segments_missing": segments_missing,
            "common_motor": gc.get("common_motor", {}),
            "bit_ttd_by_mfg_model": bit_ttd_by_mfg_model,
            "fastest_bit": fastest_bit,
            "buckets": buckets,
        })

    results.sort(key=lambda x: x["ttd_hours"] if x["ttd_hours"] > 0 else 9999)
    return results


def save_per_run_csv_vertical(per_run, out_path):
    """Save per-run formation-based curves to CSV."""
    rows = []
    for run_key, run_info in per_run.items():
        for key, data in run_info["rotary_curve"].items():
            fm_name, seg = parse_formation_bin_key(key)
            rows.append({
                "asset_id": run_info["asset_id"],
                "well_name": run_info["well_name"],
                "bha_number": run_info["bha_number"],
                "equiv_bha_key": run_info["equiv_bha_key"],
                "has_agitator": run_info["has_agitator"],
                "curve_type": "rotary",
                "formation_name": fm_name,
                "formation_segment": seg,
                "formation_bin_key": key,
                "median_rop": data["median_rop"],
                "foot_count": data["count"],
            })
        for key, data in run_info["slide_curve"].items():
            fm_name, seg = parse_formation_bin_key(key)
            rows.append({
                "asset_id": run_info["asset_id"],
                "well_name": run_info["well_name"],
                "bha_number": run_info["bha_number"],
                "equiv_bha_key": run_info["equiv_bha_key"],
                "has_agitator": run_info["has_agitator"],
                "curve_type": "slide",
                "formation_name": fm_name,
                "formation_segment": seg,
                "formation_bin_key": key,
                "median_rop": data["median_rop"],
                "foot_count": data["count"],
            })

    if rows:
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"  Per-run curves: {out_path} ({len(rows)} rows)")
    return rows


def save_group_csv_vertical(group_curves, out_path):
    """Save per-group formation-based P10/P50/P90 curves to CSV."""
    rows = []
    for group_key, gc in group_curves.items():
        for key, data in gc["rotary"].items():
            fm_name, seg = parse_formation_bin_key(key)
            rows.append({
                "equiv_bha_key": group_key,
                "num_runs": gc["num_runs"],
                "curve_type": "rotary",
                "formation_name": fm_name,
                "formation_segment": seg,
                "formation_bin_key": key,
                "p10": data["p10"],
                "p50": data["p50"],
                "p90": data["p90"],
                "contributing_runs": data["num_runs"],
                "confident": data["confident"],
            })
        for key, data in gc["slide"].items():
            fm_name, seg = parse_formation_bin_key(key)
            rows.append({
                "equiv_bha_key": group_key,
                "num_runs": gc["num_runs"],
                "curve_type": "slide",
                "formation_name": fm_name,
                "formation_segment": seg,
                "formation_bin_key": key,
                "p10": data["p10"],
                "p50": data["p50"],
                "p90": data["p90"],
                "contributing_runs": data["num_runs"],
                "confident": data["confident"],
            })

    if rows:
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"  Group curves:   {out_path} ({len(rows)} rows)")
    return rows


def build_per_run_curves(rows, rotary_bin, slide_bin):
    """Build per-run binned curves.

    Returns dict keyed by (asset_id, bha_number) with sub-dicts for
    rotary bins (by run-start distance) and slide bins (by lateral-start distance).
    Rotary uses rotary_bin (100 ft), slide uses slide_bin (250 ft).
    """
    # Group by run
    run_data = defaultdict(list)
    for r in rows:
        run_key = (r["asset_id"], r["bha_number"])
        run_data[run_key].append(r)

    per_run = {}
    for run_key, feet in run_data.items():
        meta = feet[0]
        run_info = {
            "asset_id": meta["asset_id"],
            "well_name": meta["well_name"],
            "operator": meta["operator"],
            "bha_number": meta["bha_number"],
            "equiv_bha_key": meta["equiv_bha_key"],
            "has_agitator": meta.get("has_agitator", "False"),
            "bit_manufacturer": meta.get("bit_manufacturer", ""),
            "bit_model": meta.get("bit_model", ""),
            "motor_diam": meta.get("motor_od", ""),
            "motor_model": meta.get("motor_model", ""),
            "motor_lobe_config": meta.get("motor_lobe_config", ""),
            "motor_stages_raw": meta.get("motor_stages", ""),
            "motor_rotor_lobes": "N/A",
            "motor_stator_lobes": "N/A",
            "motor_stages": "N/A",
            "total_feet": len(feet),
        }
        rotor_lobes, stator_lobes = _parse_motor_lobes(run_info["motor_lobe_config"])
        run_info["motor_rotor_lobes"] = rotor_lobes
        run_info["motor_stator_lobes"] = stator_lobes
        run_info["motor_stages"] = _parse_motor_stages(
            run_info["motor_model"],
            run_info.get("motor_stages_raw"),
        )

        # Rotary bins by distance_from_run_start (100 ft bins)
        rotary_bins = defaultdict(list)
        for f in feet:
            if f["state"] == "Rotary Drilling":
                b = bin_value(f["distance_from_run_start"], rotary_bin)
                rotary_bins[b].append(f["rop_ft_hr"])

        # Slide bins by distance_from_lateral_start (250 ft bins)
        slide_bins = defaultdict(list)
        for f in feet:
            if f["state"] == "Slide Drilling":
                b = bin_value(f["distance_from_lateral_start"], slide_bin)
                slide_bins[b].append(f["rop_ft_hr"])

        # Slide percentage by lateral-start distance bins (use slide_bin size)
        all_bins_lat = defaultdict(lambda: {"rotary": 0, "slide": 0})
        for f in feet:
            b = bin_value(f["distance_from_lateral_start"], slide_bin)
            if f["state"] == "Rotary Drilling":
                all_bins_lat[b]["rotary"] += 1
            elif f["state"] == "Slide Drilling":
                all_bins_lat[b]["slide"] += 1

        rotary_curve = {}
        for b, rops in sorted(rotary_bins.items()):
            rotary_curve[b] = {
                "median_rop": round(statistics.median(rops), 1),
                "count": len(rops),
            }

        slide_curve = {}
        for b, rops in sorted(slide_bins.items()):
            slide_curve[b] = {
                "median_rop": round(statistics.median(rops), 1),
                "count": len(rops),
            }

        slide_pct_curve = {}
        for b, counts in sorted(all_bins_lat.items()):
            total = counts["rotary"] + counts["slide"]
            if total > 0:
                slide_pct_curve[b] = round(counts["slide"] / total, 3)

        # Count rotary vs slide feet for per-group slide pct
        rotary_ft = sum(1 for f in feet if f["state"] == "Rotary Drilling")
        slide_ft = sum(1 for f in feet if f["state"] == "Slide Drilling")
        run_info["rotary_feet"] = rotary_ft
        run_info["slide_feet"] = slide_ft

        run_info["rotary_curve"] = rotary_curve
        run_info["slide_curve"] = slide_curve
        run_info["slide_pct_curve"] = slide_pct_curve
        per_run[run_key] = run_info

    return per_run


def build_group_curves(per_run, rotary_bin, slide_bin, min_runs_for_confidence=3):
    """Aggregate per-run curves into per-group P10/P50/P90 curves.

    Applies rolling median smoothing (ROLLING_WINDOW) to slide curves
    to reduce noise from sparse slide data.
    """
    # Group runs by equiv_bha_key
    groups = defaultdict(list)
    for run_key, run_info in per_run.items():
        groups[run_info["equiv_bha_key"]].append(run_info)

    group_curves = {}
    for group_key, run_list in groups.items():
        # Rotary: collect all runs' median ROPs at each run-start bin
        rotary_bin_rops = defaultdict(list)
        for run_info in run_list:
            for b, curve_data in run_info["rotary_curve"].items():
                rotary_bin_rops[b].append(curve_data["median_rop"])

        # Slide: collect all runs' median ROPs at each lateral-start bin
        slide_bin_rops = defaultdict(list)
        slide_bin_rops_agitator = defaultdict(list)
        slide_bin_rops_no_agitator = defaultdict(list)
        for run_info in run_list:
            has_agitator = str(run_info.get("has_agitator", "")).lower() in ("true", "1", "yes")
            for b, curve_data in run_info["slide_curve"].items():
                slide_bin_rops[b].append(curve_data["median_rop"])
                if has_agitator:
                    slide_bin_rops_agitator[b].append(curve_data["median_rop"])
                else:
                    slide_bin_rops_no_agitator[b].append(curve_data["median_rop"])

        # Slide %: collect all runs' slide pct at each lateral-start bin
        slide_pct_bin = defaultdict(list)
        for run_info in run_list:
            for b, pct in run_info["slide_pct_curve"].items():
                slide_pct_bin[b].append(pct)

        # Build rotary P10/P50/P90
        rotary_group = {}
        for b in sorted(rotary_bin_rops.keys()):
            rops = rotary_bin_rops[b]
            n = len(rops)
            rotary_group[b] = {
                "p10": round(percentile(rops, 10), 1),
                "p50": round(percentile(rops, 50), 1),
                "p90": round(percentile(rops, 90), 1),
                "num_runs": n,
                "confident": n >= min_runs_for_confidence,
            }

        # Build slide P10/P50/P90
        slide_group = {}
        for b in sorted(slide_bin_rops.keys()):
            rops = slide_bin_rops[b]
            n = len(rops)
            slide_group[b] = {
                "p10": round(percentile(rops, 10), 1),
                "p50": round(percentile(rops, 50), 1),
                "p90": round(percentile(rops, 90), 1),
                "num_runs": n,
                "confident": n >= min_runs_for_confidence,
            }

        # Agitator vs no-agitator slide comparison
        agitator_impact = {}
        all_slide_bins = set(slide_bin_rops_agitator.keys()) | set(slide_bin_rops_no_agitator.keys())
        for b in sorted(all_slide_bins):
            ag = slide_bin_rops_agitator.get(b, [])
            no_ag = slide_bin_rops_no_agitator.get(b, [])
            agitator_impact[b] = {
                "agitator_p50": round(percentile(ag, 50), 1) if ag else None,
                "no_agitator_p50": round(percentile(no_ag, 50), 1) if no_ag else None,
                "agitator_runs": len(ag),
                "no_agitator_runs": len(no_ag),
            }

        # Slide % P50
        slide_pct_group = {}
        for b in sorted(slide_pct_bin.keys()):
            pcts = slide_pct_bin[b]
            slide_pct_group[b] = {
                "p50": round(percentile(pcts, 50), 3),
                "num_runs": len(pcts),
            }

        # Apply rolling median smoothing to both curve types
        rotary_group_smooth = smooth_group_curve(rotary_group, ROLLING_WINDOW)
        slide_group_smooth = smooth_group_curve(slide_group, ROLLING_WINDOW)

        num_agitator = sum(1 for ri in run_list
                          if str(ri.get("has_agitator", "")).lower() in ("true", "1", "yes"))

        # Compute per-group overall slide percentage from actual data
        total_rotary_ft = sum(ri.get("rotary_feet", 0) for ri in run_list)
        total_slide_ft = sum(ri.get("slide_feet", 0) for ri in run_list)
        total_drilling_ft = total_rotary_ft + total_slide_ft
        is_rss = "RSS" in group_key.upper()
        if is_rss:
            grp_slide_pct = 0.0
        elif total_drilling_ft > 0:
            grp_slide_pct = round(total_slide_ft / total_drilling_ft, 4)
        else:
            grp_slide_pct = 0.0
        common_motor, bit_usage = _build_group_equipment_metadata(run_list)

        group_curves[group_key] = {
            "num_runs": len(run_list),
            "num_wells": len(set(ri["asset_id"] for ri in run_list)),
            "num_with_agitator": num_agitator,
            "group_slide_pct": grp_slide_pct,
            "is_rss": is_rss,
            "rotary": rotary_group_smooth,
            "rotary_raw": rotary_group,
            "slide": slide_group_smooth,
            "slide_raw": slide_group,
            "slide_pct": slide_pct_group,
            "agitator_impact": agitator_impact,
            "common_motor": common_motor,
            "bit_usage": bit_usage,
            "run_list": list(run_list),
        }

    return group_curves


def calculate_ttd(group_curves, target_lateral_length, expected_slide_pct, rotary_bin, slide_bin,
                  bucket_size=1000, include_bit_breakdown=True,
                  min_coverage_pct=MIN_LATERAL_COVERAGE_PCT):
    """Calculate Time to TD for each equivalent BHA group.

    Uses rotary P50 at the corresponding run-length bin and
    slide P50 at the lateral-length bin.
    Iterates in 100-ft steps and looks up the appropriate bin for each curve.

    Per-group slide percentage: each group uses its own observed slide %
    (from group_slide_pct). RSS groups always use 0%. The expected_slide_pct
    parameter serves as a fallback for groups with no data.

    Also collects per-step detail and aggregates into ``bucket_size``-ft
    buckets (default 1000 ft) for the breakdown table.
    """
    step = min(rotary_bin, slide_bin)  # iterate at the finer resolution
    results = []
    for group_key, gc in group_curves.items():
        total_time_hrs = 0
        bins_covered = 0
        bins_missing = 0

        # Use per-group slide pct; fall back to global if not available
        slide_pct = gc.get("group_slide_pct", expected_slide_pct)

        confident_rotary_bins = [
            b for b, v in gc["rotary"].items()
            if v.get("confident", False)
        ]
        confident_slide_bins = [
            b for b, v in gc["slide"].items()
            if v.get("confident", False)
        ]
        rotary_coverage_ft = (
            max(confident_rotary_bins) + rotary_bin if confident_rotary_bins else 0
        )
        slide_coverage_ft = (
            max(confident_slide_bins) + slide_bin if confident_slide_bins else 0
        )
        if slide_pct > 0:
            effective_coverage_ft = min(rotary_coverage_ft, slide_coverage_ft)
        else:
            effective_coverage_ft = rotary_coverage_ft
        min_required_coverage_ft = target_lateral_length * min_coverage_pct

        if effective_coverage_ft < min_required_coverage_ft:
            continue

        # Per-step detail collectors keyed by bucket_start
        bucket_detail = {}  # {bucket_start: {rot_ft, rot_time, sli_ft, sli_time, rot_rops, sli_rops}}

        for pos in range(0, target_lateral_length, step):
            seg_length = min(step, target_lateral_length - pos)
            b_rot = bin_value(pos, rotary_bin)
            b_sli = bin_value(pos, slide_bin)

            rotary_data = gc["rotary"].get(b_rot)
            rotary_rop = rotary_data["p50"] if rotary_data and rotary_data["confident"] else None

            slide_data = gc["slide"].get(b_sli)
            slide_rop = slide_data["p50"] if slide_data and slide_data["confident"] else None

            if rotary_rop and rotary_rop > 0:
                rotary_time = seg_length * (1 - slide_pct) / rotary_rop
            else:
                all_rotary = [v["p50"] for v in gc["rotary"].values() if v["confident"]]
                fallback = statistics.median(all_rotary) if all_rotary else None
                if fallback and fallback > 0:
                    rotary_time = seg_length * (1 - slide_pct) / fallback
                    rotary_rop = fallback
                else:
                    bins_missing += 1
                    continue

            if slide_rop and slide_rop > 0 and slide_pct > 0:
                slide_time = seg_length * slide_pct / slide_rop
            else:
                all_slide = [v["p50"] for v in gc["slide"].values() if v["confident"]]
                fallback = statistics.median(all_slide) if all_slide else None
                if fallback and fallback > 0:
                    slide_time = seg_length * slide_pct / fallback
                    slide_rop = fallback
                else:
                    slide_time = 0
                    slide_rop = 0

            total_time_hrs += rotary_time + slide_time
            bins_covered += 1

            # Accumulate into 1000' bucket
            bk = int(pos // bucket_size) * bucket_size
            if bk not in bucket_detail:
                bucket_detail[bk] = {
                    "rot_ft": 0, "rot_time": 0, "sli_ft": 0, "sli_time": 0,
                    "rot_rops": [], "sli_rops": [],
                }
            bd = bucket_detail[bk]
            rot_ft = seg_length * (1 - slide_pct)
            sli_ft = seg_length * slide_pct
            bd["rot_ft"] += rot_ft
            bd["rot_time"] += rotary_time
            bd["sli_ft"] += sli_ft
            bd["sli_time"] += slide_time
            if rotary_rop and rotary_rop > 0:
                bd["rot_rops"].append((rot_ft, rotary_rop))
            if slide_rop and slide_rop > 0:
                bd["sli_rops"].append((sli_ft, slide_rop))

        # Build bucket breakdown list
        buckets = []
        for bk in sorted(bucket_detail.keys()):
            bd = bucket_detail[bk]
            bk_end = min(bk + bucket_size, target_lateral_length)
            bk_len = bk_end - bk
            # Weighted-average ROP (ft-weighted)
            rot_rop_avg = 0
            if bd["rot_rops"]:
                total_w = sum(w for w, _ in bd["rot_rops"])
                rot_rop_avg = round(sum(w * r for w, r in bd["rot_rops"]) / total_w, 1) if total_w else 0
            sli_rop_avg = 0
            if bd["sli_rops"]:
                total_w = sum(w for w, _ in bd["sli_rops"])
                sli_rop_avg = round(sum(w * r for w, r in bd["sli_rops"]) / total_w, 1) if total_w else 0
            buckets.append({
                "label": f"{bk}-{bk_end}'",
                "length_ft": round(bk_len, 1),
                "rotary_rop": rot_rop_avg,
                "rotary_time": round(bd["rot_time"], 3),
                "slide_rop": sli_rop_avg,
                "slide_time": round(bd["sli_time"], 3),
                "total_time": round(bd["rot_time"] + bd["sli_time"], 3),
            })

        bit_ttd_by_mfg_model = []
        fastest_bit = None
        if include_bit_breakdown and gc.get("run_list"):
            for (bit_mfg, bit_model), subset_runs in _group_runs_by_bit(gc.get("run_list", [])).items():
                if len(subset_runs) < MIN_BIT_SUBSET_RUNS:
                    continue
                subset_gc = _rebuild_single_lateral_group(subset_runs, rotary_bin, slide_bin)
                if not subset_gc:
                    continue
                subset_results = calculate_ttd(
                    group_curves={"subset": subset_gc},
                    target_lateral_length=target_lateral_length,
                    expected_slide_pct=expected_slide_pct,
                    rotary_bin=rotary_bin,
                    slide_bin=slide_bin,
                    bucket_size=bucket_size,
                    include_bit_breakdown=False,
                )
                if not subset_results:
                    # Retry subset ranking without strict coverage gate so
                    # fastest-bit can still surface for sparse but valid subsets.
                    subset_results = calculate_ttd(
                        group_curves={"subset": subset_gc},
                        target_lateral_length=target_lateral_length,
                        expected_slide_pct=expected_slide_pct,
                        rotary_bin=rotary_bin,
                        slide_bin=slide_bin,
                        bucket_size=bucket_size,
                        include_bit_breakdown=False,
                        min_coverage_pct=0.0,
                    )
                if not subset_results:
                    continue
                subset_best = subset_results[0]
                bit_ttd_by_mfg_model.append({
                    "bit_manufacturer": bit_mfg,
                    "bit_model": bit_model,
                    "num_runs": len(subset_runs),
                    "ttd_hours": subset_best.get("ttd_hours", 0),
                    "ttd_days": subset_best.get("ttd_days", 0),
                })
            bit_ttd_by_mfg_model.sort(
                key=lambda x: (
                    float(x.get("ttd_hours", 0) or 0) if float(x.get("ttd_hours", 0) or 0) > 0 else 999999,
                    -int(x.get("num_runs", 0) or 0),
                    x.get("bit_manufacturer", ""),
                    x.get("bit_model", ""),
                )
            )
            if bit_ttd_by_mfg_model:
                fastest_bit = dict(bit_ttd_by_mfg_model[0])

        results.append({
            "group_key": group_key,
            "num_runs": gc["num_runs"],
            "num_wells": gc["num_wells"],
            "target_lateral_ft": target_lateral_length,
            "expected_slide_pct": round(slide_pct, 4),
            "actual_slide_pct": round(slide_pct, 4),
            "is_rss": gc.get("is_rss", False),
            "ttd_hours": round(total_time_hrs, 1),
            "ttd_days": round(total_time_hrs / 24, 2),
            "bins_with_data": bins_covered,
            "bins_missing": bins_missing,
            "common_motor": gc.get("common_motor", {}),
            "bit_ttd_by_mfg_model": bit_ttd_by_mfg_model,
            "fastest_bit": fastest_bit,
            "buckets": buckets,
        })

    results.sort(key=lambda x: x["ttd_hours"] if x["ttd_hours"] > 0 else 9999)
    return results


def save_per_run_csv(per_run, bin_size, out_path):
    """Save per-run curves to CSV."""
    rows = []
    for run_key, run_info in per_run.items():
        # Rotary bins
        for b, data in sorted(run_info["rotary_curve"].items()):
            rows.append({
                "asset_id": run_info["asset_id"],
                "well_name": run_info["well_name"],
                "bha_number": run_info["bha_number"],
                "equiv_bha_key": run_info["equiv_bha_key"],
                "has_agitator": run_info["has_agitator"],
                "curve_type": "rotary",
                "bin_start_ft": b,
                "bin_axis": "distance_from_run_start",
                "median_rop": data["median_rop"],
                "foot_count": data["count"],
            })
        # Slide bins
        for b, data in sorted(run_info["slide_curve"].items()):
            rows.append({
                "asset_id": run_info["asset_id"],
                "well_name": run_info["well_name"],
                "bha_number": run_info["bha_number"],
                "equiv_bha_key": run_info["equiv_bha_key"],
                "has_agitator": run_info["has_agitator"],
                "curve_type": "slide",
                "bin_start_ft": b,
                "bin_axis": "distance_from_lateral_start",
                "median_rop": data["median_rop"],
                "foot_count": data["count"],
            })

    if rows:
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"  Per-run curves: {out_path} ({len(rows)} rows)")
    return rows


def save_group_csv(group_curves, bin_size, out_path):
    """Save per-group P10/P50/P90 curves to CSV."""
    rows = []
    for group_key, gc in group_curves.items():
        for b, data in sorted(gc["rotary"].items()):
            rows.append({
                "equiv_bha_key": group_key,
                "num_runs": gc["num_runs"],
                "curve_type": "rotary",
                "bin_start_ft": b,
                "bin_axis": "distance_from_run_start",
                "p10": data["p10"],
                "p50": data["p50"],
                "p90": data["p90"],
                "contributing_runs": data["num_runs"],
                "confident": data["confident"],
            })
        for b, data in sorted(gc["slide"].items()):
            rows.append({
                "equiv_bha_key": group_key,
                "num_runs": gc["num_runs"],
                "curve_type": "slide",
                "bin_start_ft": b,
                "bin_axis": "distance_from_lateral_start",
                "p10": data["p10"],
                "p50": data["p50"],
                "p90": data["p90"],
                "contributing_runs": data["num_runs"],
                "confident": data["confident"],
            })

    if rows:
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"  Group curves:   {out_path} ({len(rows)} rows)")
    return rows


def save_ttd_csv(ttd_results, out_path):
    """Save TTD ranking to CSV (excludes nested buckets)."""
    if ttd_results:
        flat = []
        for r in ttd_results:
            row = {}
            for k, v in r.items():
                if k == "buckets":
                    continue
                if isinstance(v, (dict, list)):
                    row[k] = json.dumps(v, separators=(",", ":"))
                else:
                    row[k] = v
            flat.append(row)
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(flat[0].keys()))
            writer.writeheader()
            writer.writerows(flat)
        print(f"  TTD ranking:    {out_path}")


def save_ttd_breakdown_csv(ttd_results, out_path):
    """Save per-bucket TTD breakdown to CSV."""
    rows = []
    for r in ttd_results:
        for b in r.get("buckets", []):
            rows.append({
                "group_key": r["group_key"],
                "bucket_label": b["label"],
                "bucket_length_ft": b["length_ft"],
                "rotary_rop_p50": b["rotary_rop"],
                "rotary_time_hrs": b["rotary_time"],
                "slide_rop_p50": b["slide_rop"],
                "slide_time_hrs": b["slide_time"],
                "total_time_hrs": b["total_time"],
            })
    if rows:
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"  TTD breakdown:  {out_path} ({len(rows)} buckets)")


def main():
    # Parse args
    csv_path = None
    mode = "lateral"
    rotary_bin = DEFAULT_ROTARY_BIN
    slide_bin = DEFAULT_SLIDE_BIN
    target_length = 10000
    slide_pct = None  # auto-detect from data
    output_dir = None
    max_missing_formations = 1  # exclude groups missing > 1 formation
    export_csv = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--mode" and i + 1 < len(args):
            mode = args[i + 1].lower()
            i += 2
        elif args[i] == "--rotary-bin" and i + 1 < len(args):
            rotary_bin = int(args[i + 1])
            i += 2
        elif args[i] == "--slide-bin" and i + 1 < len(args):
            slide_bin = int(args[i + 1])
            i += 2
        elif args[i] == "--bin-size" and i + 1 < len(args):
            rotary_bin = int(args[i + 1])
            slide_bin = int(args[i + 1])
            i += 2
        elif args[i] in ("--lateral-length", "--section-length") and i + 1 < len(args):
            target_length = int(float(args[i + 1]))
            i += 2
        elif args[i] == "--slide-pct" and i + 1 < len(args):
            slide_pct = float(args[i + 1])
            i += 2
        elif args[i] == "--output-dir" and i + 1 < len(args):
            output_dir = args[i + 1]
            i += 2
        elif args[i] == "--max-missing-formations" and i + 1 < len(args):
            max_missing_formations = int(args[i + 1])
            i += 2
        elif args[i] == "--export-csv":
            export_csv = True
            i += 1
        elif not args[i].startswith("--"):
            csv_path = args[i]
            if not os.path.isabs(csv_path):
                csv_path = os.path.join(SCRIPT_DIR, csv_path)
            i += 1
        else:
            i += 1

    if output_dir is None:
        output_dir = SCRIPT_DIR
    elif not os.path.isabs(output_dir):
        output_dir = os.path.join(SCRIPT_DIR, output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Default input file depends on mode
    if csv_path is None:
        if mode == "vertical":
            csv_path = os.path.join(SCRIPT_DIR, "rop_1ft_data_vertical.csv")
        else:
            csv_path = os.path.join(SCRIPT_DIR, "rop_1ft_data.csv")

    if not os.path.exists(csv_path):
        print(f"ERROR: {csv_path} not found")
        sys.exit(1)

    if mode == "vertical":
        main_vertical(csv_path, target_length, slide_pct, output_dir,
                      max_missing_formations, export_csv)
    else:
        main_lateral(csv_path, rotary_bin, slide_bin, target_length, slide_pct,
                     output_dir, export_csv)


def main_lateral(csv_path, rotary_bin, slide_bin, target_lateral, slide_pct, output_dir=None,
                 export_csv=False):
    """Run the lateral (distance-based) curve building pipeline."""
    print(f"\n{'=' * 80}")
    print(f"  BUILD ROP TYPE CURVES (LATERAL MODE)")
    print(f"  Input: {os.path.basename(csv_path)}")
    print(f"  Rotary bin: {rotary_bin} ft | Slide bin: {slide_bin} ft")
    print(f"  Smoothing: rolling median, window={ROLLING_WINDOW} bins")
    print(f"{'=' * 80}\n")

    rows = load_1ft_data(csv_path)
    print(f"  Loaded {len(rows):,} 1ft records")

    if slide_pct is None:
        slide_count = sum(1 for r in rows if r["state"] == "Slide Drilling")
        total_count = len(rows)
        slide_pct = slide_count / total_count if total_count > 0 else 0.12
        print(f"  Auto-detected slide %: {slide_pct:.1%}")
    else:
        print(f"  User-specified slide %: {slide_pct:.1%}")

    print(f"  Target lateral length: {target_lateral:,} ft")

    print(f"\n  Building per-run curves (rotary={rotary_bin}ft, slide={slide_bin}ft)...")
    per_run = build_per_run_curves(rows, rotary_bin, slide_bin)
    print(f"  {len(per_run)} runs processed")

    print(f"\n  Building group P10/P50/P90 curves (smoothed, window={ROLLING_WINDOW})...")
    group_curves = build_group_curves(per_run, rotary_bin, slide_bin)
    print(f"  {len(group_curves)} groups")

    print(f"\n  {'Group':<30} {'Runs':<6} {'Wells':<7} {'Agit.':<6} "
          f"{'Rot Bins':<10} {'Sli Bins':<10} {'Sli(raw)':<10}")
    print(f"  {'-' * 85}")
    for gk in sorted(group_curves.keys(), key=lambda k: -group_curves[k]["num_runs"]):
        gc = group_curves[gk]
        rot_bins = len(gc["rotary"])
        sli_bins = len(gc["slide"])
        sli_raw = len(gc.get("slide_raw", {}))
        print(f"  {gk:<30} {gc['num_runs']:<6} {gc['num_wells']:<7} "
              f"{gc['num_with_agitator']:<6} {rot_bins:<10} {sli_bins:<10} {sli_raw:<10}")

    print(f"\n  Calculating Time to TD...")
    ttd_results = calculate_ttd(group_curves, target_lateral, slide_pct, rotary_bin, slide_bin)

    print(f"\n  {'#':<4} {'Group':<30} {'Runs':<6} {'TTD (hrs)':<10} {'TTD (days)':<10} "
          f"{'Bins OK':<8} {'Missing':<8}")
    print(f"  {'-' * 80}")
    for idx, t in enumerate(ttd_results, 1):
        print(f"  {idx:<4} {t['group_key']:<30} {t['num_runs']:<6} "
              f"{t['ttd_hours']:<10} {t['ttd_days']:<10} "
              f"{t['bins_with_data']:<8} {t['bins_missing']:<8}")

    out = output_dir or SCRIPT_DIR
    section_name = os.path.basename(out)
    latest = db.get_latest_run()
    rid = latest["id"] if latest else None
    print(f"\n  Saving outputs (run_id={rid})...")
    per_run_rows = save_per_run_csv(per_run, rotary_bin, os.path.join(out, "rop_curves_per_run.csv"))
    if per_run_rows:
        df = pd.DataFrame(per_run_rows)
        db.save_rop_curves_per_run(section_name, df, "lateral", run_id=rid)
        if export_csv:
            db.export_csv(df, "rop_curves_per_run")
    group_rows = save_group_csv(group_curves, rotary_bin, os.path.join(out, "rop_curves_by_group.csv"))
    if group_rows:
        df = pd.DataFrame(group_rows)
        db.save_rop_curves_by_group(section_name, df, "lateral", run_id=rid)
        if export_csv:
            db.export_csv(df, "rop_curves_by_group")
    save_ttd_csv(ttd_results, os.path.join(out, "ttd_ranking.csv"))
    save_ttd_breakdown_csv(ttd_results, os.path.join(out, "ttd_breakdown.csv"))
    if latest and ttd_results:
        db.save_ttd_rankings(latest["id"], section_name, ttd_results)
    if export_csv and ttd_results:
        db.export_csv(ttd_results, "ttd_ranking")
    print(f"\n  Done!")


def main_vertical(csv_path, section_length, slide_pct, output_dir=None,
                  max_missing_formations=1, export_csv=False):
    """Run the vertical (formation-based) curve building pipeline."""
    print(f"\n{'=' * 80}")
    print(f"  BUILD ROP TYPE CURVES (VERTICAL / FORMATION MODE)")
    print(f"  Input: {os.path.basename(csv_path)}")
    print(f"  Formation segment: {FORMATION_SEGMENT_PCT}% per bin")
    print(f"  Smoothing: rolling median, window={ROLLING_WINDOW_VERT} segments")
    print(f"{'=' * 80}\n")

    rows = load_1ft_data_vertical(csv_path)
    print(f"  Loaded {len(rows):,} 1ft records (with formation mapping)")

    if not rows:
        print("  ERROR: No valid rows with formation data.")
        return

    if slide_pct is None:
        slide_count = sum(1 for r in rows if r["state"] == "Slide Drilling")
        total_count = len(rows)
        slide_pct = slide_count / total_count if total_count > 0 else 0.20
        print(f"  Auto-detected slide %: {slide_pct:.1%}")
    else:
        print(f"  User-specified slide %: {slide_pct:.1%}")

    print(f"  Target section length: {section_length:,} ft")

    # Build formation roadmap
    roadmap, fm_order = build_formation_roadmap(rows)
    print(f"\n  Formation roadmap: {len(fm_order)} formations, {len(roadmap)} segments")
    for fm in fm_order:
        fm_feet = sum(1 for r in rows if r.get("formation_name") == fm)
        print(f"    {fm:<30} {fm_feet:>7,} feet")

    # Phase 1: Per-run curves
    print(f"\n  Building per-run formation curves...")
    per_run = build_per_run_curves_vertical(rows)
    print(f"  {len(per_run)} runs processed")

    # Phase 2: Group curves
    print(f"\n  Building group P10/P50/P90 formation curves "
          f"(smoothed, window={ROLLING_WINDOW_VERT})...")
    group_curves = build_group_curves_vertical(per_run, roadmap)
    print(f"  {len(group_curves)} groups")

    print(f"\n  {'Group':<30} {'Runs':<6} {'Wells':<7} {'Agit.':<6} "
          f"{'Rot Segs':<10} {'Sli Segs':<10}")
    print(f"  {'-' * 75}")
    for gk in sorted(group_curves.keys(), key=lambda k: -group_curves[k]["num_runs"]):
        gc = group_curves[gk]
        rot_segs = len(gc["rotary"])
        sli_segs = len(gc["slide"])
        print(f"  {gk:<30} {gc['num_runs']:<6} {gc['num_wells']:<7} "
              f"{gc['num_with_agitator']:<6} {rot_segs:<10} {sli_segs:<10}")

    # Phase 2b: Filter groups by formation coverage
    print(f"\n  Filtering groups (max {max_missing_formations} missing "
          f"formation(s) allowed)...")
    group_curves, excluded = filter_groups_by_formation_coverage(
        group_curves, roadmap, fm_order, max_missing=max_missing_formations)

    # If the configured threshold excludes every group, relax by one
    # formation as a fallback so vertical sections with sparse coverage
    # can still produce at least one comparable candidate.
    if not group_curves and max_missing_formations < max(len(fm_order) - 1, 1):
        relaxed_missing = max_missing_formations + 1
        print(f"  No groups passed; retrying with max_missing={relaxed_missing}...")
        group_curves, excluded = filter_groups_by_formation_coverage(
            group_curves=build_group_curves_vertical(per_run, roadmap),
            roadmap=roadmap,
            fm_order=fm_order,
            max_missing=relaxed_missing,
        )

    if excluded:
        print(f"  EXCLUDED {len(excluded)} group(s):")
        for gk, missing_fms in excluded:
            print(f"    {gk} -- missing {len(missing_fms)} of "
                  f"{len(fm_order)} formations "
                  f"({', '.join(missing_fms)})")
    else:
        print(f"  All {len(group_curves)} groups passed.")
    print(f"  {len(group_curves)} groups remaining for TTD + charts")

    # Phase 3: TTD ranking
    print(f"\n  Calculating Time to TD (vertical)...")
    ttd_results = calculate_ttd_vertical(
        group_curves, roadmap, fm_order, section_length, slide_pct
    )

    print(f"\n  {'#':<4} {'Group':<30} {'Runs':<6} {'TTD (hrs)':<10} {'TTD (days)':<10} "
          f"{'Segs OK':<9} {'Missing':<8}")
    print(f"  {'-' * 80}")
    for idx, t in enumerate(ttd_results, 1):
        print(f"  {idx:<4} {t['group_key']:<30} {t['num_runs']:<6} "
              f"{t['ttd_hours']:<10} {t['ttd_days']:<10} "
              f"{t['segments_with_data']:<9} {t['segments_missing']:<8}")

    out = output_dir or SCRIPT_DIR
    section_name = os.path.basename(out)
    latest = db.get_latest_run()
    rid = latest["id"] if latest else None
    # Save outputs
    print(f"\n  Saving outputs (run_id={rid})...")
    per_run_rows = save_per_run_csv_vertical(per_run, os.path.join(out, "rop_curves_per_run_vertical.csv"))
    if per_run_rows:
        df = pd.DataFrame(per_run_rows)
        db.save_rop_curves_per_run(section_name, df, "vertical", run_id=rid)
        if export_csv:
            db.export_csv(df, "rop_curves_per_run_vertical")
    group_rows = save_group_csv_vertical(group_curves, os.path.join(out, "rop_curves_by_group_vertical.csv"))
    if group_rows:
        df = pd.DataFrame(group_rows)
        db.save_rop_curves_by_group(section_name, df, "vertical", run_id=rid)
        if export_csv:
            db.export_csv(df, "rop_curves_by_group_vertical")
    save_ttd_csv(ttd_results, os.path.join(out, "ttd_ranking_vertical.csv"))
    save_ttd_breakdown_csv(ttd_results, os.path.join(out, "ttd_breakdown_vertical.csv"))
    if latest and ttd_results:
        db.save_ttd_rankings(latest["id"], section_name, ttd_results)
    if export_csv and ttd_results:
        db.export_csv(ttd_results, "ttd_ranking_vertical")

    # Also save the roadmap for the chart script
    roadmap_path = os.path.join(out, "formation_roadmap.csv")
    with open(roadmap_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["formation_bin_key", "formation_name", "formation_segment", "order"])
        for idx, key in enumerate(roadmap):
            fm_name, seg = parse_formation_bin_key(key)
            writer.writerow([key, fm_name, seg, idx])
    print(f"  Roadmap:        {roadmap_path} ({len(roadmap)} segments)")

    print(f"\n  Done!")


if __name__ == "__main__":
    main()
