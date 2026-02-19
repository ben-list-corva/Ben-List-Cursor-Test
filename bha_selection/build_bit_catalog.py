"""Build a deduplicated catalog of all unique bit models seen across all BHA CSVs.

Reads every lateral_bhas*.csv and bhas_*.csv file, deduplicates by
(manufacturer, model), and produces a single reference table with:
  - bit_manufacturer, bit_model, bit_size (diameters seen)
  - parsed_blades, parsed_cutter_mm, parse_confidence
  - total_runs, basins/datasets where seen
"""
import csv
import os
import sys
from collections import defaultdict

import db

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    export_csv_flag = "--export-csv" in sys.argv

    # Find all BHA CSVs (offset runs + full scan)
    csvs = sorted(
        os.path.join(SCRIPT_DIR, f)
        for f in os.listdir(SCRIPT_DIR)
        if (f.startswith("lateral_bhas") or f.startswith("bhas_")
            or f == "full_bit_scan.csv") and f.endswith(".csv")
    )

    if not csvs:
        print("No BHA CSV files found!")
        sys.exit(1)

    print(f"Reading {len(csvs)} BHA CSV files...")

    # Collect all unique (manufacturer, model) combos
    catalog = {}  # key = (mfg, model) -> info dict

    for csv_path in csvs:
        source = os.path.basename(csv_path)
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                mfg = (row.get("bit_manufacturer") or "").strip()
                model = (row.get("bit_model") or "").strip()
                
                if not model or model == "N/A":
                    continue
                if "Placeholder" in model:
                    continue

                key = (mfg, model)
                if key not in catalog:
                    catalog[key] = {
                        "bit_manufacturer": mfg,
                        "bit_model": model,
                        "bit_sizes": set(),
                        "parsed_blades": row.get("parsed_blades", ""),
                        "parsed_cutter_mm": row.get("parsed_cutter_mm", ""),
                        "parse_confidence": row.get("parse_confidence", ""),
                        "parse_method": row.get("parse_method", ""),
                        "total_runs": 0,
                        "sources": set(),
                        "operators": set(),
                    }

                info = catalog[key]
                info["total_runs"] += 1
                
                bit_size = row.get("bit_size", "")
                if bit_size and bit_size != "N/A":
                    info["bit_sizes"].add(str(bit_size))
                
                info["sources"].add(source)
                
                op = (row.get("operator") or "").strip()
                if op:
                    info["operators"].add(op)

    # Sort: confident first, then by total runs descending
    conf_order = {"high": 0, "check": 1, "unknown": 2, "": 3}
    entries = sorted(
        catalog.values(),
        key=lambda x: (conf_order.get(x["parse_confidence"], 3), -x["total_runs"], x["bit_manufacturer"], x["bit_model"])
    )

    # Print summary
    total_models = len(entries)
    high = sum(1 for e in entries if e["parse_confidence"] == "high")
    check = sum(1 for e in entries if e["parse_confidence"] == "check")
    unknown = sum(1 for e in entries if e["parse_confidence"] in ("unknown", ""))

    print(f"\n{'=' * 100}")
    print(f"  BIT MODEL CATALOG")
    print(f"  Total unique models: {total_models}")
    print(f"  Confident: {high} | Needs check: {check} | Unknown: {unknown}")
    print(f"{'=' * 100}\n")

    # Print table
    header = (
        f"{'Manufacturer':<18} {'Model':<22} {'Diameter(s)':<16} "
        f"{'Blades':<7} {'Cutter':<8} {'Conf':<9} {'Runs':<5} {'Parse Method'}"
    )
    print(header)
    print("-" * len(header))

    for e in entries:
        sizes = ", ".join(sorted(e["bit_sizes"]))[:14]
        method_short = e["parse_method"].split(":")[0] if e["parse_method"] else ""
        print(
            f"{e['bit_manufacturer'][:16]:<18} {e['bit_model'][:20]:<22} {sizes:<16} "
            f"{e['parsed_blades']:<7} {e['parsed_cutter_mm']:<8} {e['parse_confidence']:<9} "
            f"{e['total_runs']:<5} {method_short}"
        )

    # Save to CSV
    out_path = os.path.join(SCRIPT_DIR, "bit_catalog.csv")
    fieldnames = [
        "bit_manufacturer", "bit_model", "bit_diameters",
        "parsed_blades", "parsed_cutter_mm", "parse_confidence", "parse_method",
        "total_runs", "operators", "sources"
    ]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for e in entries:
            writer.writerow({
                "bit_manufacturer": e["bit_manufacturer"],
                "bit_model": e["bit_model"],
                "bit_diameters": "; ".join(sorted(e["bit_sizes"])),
                "parsed_blades": e["parsed_blades"],
                "parsed_cutter_mm": e["parsed_cutter_mm"],
                "parse_confidence": e["parse_confidence"],
                "parse_method": e["parse_method"],
                "total_runs": e["total_runs"],
                "operators": "; ".join(sorted(e["operators"])),
                "sources": "; ".join(sorted(e["sources"])),
            })

    print(f"\nSaved catalog to: {out_path}")

    catalog_entries = [
        {
            "bit_manufacturer": e["bit_manufacturer"],
            "bit_model": e["bit_model"],
            "bit_diameters": "; ".join(sorted(e["bit_sizes"])),
            "parsed_blades": e["parsed_blades"],
            "parsed_cutter_mm": e["parsed_cutter_mm"],
            "parse_confidence": e["parse_confidence"],
            "parse_method": e["parse_method"],
            "total_runs": e["total_runs"],
            "operators": "; ".join(sorted(e["operators"])),
            "sources": "; ".join(sorted(e["sources"])),
        }
        for e in entries
    ]
    db.save_bit_catalog(catalog_entries)

    if export_csv_flag:
        db.export_csv(catalog_entries, "bit_catalog")

    # Print "needs review" section
    needs_review = [e for e in entries if e["parse_confidence"] in ("check", "unknown", "")]
    if needs_review:
        print(f"\n{'=' * 100}")
        print(f"  MODELS NEEDING REVIEW ({len(needs_review)})")
        print(f"{'=' * 100}\n")
        for e in needs_review:
            print(f"  {e['bit_manufacturer']:<16} {e['bit_model']:<22} -> blades={e['parsed_blades']}, cutter={e['parsed_cutter_mm']}  ({e['parse_method']})")


if __name__ == "__main__":
    main()
