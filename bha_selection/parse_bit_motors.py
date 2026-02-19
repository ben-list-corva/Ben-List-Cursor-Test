"""Parse bit model strings to extract blade count and cutter size.

Two industry encoding conventions:

  CONVENTION 1 - Fractional Inch (Baker Hughes, Halliburton):
    Cutter digit = numerator of X/8 inch:
      3 -> 3/8" -> ~8mm    (uncommon)
      4 -> 4/8" -> 13mm    (confirmed)
      5 -> 5/8" -> 16mm    (reclassified: nominally 15.875mm, grouped as 16mm)
    Digit ORDER: cutter FIRST, zero separator, blades last
      Example: DD506TS -> 5=16mm, 0, 6=blades -> 6 blades, 16mm

  CONVENTION 2 - Metric (NOV, Schlumberger, Ulterra, Smith):
    Cutter = last digit of mm (2-digit) or literal mm (3-digit):
      3 -> 13mm    5 -> 16mm    6 -> 16mm    1 -> 11mm
      13 -> 13mm   16 -> 16mm   11 -> 11mm   15 -> 16mm
    Digit ORDER: blades FIRST, cutter last
      Example: TK63-G9  -> 6=blades, 3=13mm
      Example: Z613S    -> 6=blades, 13=13mm (literal)

  NOTE: 15mm and 16mm cutters are grouped together as 16mm.
  Baker 5/8" (15.875mm) and metric 16mm are functionally equivalent.
  Metric "15" literals are also remapped to 16mm for consistency.

  DETECTION LOGIC (model-string-shape, not manufacturer):
    1. X0Y pattern (3-digit, zero in middle) -> Convention 1 (Baker)
    2. 3+ digits, blades-first, literal mm    -> Convention 2 (Metric)
    3. 2 digits: use prefix to pick convention
       - H* (Halliburton) -> Convention 1 (fraction)
       - TK* (NOV)        -> Convention 2 (metric last-digit)
"""
import csv
import os
import re
import sys

import db

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---- Cutter code -> mm mappings ----

# Convention 1: Fractional inch (Baker / Halliburton)
FRACTION_CUTTER_MAP = {
    "3": 8,     # 3/8" (uncommon, needs verification)
    "4": 13,    # 4/8" = confirmed 13mm
    "5": 16,    # 5/8" = 15.875mm, grouped as 16mm
}

# Convention 2: Metric last-digit (NOV TK-series)
METRIC_LASTDIGIT_MAP = {
    "1": 11,
    "3": 13,
    "5": 16,    # 15mm -> grouped as 16mm
    "6": 16,
}


def parse_bit(manufacturer, model):
    """Parse any PDC bit model string to extract (blades, cutter_mm).

    Detection order:
      1. Known prefix patterns (TK*, Z*, U*, SPL*, SDI*, XP*, H*)
      2. Baker X0Y pattern (any model with [digit]0[digit])
      3. 3-digit blades-first literal-mm fallback
      4. 2-digit with best-guess convention
    """
    if not model or model == "N/A" or "Placeholder" in str(model):
        return {"blades": "", "cutter_mm": "", "parse_method": "skip", "confidence": ""}

    model_clean = str(model).strip().lstrip("( ")

    # Valid blade counts and cutter sizes for sanity checking
    VALID_BLADES = {3, 4, 5, 6, 7, 8}
    VALID_CUTTER_MM = {8, 9, 11, 13, 14, 15, 16, 19, 22}

    # ========== PATTERN 1: NOV TK/TKC/TKF/TKFC/TFK (2-digit, metric convention) ==========
    # Allow any combo of C/F/K after T: TK, TKC, TKF, TKFC, TFK, TKCC, etc.
    # Also handle transpositions like TFK (common data entry error for TKF)
    m = re.search(r'T[KFCkfc]{1,4}(\d)(\d)', model_clean)
    if m:
        blades, cc = int(m.group(1)), m.group(2)
        if blades in VALID_BLADES:
            mm = METRIC_LASTDIGIT_MAP.get(cc)
            conf = "high" if mm else "check"
            return _result(blades, mm or f"?({cc})", f"NOV-TK:{model_clean}->B{blades},C{cc}", conf)

    # ========== PATTERN 2: NOV TX/TXd/Taurex TSt/TST/TSd (3-digit, literal mm) ==========
    # Allow optional space between prefix and digits (e.g., "TXd 614")
    m = re.search(r'T[SXsx][A-Za-z]?\s?(\d)(\d{2})', model_clean)
    if m:
        blades, mm = int(m.group(1)), int(m.group(2))
        if blades in VALID_BLADES and mm in VALID_CUTTER_MM:
            return _result(blades, mm, f"TX:{model_clean}->B{blades},{mm}mm", "high")

    # ========== PATTERN 3: SLB Z-series (3-digit, literal mm) ==========
    m = re.search(r'Z(\d)(\d{2})', model_clean)
    if m:
        blades, mm = int(m.group(1)), int(m.group(2))
        if blades in VALID_BLADES and mm in VALID_CUTTER_MM:
            return _result(blades, mm, f"SLB-Z:{model_clean}->B{blades},{mm}mm", "high")

    # ========== PATTERN 4: SLB BXT/BT/DXT-series (3-digit, literal mm) ==========
    # Matches: BXT616SM, BT613SM, DXT616SM
    m = re.search(r'[BD]X?T(\d)(\d{2})', model_clean)
    if m:
        blades, mm = int(m.group(1)), int(m.group(2))
        if blades in VALID_BLADES and mm in VALID_CUTTER_MM:
            return _result(blades, mm, f"SLB-BT:{model_clean}->B{blades},{mm}mm", "high")

    # ========== PATTERN 5: XP-series (3-digit, literal mm) ==========
    m = re.search(r'XP(\d)(\d{2})', model_clean)
    if m:
        blades, mm = int(m.group(1)), int(m.group(2))
        if blades in VALID_BLADES and mm in VALID_CUTTER_MM:
            return _result(blades, mm, f"XP:{model_clean}->B{blades},{mm}mm", "high")

    # ========== PATTERN 6: SLB SDI-series (3-digit, literal mm) ==========
    m = re.search(r'SDI(\d)(\d{2})', model_clean)
    if m:
        blades, mm = int(m.group(1)), int(m.group(2))
        if blades in VALID_BLADES and mm in VALID_CUTTER_MM:
            return _result(blades, mm, f"SLB-SDI:{model_clean}->B{blades},{mm}mm", "high")

    # ========== PATTERN 7: Ulterra U-series (3-digit, literal mm) ==========
    # Must start with U followed by a valid blade digit (3-8)
    m = re.search(r'U([3-8])(\d{2})', model_clean)
    if m:
        blades, mm = int(m.group(1)), int(m.group(2))
        if mm in VALID_CUTTER_MM:
            return _result(blades, mm, f"Ulterra-U:{model_clean}->B{blades},{mm}mm", "high")

    # ========== PATTERN 8: Ulterra SPL/RPS-series (3-digit, literal mm) ==========
    m = re.search(r'(?:SPL|RPS)(\d)(\d{2})', model_clean)
    if m:
        blades, mm = int(m.group(1)), int(m.group(2))
        if blades in VALID_BLADES and mm in VALID_CUTTER_MM:
            return _result(blades, mm, f"Ulterra:{model_clean}->B{blades},{mm}mm", "high")

    # ========== PATTERN 9: Varel VION-series (3-digit, literal mm) ==========
    # Case-insensitive: Vion-616, VION-616, Vion 616
    m = re.search(r'[Vv][Ii][Oo][Nn][- ]?(\d)(\d{2})', model_clean)
    if m:
        blades, mm = int(m.group(1)), int(m.group(2))
        if blades in VALID_BLADES and mm in VALID_CUTTER_MM:
            return _result(blades, mm, f"Varel:{model_clean}->B{blades},{mm}mm", "high")

    # ========== PATTERN 10: Ulterra CF/WAV-series (3-digit, literal mm) ==========
    # Matches: CF611, CF613, CF616, CF716, WAV616
    m = re.search(r'(?:CF|WAV)(\d)(\d{2})', model_clean)
    if m:
        blades, mm = int(m.group(1)), int(m.group(2))
        if blades in VALID_BLADES and mm in VALID_CUTTER_MM:
            return _result(blades, mm, f"Ulterra-CF:{model_clean}->B{blades},{mm}mm", "high")

    # ========== PATTERN 11: Ulterra RP-series (incomplete RPS, 3-digit, literal mm) ==========
    # Matches: RP516 (likely incomplete "RPS516")
    m = re.search(r'RP(\d)(\d{2})', model_clean)
    if m:
        blades, mm = int(m.group(1)), int(m.group(2))
        if blades in VALID_BLADES and mm in VALID_CUTTER_MM:
            return _result(blades, mm, f"Ulterra-RP:{model_clean}->B{blades},{mm}mm", "high")

    # ========== PATTERN 12: Halliburton GTD-series (2-digit, fraction convention) ==========
    # Matches: GTD64DU -- Halliburton GaugeTech line, same encoding as HD
    m = re.search(r'GTD(\d)(\d)', model_clean)
    if m:
        blades, cc = int(m.group(1)), m.group(2)
        if blades in VALID_BLADES:
            mm = FRACTION_CUTTER_MAP.get(cc)
            conf = "high" if mm else "check"
            return _result(blades, mm or f"?({cc})", f"HAL-GTD:{model_clean}->B{blades},C{cc}(frac)", conf)

    # ========== PATTERN 13: Halliburton H-prefix (2-digit, fraction convention) ==========
    # Matches: HD64s, HXi64s, HXi64Ms, HD64M, HD65E, HD65K, HDi64, HBDS HD64M, HXi54s, HXi65s
    m = re.search(r'H[A-Za-z]*(\d)(\d)', model_clean)
    if m:
        blades, cc = int(m.group(1)), m.group(2)
        if blades in VALID_BLADES:
            mm = FRACTION_CUTTER_MAP.get(cc)
            conf = "high" if mm else "check"
            return _result(blades, mm or f"?({cc})", f"HAL:{model_clean}->B{blades},C{cc}(frac)", conf)

    # ========== PATTERN 14: Baker X0Y (3-digit, cutter-first, fraction convention) ==========
    # Matches: DD506TS, D406TS, P406S, TD406FS, LC-D405TS, P306WS, P506WH, P507WH, DD506THX
    m = re.search(r'(\d)0(\d)', model_clean)
    if m:
        cc, blades = m.group(1), int(m.group(2))
        if blades in VALID_BLADES:
            mm = FRACTION_CUTTER_MAP.get(cc)
            conf = "high" if mm else "check"
            return _result(blades, mm or f"?({cc})", f"Baker:{model_clean}->C{cc}0B{blades}(frac)", conf)

    # ========== PATTERN 15: Bare 3-digit start (e.g., "613-N3") ==========
    # Models that start with digits and look like "[B][CC]-suffix" (missing prefix)
    m = re.match(r'^(\d)(\d{2})\b', model_clean)
    if m:
        blades, mm = int(m.group(1)), int(m.group(2))
        if blades in VALID_BLADES and mm in VALID_CUTTER_MM:
            return _result(blades, mm, f"bare-3dig:{model_clean}->B{blades},{mm}mm", "high")

    # ========== FALLBACKS with sanity checks ==========

    # Try 3-digit blades-first literal mm (only if values are sane)
    m = re.search(r'(\d)(\d{2})', model_clean)
    if m:
        blades, mm = int(m.group(1)), int(m.group(2))
        if blades in VALID_BLADES and mm in VALID_CUTTER_MM:
            return _result(blades, mm, f"fallback-3dig:{model_clean}->B{blades},{mm}mm", "check")

    # Try 2-digit pattern (only if blade count is sane)
    m = re.search(r'(\d)(\d)', model_clean)
    if m:
        blades, cc = int(m.group(1)), m.group(2)
        if blades in VALID_BLADES:
            return _result(blades, f"?({cc})", f"fallback-2dig:{model_clean}->B{blades},C{cc}", "check")

    return _result("?", "?", f"no_match:{model_clean}", "unknown")


def _result(blades, cutter_mm, method, confidence):
    # Remap 15mm -> 16mm (5/8" = 15.875mm, functionally same as 16mm)
    cm = cutter_mm
    if cm == 15 or cm == "15":
        cm = 16
    return {
        "blades": str(blades),
        "cutter_mm": str(cm),
        "parse_method": method,
        "confidence": confidence,
    }


def parse_single_bha(row):
    """Parse bit and motor fields from a BHA row dict. Returns dict for update_bha_parsed_fields."""
    bit = parse_bit(row.get("bit_manufacturer", ""), row.get("bit_model", ""))
    motor = parse_motor_lobes(row.get("motor_model", ""), row.get("motor_rpg", ""))
    return {
        "parsed_blades": bit["blades"],
        "parsed_cutter_mm": bit["cutter_mm"],
        "parse_confidence": bit["confidence"],
        "parse_method": bit["parse_method"],
        "motor_lobe_config": motor["motor_lobe_config"],
        "motor_rpg_band": motor["motor_rpg_band"],
    }


def parse_motor_lobes(motor_model, motor_rpg):
    """Parse motor model string to extract lobe configuration."""
    if not motor_model or motor_model == "N/A" or "Placeholder" in str(motor_model):
        return {"motor_lobe_config": "", "motor_rpg_band": ""}

    model = str(motor_model).strip()

    # Extract X/Y lobe pattern
    m = re.search(r'(\d)/(\d)', model)
    lobe_config = f"{m.group(1)}/{m.group(2)}" if m else "?"

    # RPG band
    try:
        rpg = float(motor_rpg)
        if rpg <= 0.30:
            rpg_band = "lo"
        elif rpg <= 0.45:
            rpg_band = "mid"
        elif rpg <= 0.55:
            rpg_band = "hi"
        else:
            rpg_band = "vhi"
    except (ValueError, TypeError):
        rpg_band = "?"

    return {"motor_lobe_config": lobe_config, "motor_rpg_band": rpg_band}


def process_csv(csv_path):
    """Read a lateral_bhas CSV, add parsed columns, write back."""
    rows = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        for row in reader:
            rows.append(row)

    new_cols = ["parsed_blades", "parsed_cutter_mm", "parse_confidence", "parse_method",
                "motor_lobe_config", "motor_rpg_band"]
    base_fieldnames = [f for f in fieldnames if f not in new_cols]
    out_fieldnames = base_fieldnames + new_cols

    stats = {"total": 0, "high": 0, "check": 0, "unknown": 0, "skip": 0}

    for row in rows:
        stats["total"] += 1
        bit = parse_bit(row.get("bit_manufacturer", ""), row.get("bit_model", ""))
        motor = parse_motor_lobes(row.get("motor_model", ""), row.get("motor_rpg", ""))

        row["parsed_blades"] = bit["blades"]
        row["parsed_cutter_mm"] = bit["cutter_mm"]
        row["parse_confidence"] = bit["confidence"]
        row["parse_method"] = bit["parse_method"]
        row["motor_lobe_config"] = motor["motor_lobe_config"]
        row["motor_rpg_band"] = motor["motor_rpg_band"]

        conf = bit["confidence"]
        if conf in stats:
            stats[conf] += 1
        else:
            stats["unknown"] += 1

    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=out_fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    except PermissionError:
        print(f"  WARNING: Cannot write to {csv_path} (file locked, open in Excel?). Skipping save.")

    return rows, stats


def print_summary(rows, stats, label):
    print(f"\n{'=' * 90}")
    print(f"  {label}")
    print(f"  Total: {stats['total']} | High: {stats['high']} | Check: {stats['check']} | "
          f"Unknown: {stats['unknown']} | Skipped: {stats['skip']}")
    print(f"{'=' * 90}\n")

    # Bit groups
    groups = {}
    for row in rows:
        b, c = row.get("parsed_blades", ""), row.get("parsed_cutter_mm", "")
        if not b and not c:
            continue
        key = (b, c)
        if key not in groups:
            groups[key] = {"count": 0, "models": set(), "methods": set()}
        groups[key]["count"] += 1
        groups[key]["models"].add(row.get("bit_model", ""))
        groups[key]["methods"].add(row.get("parse_method", "").split(":")[0])

    print(f"  {'Blades':<8} {'Cutter':<10} {'Conv':<14} {'Runs':<6} Models")
    print(f"  {'-' * 84}")
    for (b, c), info in sorted(groups.items(), key=lambda x: (-x[1]["count"], x[0])):
        models = ", ".join(sorted(info["models"]))[:55]
        conv = ", ".join(sorted(info["methods"]))
        print(f"  {b:<8} {c:<10} {conv:<14} {info['count']:<6} {models}")

    # Motor groups
    mgroups = {}
    for row in rows:
        lobe = row.get("motor_lobe_config", "")
        band = row.get("motor_rpg_band", "")
        if not lobe:
            continue
        key = (lobe, band)
        if key not in mgroups:
            mgroups[key] = {"count": 0, "rpgs": []}
        mgroups[key]["count"] += 1
        try:
            mgroups[key]["rpgs"].append(float(row.get("motor_rpg", "")))
        except (ValueError, TypeError):
            pass

    print(f"\n  {'Lobes':<8} {'Band':<8} {'Runs':<6} {'RPG Range'}")
    print(f"  {'-' * 40}")
    for (lobe, band), info in sorted(mgroups.items()):
        rpgs = info["rpgs"]
        rng = f"{min(rpgs):.3f} - {max(rpgs):.3f}" if rpgs else "N/A"
        print(f"  {lobe:<8} {band:<8} {info['count']:<6} {rng}")


def main():
    export_csv_flag = "--export-csv" in sys.argv
    sys.argv = [a for a in sys.argv if a != "--export-csv"]

    # Process all BHA CSV files (*_bhas* and bhas_*)
    BHA_PREFIXES = ("lateral_bhas", "intermediate_bhas", "vertical_bhas",
                    "surface_bhas", "curve_bhas", "all_bhas", "bhas_")
    csvs = sorted(
        os.path.join(SCRIPT_DIR, f)
        for f in os.listdir(SCRIPT_DIR)
        if any(f.startswith(p) for p in BHA_PREFIXES) and f.endswith(".csv")
    )
    if not csvs:
        print("No BHA CSV files found!")
        sys.exit(1)

    for csv_path in csvs:
        label = os.path.basename(csv_path)
        print(f"\nProcessing: {label}")
        rows, stats = process_csv(csv_path)
        print_summary(rows, stats, label)
        print(f"  Saved -> {csv_path}")

    # Also update database if available
    try:
        latest = db.get_latest_run()
        if latest:
            bha_rows = db.get_bha_runs(latest["id"])
            updated = 0
            for row in bha_rows:
                if not row.get("parsed_blades"):
                    fields = parse_single_bha(row)
                    db.update_bha_parsed_fields(latest["id"], row["id"], fields)
                    updated += 1
            print(f"\n  DB: Updated {updated} BHA rows with parsed fields")
            if export_csv_flag and bha_rows:
                bha_rows = db.get_bha_runs(latest["id"])
                db.export_csv(bha_rows, "bha_runs_parsed")
    except Exception as e:
        print(f"  DB update warning: {e}")


if __name__ == "__main__":
    main()
