# Bit Characterization Logic

How we extract blade count and cutter size from PDC bit model strings.

**Parser**: `bha_selection/parse_bit_motors.py`
**Full scan**: `bha_selection/full_corva_bit_scan.py` (scans all 57,776 wells on Corva)
**Catalog**: `bha_selection/bit_catalog.csv` (run `build_bit_catalog.py` or Phase 3 of full scan)

---

## The Problem

Corva's `data.drillstring` records include bit `model` and `make` (manufacturer) as free-text strings, but `blade_count` and `cutter_size` fields are almost always empty. However, the model string itself **encodes** blade count and cutter size using industry-standard naming conventions.

## The Two Encoding Conventions

Every PDC bit model number encodes two key values: **blade count** (typically 3-8) and **cutter size**. There are exactly two conventions used across bit manufacturers:

### Convention 1: Fractional Inch (Baker Hughes, Halliburton)

The cutter digit represents X/8 of an inch. The digit ORDER is **cutter first, blades last**, separated by a zero.

**Pattern**: `[alpha prefix][C]0[B][alpha suffix]`

- `C` = cutter code (digit, representing X/8 inch)
- `B` = blade count (digit)

**Cutter code to mm mapping**:

| Code | Fraction | Actual mm | Grouped as | Confirmed? |
|------|----------|-----------|------------|------------|
| 3    | 3/8"     | 9.525mm   | 8mm        | Needs verification |
| 4    | 4/8"     | 12.7mm    | 13mm       | Confirmed |
| 5    | 5/8"     | 15.875mm  | **16mm**   | Confirmed (reclassified from 15mm) |

> **Note**: 5/8" (15.875mm) is grouped as 16mm. The 15mm and 16mm cutter sizes are functionally equivalent and are unified under 16mm for all grouping purposes.

**Examples**:

| Model | Prefix | Code | Cutter | Blades | mm |
|-------|--------|------|--------|--------|----|
| DD**506**TS | DD | 506 | 5 | 6 | 16mm |
| D**406**TS | D | 406 | 4 | 6 | 13mm |
| LC-D**405**TS | LC-D | 405 | 4 | 5 | 13mm |
| P**306**WS | P | 306 | 3 | 6 | ~8mm |
| P**507**WH | P | 507 | 5 | 7 | 16mm |
| TD**406**FS | TD | 406 | 4 | 6 | 13mm |

**Baker prefix variants**: DD, D, TD, P, LC-, LC-D, LC-DD

**Halliburton** uses the same fractional inch convention for the cutter digit, but with a **blades-first** order (like Convention 2). The two-digit core after stripping the H-prefix is `[blades][cutter_code]`.

| Model | Prefix | Blades | Cutter Code | mm |
|-------|--------|--------|-------------|----|
| HD**64**s | HD | 6 | 4 | 13mm |
| HXi**64**s | HXi | 6 | 4 | 13mm |
| HD**65**E | HD | 6 | 5 | 16mm |
| HXi**54**s | HXi | 5 | 4 | 13mm |
| HD**65**K | HD | 6 | 5 | 16mm |

**Halliburton prefix variants**: HD, HXi, HDi, HBDS (followed by HD/HXi)

### Convention 2: Metric (NOV, Schlumberger, Ulterra, Smith, Taurex, Varel)

The cutter value is either the **last digit of the mm size** (in 2-digit models) or **literal mm** (in 3-digit models). The digit ORDER is always **blades first, cutter last**.

**Two-digit pattern** (NOV TK-series): `TK[C|F]*[B][C_last_digit]-suffix`

| Last Digit | mm Size | Grouped as | Confirmed? |
|------------|---------|------------|------------|
| 1          | 11mm    | 11mm       | Inferred (U611, CF611) |
| 3          | 13mm    | 13mm       | Confirmed (TK63 = 13mm) |
| 4          | 14mm    | 14mm       | Seen once (TXd 614), needs verification |
| 5          | 15mm    | **16mm**   | Reclassified: grouped with 16mm |
| 6          | 16mm    | 16mm       | Confirmed (TK56 = 5 blades, 16mm) |
| 7          | 17mm?   | 17mm?      | Seen once (TKC67), needs verification |

**Three-digit pattern** (literal mm): `[prefix][B][CC]-suffix`

| Model | Prefix | Blades | Cutter (literal mm) |
|-------|--------|--------|---------------------|
| Z**613**S | Z | 6 | 13mm |
| BXT**616**SM | BXT | 6 | 16mm |
| BT**516**M | BT | 5 | 16mm |
| SDI**611** | SDI | 6 | 11mm |
| XP**616** | XP | 6 | 16mm |
| SPL**616** | SPL | 6 | 16mm |
| U**613**M | U | 6 | 13mm |
| TXd**613** | TXd | 6 | 13mm |
| VION-**616** | VION- | 6 | 16mm |
| TSt**616** | TSt | 6 | 16mm |
| RPS**616** | RPS | 6 | 16mm |
| CF**611** | CF | 6 | 11mm |

## Parser Detection Order

The parser in `parse_bit_motors.py` uses **model string shape** (not manufacturer name) to classify bits. This makes it robust to manufacturer field errors in the data.

Detection cascade:

1. **NOV TK-series**: regex `T[KFCkfc]{1,4}(\d)(\d)` -- matches TK, TKC, TKF, TKFC, TFK (transposition), TKCC, etc.
2. **NOV/Taurex TX-series**: regex `T[SXsx][A-Za-z]?\s?(\d)(\d{2})` -- matches TXd, TSt, TSd, TST (case-insensitive), allows space before digits
3. **SLB Z-series**: regex `Z(\d)(\d{2})`
4. **SLB BXT/BT/DXT**: regex `[BD]X?T(\d)(\d{2})`
5. **XP-series**: regex `XP(\d)(\d{2})`
6. **SLB SDI-series**: regex `SDI(\d)(\d{2})`
7. **Ulterra U-series**: regex `U([3-8])(\d{2})` -- requires valid blade digit to avoid false matches
8. **Ulterra SPL/RPS**: regex `(?:SPL|RPS)(\d)(\d{2})`
9. **Varel VION**: regex `[Vv][Ii][Oo][Nn][- ]?(\d)(\d{2})` -- case-insensitive
10. **Ulterra CF/WAV**: regex `(?:CF|WAV)(\d)(\d{2})` -- CutterForce and Wave product lines
11. **Ulterra RP**: regex `RP(\d)(\d{2})` -- catches incomplete "RPS" entries
12. **Halliburton GTD**: regex `GTD(\d)(\d)` -- GaugeTech line, fraction convention
13. **Halliburton H-prefix**: regex `H[A-Za-z]*(\d)(\d)` -- fraction convention
14. **Baker X0Y pattern**: regex `(\d)0(\d)` -- fraction convention, cutter-first
15. **Bare 3-digit start**: regex `^(\d)(\d{2})\b` -- models starting with digits (e.g., "613-N3")
16. **Fallback 3-digit**: regex `(\d)(\d{2})` with sanity checks
17. **Fallback 2-digit**: regex `(\d)(\d)` with blade sanity check

**Sanity checks** (applied to fallbacks):
- Valid blade counts: 3, 4, 5, 6, 7, 8
- Valid cutter sizes (mm): 8, 9, 11, 13, 14, 15, 16, 19, 22 (note: 15mm is remapped to 16mm in output)

## Full-Corva Scan Results (Feb 2026)

Ran across all 57,776 wells accessible via API, filtering to BHAs from the past 18 months.

| Metric | Count |
|--------|-------|
| Wells scanned | 57,776 |
| Wells with BHA data | 13,088 |
| Total BHA runs extracted | 64,865 |
| BHAs with bit model data | 44,487 |
| Unique bit models | 5,040 |

**Row-level confidence** (of 44,487 BHAs with model strings):

| Confidence | Runs | % |
|-----------|------|---|
| High | 35,874 | 80.7% |
| Check | 6,613 | 14.9% |
| Unknown | 2,000 | 4.5% |

**Top parse methods by volume**:

| Method | Runs |
|--------|------|
| Baker (X0Y) | 10,251 |
| NOV-TK | 9,955 |
| HAL (H-prefix) | 3,796 |
| Ulterra-U | 2,763 |
| Ulterra (SPL/RPS) | 2,374 |
| TX (Taurex/NOV) | 1,803 |
| XP | 1,782 |
| Ulterra-CF | 1,636 |
| SLB-BT | 873 |
| SLB-Z | 829 |
| Varel (VION) | 618 |
| HAL-GTD | 247 |

## Known Edge Cases and Unresolved Models

### High-volume models needing new patterns (next parser iteration)

These are the most-common models currently at "check" or "unknown" confidence, discovered during the full-Corva scan. Adding dedicated patterns for these would increase coverage significantly.

| Model | Manufacturer | Runs | Likely Parse | Notes |
|-------|-------------|------|--------------|-------|
| BY519 | Schlumberger | 234 | 5B, 19mm | SLB Y-series, 3-digit literal mm |
| DF611 | Drilformance | 154 | 6B, 11mm | 3-digit literal mm |
| BF513 | Schlumberger | 92 | 5B, 13mm | SLB F-series, 3-digit literal mm |
| A1GRC | Halliburton | 86 | ? | Not standard PDC encoding |
| XR+C | Schlumberger | 79 | ? | Not standard PDC encoding |
| SF56 | Halliburton | 77 | 5B, 6/8"=19mm? | Halliburton fraction convention |
| RH76P-E1 | NOV | 77 | 7B, 16mm | NOV metric convention (not Halliburton!) |
| HF513 | Schlumberger | 74 | 5B, 13mm | SLB H-series, 3-digit literal mm |
| BF616MC | Schlumberger | 69 | 6B, 16mm | SLB F-series, 3-digit literal mm |
| DD604M | Baker Hughes | 67 | 4B, 6/8"=19mm? | Baker X0Y, cutter code 6 |
| GT65s | Halliburton | 67 | 6B, 5/8"=16mm | Halliburton GT line, fraction convention (grouped as 16mm) |
| D605S | Baker Hughes | 65 | 5B, 6/8"=19mm? | Baker X0Y, cutter code 6 |
| HT513 | Schlumberger | 54 | 5B, 13mm | SLB HT-series, 3-digit literal mm |
| SPD616 | Diamant | 53 | 6B, 16mm | 3-digit literal mm |
| BF613 | Schlumberger | 50 | 6B, 13mm | SLB F-series, 3-digit literal mm |
| K6M425 | Baker Hughes | 50 | ? | Kymera hybrid bit, non-standard encoding |
| TK59 | NOV | 49 | 5B, code 9=? | Metric code 9 not in map (19mm?) |
| U913M | Ulterra | 47 | 9B, 13mm | 9 blades outside 3-8 range |
| DSC616M-X23 | NOV | 46 | 6B, 16mm | NOV DSC-series, 3-digit literal mm |
| K6M524 | Baker Hughes | 45 | ? | Kymera hybrid bit, non-standard encoding |

### Proposed new cutter code mappings (need user verification)

| Code | Baker/Halliburton (fraction) | Metric (last-digit) | Evidence |
|------|------------------------------|---------------------|----------|
| 6 | 6/8" = 19mm | 16mm | Baker DD604M (67 runs), D605S (65 runs) |
| 8 | 8/8" = 25mm? | 18mm? | Baker T806KS, D806X -- needs verification |
| 9 | N/A | 19mm? | NOV TK59 (49 runs) -- needs verification |

### Models that don't follow encoding conventions

| Model | Manufacturer | Issue | Best Guess |
|-------|-------------|-------|------------|
| A1GRC | Halliburton | No digit encoding | Unknown (MWD tool?) |
| XR+C | Schlumberger | No digit encoding | Unknown (specialty tool?) |
| K6M425/K6M524 | Baker Hughes | Kymera hybrid bit numbering | Non-standard, needs manual mapping |
| U05105 | Ulterra | Product SKU, not encoded | Unknown |
| TKFC6-AZ10 | NOV | Only 1 digit after TKFC prefix | Unknown |

### Cutter digit ambiguities

| Digit | Baker/Halliburton (fraction) | NOV/SLB/Ulterra (metric) | Same result? |
|-------|------------------------------|--------------------------|--------------|
| 3 | 3/8" → ~8mm | 13mm | NO |
| 4 | 4/8" → 13mm | 14mm | NO |
| 5 | 5/8" → 16mm (grouped) | 16mm (grouped from 15) | YES (both → 16mm) |
| 6 | 6/8" → 19mm? | 16mm | NO (needs verification) |
| 7 | 7/8" → 22mm? | 17mm? | ? |
| 8 | 8/8" → 25mm? | 18mm? | ? |
| 9 | N/A | 19mm? | ? |

The ambiguity only matters for 2-digit models where the convention is determined by the model prefix (H* = fraction, TK* = metric). For 3-digit literal-mm models and Baker X0Y models, there's no ambiguity.

> **Cutter size grouping rule (Feb 2026)**: All 15mm values are remapped to 16mm. Baker 5/8" (15.875mm) and metric 15mm/16mm are functionally equivalent and grouped together as 16mm for all equivalent BHA comparisons.

## Updating This Catalog

### Quick update (offset runs only)
1. Run BHA extraction scripts
2. Run `parse_bit_motors.py` to add parsed columns to the CSVs
3. Run `build_bit_catalog.py` to regenerate `bit_catalog.csv`
4. Review the "MODELS NEEDING REVIEW" section in the output

### Full-Corva rescan
1. Run `python full_corva_bit_scan.py --phase1` to re-enumerate wells (if needed)
2. Delete `scan_progress.json` to force a full rescan, or leave it to only process new wells
3. Run `python full_corva_bit_scan.py --phase2` to process all wells
4. Run `python full_corva_bit_scan.py --phase3` to rebuild the catalog
5. Review results and update `parse_bit_motors.py` patterns as needed

## Motor Characterization (Brief)

Motor model strings encode lobe configuration directly as `X/Y` (e.g., "5/6 8.2 stg" = 5 rotor lobes, 6 stator lobes, 8.2 stages). The parser extracts:
- **Lobe config**: regex `(\d)/(\d)` from motor model string
- **RPG band**: from the numeric `motor_rpg` field, binned as lo (<=0.30), mid (0.31-0.45), hi (0.46-0.55), vhi (>0.55)

Motor manufacturer names vary widely for the same power section (e.g., "ProDirectional", "BHA", "KLX", "Altitude", "Patriot" may all supply the same lobe configuration). The lobe config + RPG is more meaningful for grouping than manufacturer.
