#!/usr/bin/env python3
"""
generate_report.py
------------------
Generates a short Markdown report aggregating KPIs and A/B results.

Assumes the following files exist:
    - data/kpis_per_lap.csv (from compute_kpis.py)
    - data/ab_lap_time.md (from compare_runs.py --metric lap_time_s)
    - data/ab_mean_speed.md (from compare_runs.py --metric mean_speed_mps)

Usage:
    python scripts/generate_report.py --kpis data/kpis_per_lap.csv \
        --ab1 data/ab_lap_time.md --ab2 data/ab_mean_speed.md --reg data/regression.txt \
        --output data/report.md
"""

import argparse
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kpis", required=True)
    ap.add_argument("--ab1", required=True, help="A/B result markdown (e.g., lap_time_s)")
    ap.add_argument("--ab2", required=True, help="Another A/B result markdown (e.g., mean_speed_mps)")
    ap.add_argument("--reg", required=True, help="Regression text summary")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    k = pd.read_csv(args.kpis)

    # Load A/B markdowns and regression text
    with open(args.ab1, "r") as f:
        ab1 = f.read()
    with open(args.ab2, "r") as f:
        ab2 = f.read()
    with open(args.reg, "r") as f:
        reg = f.read()

    md = []
    md.append("# AutoKPI Telemetry — Synthetic Report")
    md.append("")
    md.append("## Per-lap KPIs (excerpt)")
    md.append("")
    md.append(k.head(10).to_markdown(index=False))
    md.append("")
    md.append("## A/B — Lap Time")
    md.append("")
    md.append(ab1)
    md.append("")
    md.append("## A/B — Mean Speed")
    md.append("")
    md.append(ab2)
    md.append("")
    md.append("## Regression Summary")
    md.append("")
    md.append("```")
    md.append(reg)
    md.append("```")

    with open(args.output, "w") as f:
        f.write("\n".join(md))
    print(f"Wrote report to {args.output}")

if __name__ == "__main__":
    main()
