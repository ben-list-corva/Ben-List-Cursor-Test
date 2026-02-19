# Formation roadmap methodology (client-ready)

We built the limits table from Corva `wits.summary-1ft` using two contiguous intervals:
- Asset `18398736`: Intermediate 12.25 in section from 2851 ft through the Travis Peak Middle cutoff.
- Asset `64628631`: from below Travis Peak Middle through the remainder of the run.

Each 1-ft record was mapped to formation using `data.formations` tops, then statistics were calculated per formation:
- **ROP limit**: `P95(ROP) * 1.3`, rounded to nearest 10 ft/hr.
- **Diff Press limit**: `P95(diff_press) * 1.3`, rounded to nearest 10 psi.
- **WOB**: `P95(weight_on_bit)`, rounded down to whole klbf.
- **Rotary RPM**: median rotary RPM, rounded to nearest 5 RPM.

Data quality controls:
- Included only drilling states (`Rotary Drilling`, `Slide Drilling`).
- Derived ROP from `timestamp_max - timestamp_min` and applied a 5-500 ft/hr sanity filter.
- Used *_median/*_mean/*_max fallback hierarchy for WOB and RPM when needed in summary-1ft records.
