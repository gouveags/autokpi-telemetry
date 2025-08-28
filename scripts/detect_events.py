#!/usr/bin/env python3
"""
detect_events.py
----------------
Detects simple events from telemetry: overspeed, high lateral g, sensor faults.

Usage:
    python scripts/detect_events.py --input data/synthetic_telemetry.csv --output data/events.csv \
        --overspeed_threshold 65 --lateral_g_threshold 1.8
"""

import argparse
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--overspeed_threshold", type=float, default=65.0)
    ap.add_argument("--lateral_g_threshold", type=float, default=1.8)
    args = ap.parse_args()

    df = pd.read_csv(args.input, parse_dates=["timestamp"])

    events = []
    for _, r in df.iterrows():
        # Overspeed
        if r["speed_mps"] > args.overspeed_threshold:
            events.append({
                "timestamp": r["timestamp"],
                "lap_id": int(r["lap_id"]),
                "setup": r["setup"],
                "event": "overspeed",
                "value": float(r["speed_mps"]),
                "threshold": args.overspeed_threshold
            })
        # Lateral G exceed
        if r["lateral_g"] > args.lateral_g_threshold:
            events.append({
                "timestamp": r["timestamp"],
                "lap_id": int(r["lap_id"]),
                "setup": r["setup"],
                "event": "lateral_g_exceed",
                "value": float(r["lateral_g"]),
                "threshold": args.lateral_g_threshold
            })
        # Sensor fault
        if int(r["sensor_fault"]) == 1:
            events.append({
                "timestamp": r["timestamp"],
                "lap_id": int(r["lap_id"]),
                "setup": r["setup"],
                "event": "sensor_fault",
                "value": 1,
                "threshold": 1
            })

    evdf = pd.DataFrame(events).sort_values(["lap_id","timestamp"])
    evdf.to_csv(args.output, index=False)
    print(f"Wrote events to {args.output}")

if __name__ == "__main__":
    main()
