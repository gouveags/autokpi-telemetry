#!/usr/bin/env python3
"""
compare_runs.py
---------------
Compare KPIs between setup A and B using a Welch t-test on per-lap metrics.

Inputs:
    - KPIs CSV from compute_kpis.py

Outputs:
    - Markdown summary with means, standard deviations, Welch t-test p-values

Usage:
    python scripts/compare_runs.py --input data/kpis_per_lap.csv --metric lap_time_s --output data/ab_lap_time.md
"""

import argparse
import pandas as pd
import numpy as np

def welch_ttest(a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    ma, mb = a.mean(), b.mean()
    sa2, sb2 = a.var(ddof=1), b.var(ddof=1)
    na, nb = len(a), len(b)
    t = (ma - mb) / np.sqrt(sa2/na + sb2/nb)
    # Welch-Satterthwaite degrees of freedom
    df = (sa2/na + sb2/nb)**2 / ((sa2**2)/((na**2)*(na-1)) + (sb2**2)/((nb**2)*(nb-1)))
    # Two-sided p-value via t CDF approximation using scipy would be better; fallback to survival func with normal approx
    # We'll approximate using the standard normal for simplicity in this lightweight script.
    from math import erf, sqrt
    # Normal approximation (conservative for reasonably large df)
    p_two = 2*(1 - 0.5*(1 + erf(abs(t)/sqrt(2))))
    return t, df, p_two

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--metric", required=True, help="Column in KPIs to compare, e.g., lap_time_s, mean_speed_mps")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    kpis = pd.read_csv(args.input)
    a = kpis[kpis["setup"]=="A"][args.metric].values
    b = kpis[kpis["setup"]=="B"][args.metric].values

    if len(a) < 2 or len(b) < 2:
        raise SystemExit("Need at least two laps per setup for comparison.")

    t, df, p = welch_ttest(a, b)

    md = []
    md.append(f"# A/B Comparison for `{args.metric}`")
    md.append("")
    md.append("| Setup | N | Mean | Std |")
    md.append("|------:|--:|-----:|----:|")
    for setup, arr in [("A", a), ("B", b)]:
        md.append(f"| {setup} | {len(arr)} | {arr.mean():.3f} | {arr.std(ddof=1):.3f} |")
    md.append("")
    md.append(f"Welch t-test: t = {t:.3f}, df ≈ {df:.1f}, p ≈ {p:.4f} (normal approx).")
    md.append("")
    with open(args.output, "w") as f:
        f.write("\n".join(md))
    print(f"Wrote A/B comparison for {args.metric} to {args.output}")

if __name__ == "__main__":
    main()
