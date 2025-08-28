#!/usr/bin/env python3
"""
count_exceedances.py
--------------------
Counts exceedances for a chosen channel and threshold per lap.

Usage:
    python scripts/count_exceedances.py --input data/synthetic_telemetry.csv --output data/exceedances.csv \
        --channel lateral_g --threshold 1.8
"""

import argparse
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--channel", required=True, help="Column to threshold, e.g., lateral_g, speed_mps")
    ap.add_argument("--threshold", type=float, required=True)
    ap.add_argument("--op", default=">", choices=[">",">=","<","<="])
    args = ap.parse_args()

    df = pd.read_csv(args.input, parse_dates=["timestamp"])

    rows = []
    for (lap_id, setup), g in df.groupby(["lap_id","setup"], sort=True):
        if args.op == ">":
            count = (g[args.channel] > args.threshold).sum()
        elif args.op == ">=":
            count = (g[args.channel] >= args.threshold).sum()
        elif args.op == "<":
            count = (g[args.channel] < args.threshold).sum()
        elif args.op == "<=":
            count = (g[args.channel] <= args.threshold).sum()
        else:
            raise ValueError("Invalid op")
        rows.append({
            "lap_id": lap_id, "setup": setup,
            "channel": args.channel, "op": args.op,
            "threshold": args.threshold, "count": int(count)
        })

    out = pd.DataFrame(rows).sort_values(["channel","setup","lap_id"])
    out.to_csv(args.output, index=False)
    print(f"Wrote exceedances to {args.output}")

if __name__ == "__main__":
    main()
