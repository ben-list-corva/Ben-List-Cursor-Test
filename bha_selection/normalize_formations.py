"""Normalize formation names using target-well-reference or TVD-only clustering.

Reads formation_tops.csv, consolidates sub-formations into canonical groups,
and outputs formation_tops_canonical.csv (same schema — zero downstream changes)
plus canonical_map.json for future FE display/overrides.

Modes
-----
target-reference (default):
    Use a target well's formations as the canonical reference.  Sub-formations
    are auto-consolidated by name hierarchy + TVD proximity.  Offset wells are
    mapped to canonical formations by TVD range.

tvd-only:
    Cluster all formation tops by TVD proximity (ignoring names).  Clusters are
    named by the most common formation name in each cluster.

Usage
-----
    python normalize_formations.py --target-asset 82512872
    python normalize_formations.py --mode tvd-only --tvd-gap 200
    python normalize_formations.py --target-asset 82512872 --overrides overrides.json
"""

import argparse
import csv
import json
import os
import re
import time
from collections import Counter, defaultdict
from statistics import median

import db

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Name‐hierarchy helpers ──────────────────────────────────────────────────

STRIP_PREFIXES = ("Upper ", "Lower ", "Base ", "Middle ")

STRIP_SUFFIXES_RE = re.compile(
    r'[\s_]+'
    r'(?:'
    r'[A-Ea-e]\s*Bench'        # letter bench  (B Bench, C Bench …)
    r'|Bench'                   # generic bench
    r'|Sand(?:stone)?'          # Sand / Sandstone
    r'|Shale'
    r'|Carbonate'
    r'|Limestone'
    r'|Lime'
    r'|Dolomite'
    r'|Lower'                   # trailing Lower (e.g. "Austin Chalk Lower")
    r'|Upper'                   # trailing Upper
    r'|Base'                    # trailing Base
    r'|Middle'
    r'|\d+[a-z]?'              # ordinals  (2a, 3, 6a, 4a)
    r'|[A-E]'                  # single‐letter suffix
    r')$',
    re.IGNORECASE,
)

QUALIFIER_WORDS = frozenset({
    "bench", "sand", "sandstone", "shale", "carbonate", "limestone",
    "lime", "dolomite", "base", "upper", "lower", "middle", "top",
    "bottom",
})


def extract_root(name: str) -> str:
    """Derive the root formation name by stripping prefixes, suffixes, and
    normalizing underscores.  E.g.  "Upper Eagle Ford_6a"  →  "Eagle Ford".
    """
    root = name.strip()

    # Strip one leading prefix
    for pfx in STRIP_PREFIXES:
        if root.startswith(pfx):
            root = root[len(pfx):]
            break

    # Normalize underscores → spaces
    root = root.replace("_", " ").strip()

    # Iteratively strip trailing suffixes (up to 3 passes)
    for _ in range(3):
        new = STRIP_SUFFIXES_RE.sub("", root).strip()
        if new == root or not new:
            break
        root = new

    return root if root else name.strip()


def is_orphan_name(name: str) -> bool:
    """Return True if *name* looks like a sub‐unit qualifier rather than a
    standalone formation name.  E.g. "B Bench" → True, "Buda" → False.
    """
    words = name.lower().split()
    if not words:
        return False
    # Every word is either a single letter or a known qualifier
    return all(
        w in QUALIFIER_WORDS or (len(w) == 1 and w.isalpha())
        for w in words
    )


# ── Data loading ─────────────────────────────────────────────────────────────

def load_formation_tops(csv_path: str) -> list[dict]:
    """Load raw formation_tops.csv into a list of dicts."""
    rows = []
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                rows.append({
                    "asset_id": row["asset_id"].strip(),
                    "well_name": row.get("well_name", "").strip(),
                    "formation_name": row.get("formation_name", "").strip(),
                    "md_top": float(row["md_top"]),
                    "tvd_top": float(row["tvd_top"]),
                    "md_thickness": (float(row["md_thickness"])
                                     if row.get("md_thickness") else None),
                    "tvd_thickness": (float(row["tvd_thickness"])
                                      if row.get("tvd_thickness") else None),
                    "lithology": row.get("lithology", ""),
                })
            except (ValueError, KeyError):
                continue
    return rows


def tops_by_well(rows: list[dict]) -> dict[str, list[dict]]:
    """Group rows by asset_id, sorted by tvd_top within each well."""
    by_well: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_well[r["asset_id"]].append(r)
    for aid in by_well:
        by_well[aid].sort(key=lambda x: x["tvd_top"])
    return dict(by_well)


# ── Target‐reference mode ───────────────────────────────────────────────────

def build_canonical_from_target(target_tops: list[dict]) -> list[dict]:
    """Build canonical formation groups from a target well's formation list.

    Returns a list of canonical entries sorted by TVD::

        [{"canonical_name": "Eagle Ford",
          "tvd_top": 9409.0,
          "tvd_bottom": 9647.0,
          "sub_formations": ["Upper Eagle Ford", …]}, …]
    """
    if not target_tops:
        return []

    # --- Step 1: extract root for each formation ----
    formations = sorted(target_tops, key=lambda t: t["tvd_top"])
    roots = [(f, extract_root(f["formation_name"])) for f in formations]

    # --- Step 2: group by root ----
    root_groups: dict[str, list[dict]] = defaultdict(list)
    for f, root in roots:
        root_groups[root].append(f)

    # --- Step 3: resolve orphans ----
    # Walk formations in TVD order; any orphan gets merged into the most
    # recent non‐orphan group above it.
    assigned: dict[str, str] = {}  # formation_name → canonical_name
    current_parent: str | None = None

    for f, root in roots:
        # Is this root group a singleton whose name looks like a sub‐unit?
        is_orphan = (
            len(root_groups[root]) == 1
            and is_orphan_name(f["formation_name"])
        )
        if is_orphan and current_parent is not None:
            assigned[f["formation_name"]] = current_parent
        else:
            # Use this root as a canonical name
            assigned[f["formation_name"]] = root
            current_parent = root

    # --- Step 4: build canonical entries ----
    canon_dict: dict[str, dict] = {}
    for f in formations:
        cname = assigned[f["formation_name"]]
        if cname not in canon_dict:
            canon_dict[cname] = {
                "canonical_name": cname,
                "tvd_top": f["tvd_top"],
                "tvd_bottom": f["tvd_top"],
                "sub_formations": [],
            }
        entry = canon_dict[cname]
        entry["tvd_top"] = min(entry["tvd_top"], f["tvd_top"])
        entry["tvd_bottom"] = max(entry["tvd_bottom"], f["tvd_top"])
        entry["sub_formations"].append(f["formation_name"])

    # Set tvd_bottom of each canonical to the tvd_top of the next canonical
    canonicals = sorted(canon_dict.values(), key=lambda c: c["tvd_top"])
    for i, c in enumerate(canonicals):
        if i + 1 < len(canonicals):
            c["tvd_bottom"] = canonicals[i + 1]["tvd_top"]
        else:
            # Last formation: extend by tvd_thickness of deepest sub‐formation
            deepest = max(
                (f for f in formations
                 if assigned[f["formation_name"]] == c["canonical_name"]),
                key=lambda x: x["tvd_top"],
            )
            if deepest.get("tvd_thickness") and deepest["tvd_thickness"] > 0:
                c["tvd_bottom"] = deepest["tvd_top"] + deepest["tvd_thickness"]
            else:
                c["tvd_bottom"] = c["tvd_top"] + 500  # fallback

    return canonicals


def map_offset_to_canonical(
    offset_tops: list[dict],
    canonicals: list[dict],
) -> dict[str, str]:
    """Map an offset well's formation names to canonical names by TVD.

    Returns {original_formation_name: canonical_name}.
    """
    mapping: dict[str, str] = {}
    if not canonicals:
        return mapping

    for f in offset_tops:
        tvd = f["tvd_top"]
        best = None
        best_dist = float("inf")

        for c in canonicals:
            if c["tvd_top"] <= tvd < c["tvd_bottom"]:
                best = c["canonical_name"]
                break
            # Track nearest in case nothing contains this TVD
            dist = min(abs(tvd - c["tvd_top"]), abs(tvd - c["tvd_bottom"]))
            if dist < best_dist:
                best_dist = dist
                best = c["canonical_name"]

        if best is not None:
            mapping[f["formation_name"]] = best

    return mapping


def consolidate_well(
    well_tops: list[dict],
    name_mapping: dict[str, str],
) -> list[dict]:
    """Merge a single well's formation tops according to a name mapping.

    Multiple original formations that map to the same canonical name are
    collapsed into one row using ``min(md_top)``, ``min(tvd_top)``, and
    recomputed thicknesses.
    """
    groups: dict[str, list[dict]] = defaultdict(list)
    for f in well_tops:
        cname = name_mapping.get(f["formation_name"])
        if cname is None:
            continue
        groups[cname].append(f)

    consolidated: list[dict] = []
    for cname, members in groups.items():
        members.sort(key=lambda x: x["tvd_top"])
        consolidated.append({
            "asset_id": members[0]["asset_id"],
            "well_name": members[0]["well_name"],
            "formation_name": cname,
            "md_top": min(m["md_top"] for m in members),
            "tvd_top": min(m["tvd_top"] for m in members),
            # thickness will be recomputed below
            "md_thickness": None,
            "tvd_thickness": None,
            "lithology": members[0].get("lithology", ""),
        })

    # Sort by tvd_top and recompute thicknesses
    consolidated.sort(key=lambda x: x["tvd_top"])
    for i, entry in enumerate(consolidated):
        if i + 1 < len(consolidated):
            entry["md_thickness"] = round(
                consolidated[i + 1]["md_top"] - entry["md_top"], 1)
            entry["tvd_thickness"] = round(
                consolidated[i + 1]["tvd_top"] - entry["tvd_top"], 1)
        else:
            # Last formation: estimate from original data
            orig = groups[entry["formation_name"]]
            deepest = max(orig, key=lambda x: x["tvd_top"])
            if deepest.get("tvd_thickness") and deepest["tvd_thickness"]:
                extent = (deepest["tvd_top"] + deepest["tvd_thickness"]
                          - entry["tvd_top"])
                entry["tvd_thickness"] = round(extent, 1)
                md_extent = (deepest["md_top"]
                             + (deepest["md_thickness"] or 0)
                             - entry["md_top"])
                entry["md_thickness"] = round(md_extent, 1) if md_extent > 0 else None
            # else leave None

    return consolidated


def run_target_reference(
    all_tops: list[dict],
    target_asset_id: str,
    overrides: dict | None = None,
) -> tuple[list[dict], dict]:
    """Run the target‐well‐reference normalization.

    Returns (consolidated_rows, canonical_map_dict).
    """
    by_well = tops_by_well(all_tops)

    if target_asset_id not in by_well:
        raise ValueError(
            f"Target asset {target_asset_id} not found in formation_tops.csv. "
            f"Available: {', '.join(sorted(by_well.keys())[:10])}…"
        )

    target_tops = by_well[target_asset_id]
    target_name = target_tops[0]["well_name"] if target_tops else ""

    # Build canonical formations from target well
    canonicals = build_canonical_from_target(target_tops)

    # Apply user overrides (merge/rename rules)
    if overrides:
        canonicals = apply_overrides(canonicals, overrides, target_tops)

    print(f"\n  Canonical formations ({len(canonicals)}):")
    for i, c in enumerate(canonicals):
        subs = ", ".join(c["sub_formations"])
        print(f"    {i+1:>2}. {c['canonical_name']:<25} "
              f"TVD {c['tvd_top']:.0f}-{c['tvd_bottom']:.0f}  "
              f"[{subs}]")

    # Map and consolidate every well
    all_consolidated: list[dict] = []
    well_mappings: dict[str, dict[str, list[str]]] = {}
    wells_excluded: list[dict] = []

    for aid, wtops in by_well.items():
        if not wtops:
            wells_excluded.append({
                "asset_id": aid,
                "name": "",
                "reason": "No formation data",
            })
            continue

        mapping = map_offset_to_canonical(wtops, canonicals)
        if not mapping:
            wells_excluded.append({
                "asset_id": aid,
                "name": wtops[0]["well_name"] if wtops else "",
                "reason": "No formations mapped to canonical ranges",
            })
            continue

        consolidated = consolidate_well(wtops, mapping)
        all_consolidated.extend(consolidated)

        # Record per-well mapping for JSON output
        by_canon: dict[str, list[str]] = defaultdict(list)
        for orig, canon in mapping.items():
            by_canon[canon].append(orig)
        well_mappings[aid] = dict(by_canon)

    # Build canonical_map dict for JSON output
    canonical_map = {
        "mode": "target-reference",
        "target_well": {
            "asset_id": target_asset_id,
            "name": target_name,
        },
        "canonical_formations": [
            {
                "canonical_name": c["canonical_name"],
                "order": i,
                "target_tvd_top": c["tvd_top"],
                "target_tvd_bottom": c["tvd_bottom"],
                "target_sub_formations": c["sub_formations"],
            }
            for i, c in enumerate(canonicals)
        ],
        "well_mappings": well_mappings,
        "wells_excluded": wells_excluded,
    }

    return all_consolidated, canonical_map


# ── TVD‐only mode ───────────────────────────────────────────────────────────

def cluster_by_tvd(
    all_tops: list[dict],
    gap_threshold: float = 200.0,
) -> tuple[list[dict], dict]:
    """Cluster formation tops by TVD proximity, ignoring names.

    Starts a new cluster whenever the gap between consecutive tops (across
    all wells) exceeds *gap_threshold* feet.

    Returns (consolidated_rows, canonical_map_dict).
    """
    # Collect every (tvd_top, formation_name) across all wells
    all_tvd_name = []
    for r in all_tops:
        all_tvd_name.append((r["tvd_top"], r["formation_name"]))

    if not all_tvd_name:
        return [], {"mode": "tvd-only", "canonical_formations": [],
                    "well_mappings": {}, "wells_excluded": []}

    # Sort by TVD, find gaps → clusters
    all_tvd_name.sort(key=lambda x: x[0])
    clusters: list[list[tuple[float, str]]] = [[all_tvd_name[0]]]
    for tvd, name in all_tvd_name[1:]:
        if tvd - clusters[-1][-1][0] > gap_threshold:
            clusters.append([])
        clusters[-1].append((tvd, name))

    # Name each cluster by the most common formation name within it
    cluster_defs: list[dict] = []
    for i, members in enumerate(clusters):
        name_counts = Counter(n for _, n in members)
        best_name = name_counts.most_common(1)[0][0]
        tvds = [t for t, _ in members]
        cluster_defs.append({
            "canonical_name": best_name,
            "tvd_top": min(tvds),
            "tvd_bottom": max(tvds),
            "member_names": sorted(set(n for _, n in members)),
        })

    # Adjust tvd_bottom to next cluster's tvd_top
    for i, cd in enumerate(cluster_defs):
        if i + 1 < len(cluster_defs):
            cd["tvd_bottom"] = cluster_defs[i + 1]["tvd_top"]
        else:
            cd["tvd_bottom"] = cd["tvd_bottom"] + 500  # fallback

    print(f"\n  TVD clusters ({len(cluster_defs)}):")
    for i, cd in enumerate(cluster_defs):
        names = ", ".join(cd["member_names"][:5])
        if len(cd["member_names"]) > 5:
            names += f"… (+{len(cd['member_names'])-5})"
        print(f"    {i+1:>2}. {cd['canonical_name']:<25} "
              f"TVD {cd['tvd_top']:.0f}-{cd['tvd_bottom']:.0f}  "
              f"[{names}]")

    # Build name mapping per well and consolidate
    by_well = tops_by_well(all_tops)
    all_consolidated: list[dict] = []
    well_mappings: dict[str, dict[str, list[str]]] = {}
    wells_excluded: list[dict] = []

    for aid, wtops in by_well.items():
        if not wtops:
            wells_excluded.append({
                "asset_id": aid, "name": "", "reason": "No formation data"})
            continue

        mapping = map_offset_to_canonical(wtops, cluster_defs)
        if not mapping:
            wells_excluded.append({
                "asset_id": aid,
                "name": wtops[0]["well_name"] if wtops else "",
                "reason": "No formations mapped to clusters",
            })
            continue

        consolidated = consolidate_well(wtops, mapping)
        all_consolidated.extend(consolidated)

        by_canon: dict[str, list[str]] = defaultdict(list)
        for orig, canon in mapping.items():
            by_canon[canon].append(orig)
        well_mappings[aid] = dict(by_canon)

    canonical_map = {
        "mode": "tvd-only",
        "tvd_gap_threshold": gap_threshold,
        "canonical_formations": [
            {
                "canonical_name": cd["canonical_name"],
                "order": i,
                "target_tvd_top": cd["tvd_top"],
                "target_tvd_bottom": cd["tvd_bottom"],
                "member_names": cd["member_names"],
            }
            for i, cd in enumerate(cluster_defs)
        ],
        "well_mappings": well_mappings,
        "wells_excluded": wells_excluded,
    }

    return all_consolidated, canonical_map


# ── Overrides ────────────────────────────────────────────────────────────────

def load_overrides(json_path: str) -> dict:
    """Load user override rules from a JSON file.

    Expected format::

        {
          "formations": {
            "Carrizo": ["Carrizo", "Corrizo", "Carrizo Base", "Cenizo"],
            "Eagle Ford": ["Upper Eagle Ford", "Lower Eagle Ford", "Eagle Ford"]
          }
        }

    If ``formations`` is provided, the auto‐detected canonical groups are
    replaced by these explicit groupings.
    """
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def apply_overrides(
    canonicals: list[dict],
    overrides: dict,
    target_tops: list[dict],
) -> list[dict]:
    """Apply user overrides to the canonical formation list.

    If overrides contain a ``formations`` key with explicit groupings, rebuild
    the canonical list accordingly.  Otherwise return canonicals unchanged.
    """
    fm_groups = overrides.get("formations")
    if not fm_groups:
        return canonicals

    # Build a lookup: formation_name → tvd_top from the target well
    tvd_lookup = {f["formation_name"]: f["tvd_top"] for f in target_tops}

    new_canonicals: list[dict] = []
    for canon_name, sub_names in fm_groups.items():
        tvds = [tvd_lookup[s] for s in sub_names if s in tvd_lookup]
        if not tvds:
            continue
        new_canonicals.append({
            "canonical_name": canon_name,
            "tvd_top": min(tvds),
            "tvd_bottom": max(tvds),
            "sub_formations": [s for s in sub_names if s in tvd_lookup],
        })

    # Sort by tvd_top, fix tvd_bottom
    new_canonicals.sort(key=lambda c: c["tvd_top"])
    for i, c in enumerate(new_canonicals):
        if i + 1 < len(new_canonicals):
            c["tvd_bottom"] = new_canonicals[i + 1]["tvd_top"]
        else:
            c["tvd_bottom"] = c["tvd_top"] + 500

    # Anything from the target well NOT covered by overrides → keep from auto
    covered_tvd = set()
    for c in new_canonicals:
        for s in c["sub_formations"]:
            covered_tvd.add(tvd_lookup.get(s))

    for c in canonicals:
        if c["tvd_top"] not in covered_tvd:
            already = any(nc["canonical_name"] == c["canonical_name"]
                          for nc in new_canonicals)
            if not already:
                new_canonicals.append(c)

    new_canonicals.sort(key=lambda c: c["tvd_top"])

    # Re-fix tvd_bottom chain
    for i, c in enumerate(new_canonicals):
        if i + 1 < len(new_canonicals):
            c["tvd_bottom"] = new_canonicals[i + 1]["tvd_top"]

    return new_canonicals


# ── Output ───────────────────────────────────────────────────────────────────

def save_canonical_csv(rows: list[dict], out_path: str) -> None:
    """Save consolidated formation tops to CSV (same schema as input)."""
    fieldnames = [
        "asset_id", "well_name", "formation_name", "md_top", "tvd_top",
        "md_thickness", "tvd_thickness", "lithology",
    ]
    try:
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for r in rows:
                writer.writerow({
                    "asset_id": r["asset_id"],
                    "well_name": r["well_name"],
                    "formation_name": r["formation_name"],
                    "md_top": r["md_top"],
                    "tvd_top": r["tvd_top"],
                    "md_thickness": r["md_thickness"] if r["md_thickness"] is not None else "",
                    "tvd_thickness": r["tvd_thickness"] if r["tvd_thickness"] is not None else "",
                    "lithology": r.get("lithology", ""),
                })
        print(f"\n  Saved CSV: {out_path}")
    except PermissionError:
        backup = out_path.replace(".csv", f"_{int(time.time())}.csv")
        with open(backup, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for r in rows:
                writer.writerow({
                    "asset_id": r["asset_id"],
                    "well_name": r["well_name"],
                    "formation_name": r["formation_name"],
                    "md_top": r["md_top"],
                    "tvd_top": r["tvd_top"],
                    "md_thickness": r["md_thickness"] if r["md_thickness"] is not None else "",
                    "tvd_thickness": r["tvd_thickness"] if r["tvd_thickness"] is not None else "",
                    "lithology": r.get("lithology", ""),
                })
        print(f"\n  WARNING: File locked. Saved to: {backup}")


def save_canonical_map(cmap: dict, out_path: str) -> None:
    """Save the canonical map as formatted JSON."""
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(cmap, f, indent=2, ensure_ascii=False)
        print(f"  Saved JSON: {out_path}")
    except PermissionError:
        backup = out_path.replace(".json", f"_{int(time.time())}.json")
        with open(backup, "w", encoding="utf-8") as f:
            json.dump(cmap, f, indent=2, ensure_ascii=False)
        print(f"  WARNING: File locked. Saved to: {backup}")


# ── Reporting ────────────────────────────────────────────────────────────────

def print_summary(
    all_tops: list[dict],
    consolidated: list[dict],
    canonical_map: dict,
) -> None:
    """Print a human‐readable summary of the normalization results."""
    by_well_orig = tops_by_well(all_tops)
    by_well_new = tops_by_well(consolidated)

    orig_names = set(r["formation_name"] for r in all_tops)
    new_names = set(r["formation_name"] for r in consolidated)

    n_wells_orig = len(by_well_orig)
    n_wells_new = len(by_well_new)
    n_excluded = len(canonical_map.get("wells_excluded", []))

    print(f"\n  {'=' * 60}")
    print(f"  NORMALIZATION SUMMARY")
    print(f"  {'=' * 60}")
    print(f"  Original formation names:  {len(orig_names):>4}")
    print(f"  Canonical formation names: {len(new_names):>4}")
    print(f"  Reduction:                 {len(orig_names) - len(new_names):>4} fewer names")
    print(f"  Original bins (x10 segs):  {len(orig_names) * 10:>4}")
    print(f"  Canonical bins (x10 segs): {len(new_names) * 10:>4}")
    print(f"  Wells with data:           {n_wells_new:>4}")
    print(f"  Wells excluded:            {n_excluded:>4}")
    print(f"  Consolidated rows:         {len(consolidated):>4}")

    # Per-canonical formation: how many wells have it?
    fm_well_counts: dict[str, int] = Counter()
    for r in consolidated:
        fm_well_counts[r["formation_name"]] += 1

    canon_order = {
        c["canonical_name"]: c["order"]
        for c in canonical_map.get("canonical_formations", [])
    }
    print(f"\n  Per-canonical formation well counts:")
    for fm in sorted(fm_well_counts, key=lambda x: canon_order.get(x, 999)):
        print(f"    {fm:<30} {fm_well_counts[fm]:>3} wells")

    if canonical_map.get("wells_excluded"):
        print(f"\n  Excluded wells:")
        for w in canonical_map["wells_excluded"]:
            print(f"    {w.get('name', w['asset_id']):<40} {w['reason']}")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Normalize formation names for vertical ROP curves.")
    parser.add_argument(
        "--mode", choices=["target-reference", "tvd-only"],
        default="target-reference",
        help="Normalization mode (default: target-reference)")
    parser.add_argument(
        "--target-asset", type=str, default=None,
        help="Asset ID of the target/reference well (required for target-reference mode)")
    parser.add_argument(
        "--tvd-gap", type=float, default=200.0,
        help="TVD gap threshold for tvd-only clustering (default: 200 ft)")
    parser.add_argument(
        "--input", type=str, default=None,
        help="Input formation_tops.csv path")
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output formation_tops_canonical.csv path")
    parser.add_argument(
        "--overrides", type=str, default=None,
        help="Path to JSON overrides file for custom groupings")
    parser.add_argument(
        "--export-csv", action="store_true",
        help="Also dump CSV to exports/")

    args = parser.parse_args()

    # Resolve paths
    input_path = args.input or os.path.join(SCRIPT_DIR, "formation_tops.csv")
    if not os.path.isabs(input_path):
        input_path = os.path.join(SCRIPT_DIR, input_path)

    output_path = args.output or os.path.join(
        SCRIPT_DIR, "formation_tops_canonical.csv")
    if not os.path.isabs(output_path):
        output_path = os.path.join(SCRIPT_DIR, output_path)

    json_path = output_path.replace(".csv", "").replace(
        "_canonical", "") + "_canonical_map.json"
    # Default: formation_tops_canonical_map.json
    if "canonical_map" not in json_path:
        json_path = os.path.join(SCRIPT_DIR, "canonical_map.json")

    print(f"\n{'=' * 70}")
    print(f"  NORMALIZE FORMATIONS")
    print(f"  Mode:  {args.mode}")
    print(f"  Input: {os.path.basename(input_path)}")
    print(f"{'=' * 70}")

    # Load data
    all_tops = load_formation_tops(input_path)
    if not all_tops:
        print("  ERROR: No formation data loaded.")
        return

    by_well = tops_by_well(all_tops)
    orig_names = set(r["formation_name"] for r in all_tops)
    print(f"\n  Loaded {len(all_tops)} formation tops from {len(by_well)} wells")
    print(f"  Unique raw formation names: {len(orig_names)}")

    # Load overrides if provided
    overrides = None
    if args.overrides:
        override_path = args.overrides
        if not os.path.isabs(override_path):
            override_path = os.path.join(SCRIPT_DIR, override_path)
        if os.path.exists(override_path):
            overrides = load_overrides(override_path)
            print(f"  Loaded overrides from: {os.path.basename(override_path)}")
        else:
            print(f"  WARNING: Overrides file not found: {override_path}")

    # Run normalization
    if args.mode == "target-reference":
        if not args.target_asset:
            # Try to pick the well with the most formations
            best = max(by_well.items(), key=lambda x: len(x[1]))
            print(f"\n  WARNING: No --target-asset specified.")
            print(f"  Auto-selecting well with most formations: "
                  f"{best[1][0]['well_name']} ({best[0]}, "
                  f"{len(best[1])} formations)")
            target_id = best[0]
        else:
            target_id = args.target_asset

        consolidated, canonical_map = run_target_reference(
            all_tops, target_id, overrides)

    else:  # tvd-only
        consolidated, canonical_map = cluster_by_tvd(
            all_tops, gap_threshold=args.tvd_gap)

    if not consolidated:
        print("\n  ERROR: No consolidated data produced.")
        return

    # Save outputs
    save_canonical_csv(consolidated, output_path)

    # Save canonical formation tops to database
    try:
        db.save_formation_tops(consolidated, replace_asset=None)
    except Exception as e:
        print(f"  DB save warning: {e}")

    json_out = os.path.join(SCRIPT_DIR, "canonical_map.json")
    save_canonical_map(canonical_map, json_out)

    # Save canonical formations to database
    canonical_formations_data = list(canonical_map["canonical_formations"])
    # Normalize tvd-only entries: db expects sub_formations/target_sub_formations
    for entry in canonical_formations_data:
        if "member_names" in entry and "target_sub_formations" not in entry and "sub_formations" not in entry:
            entry["target_sub_formations"] = entry["member_names"]
    try:
        latest = db.get_latest_run()
        if latest:
            db.save_canonical_formations(latest["id"], canonical_formations_data)
    except Exception as e:
        print(f"  DB save warning: {e}")

    if args.export_csv:
        db.export_csv(consolidated, "formation_tops_canonical")

    # Summary
    print_summary(all_tops, consolidated, canonical_map)

    print(f"\n  Next step:")
    print(f"    python pull_1ft_for_runs.py <bha_csv> "
          f"--mode vertical --formations {os.path.basename(output_path)}")


if __name__ == "__main__":
    main()
