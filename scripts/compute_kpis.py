#!/usr/bin/env python3
"""
compute_kpis.py
---------------
Compute per-lap KPIs from a telemetry CSV.

Inputs:
    - Telemetry CSV with columns:
        timestamp, car_id, lap_id, setup, sample_idx, speed_mps, rpm, throttle_pct,
        brake_pct, gear, lateral_g, longitudinal_g, fluid_temp_c, sensor_fault

Outputs:
    - CSV with per-lap KPIs: kpis_per_lap.csv

Usage:
    python scripts/compute_kpis.py --input data/synthetic_telemetry.csv --output data/kpis_per_lap.csv
"""

import argparse
import pandas as pd
import numpy as np


def pct(series, threshold, op=">="):
    if len(series) == 0:
        return 0.0
    if op == ">=":
        return (series >= threshold).mean()
    elif op == ">":
        return (series > threshold).mean()
    elif op == "<=":
        return (series <= threshold).mean()
    elif op == "<":
        return (series < threshold).mean()
    else:
        raise ValueError("Invalid op")


def count_gear_changes(gears):
    if len(gears) <= 1:
        return 0
    # count transitions
    return (gears.values[1:] != gears.values[:-1]).sum()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Input telemetry CSV")
    ap.add_argument("--output", required=True, help="Output per-lap KPIs CSV")
    ap.add_argument(
        "--lateral_g_threshold",
        type=float,
        default=1.8,
        help="Exceedance threshold for lateral g",
    )
    ap.add_argument(
        "--overspeed_threshold",
        type=float,
        default=65.0,
        help="Overspeed threshold (m/s)",
    )
    args = ap.parse_args()

    df = pd.read_csv(args.input)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="ISO8601")

    kpi_rows = []
    for (lap_id, setup), g in df.groupby(["lap_id", "setup"], sort=True):  # type: ignore
        lap_time = (g["timestamp"].max() - g["timestamp"].min()).total_seconds()
        mean_speed = g["speed_mps"].mean()
        p95_speed = g["speed_mps"].quantile(0.95)
        throttle_duty = pct(g["throttle_pct"], 80, op=">=")
        brake_duty = pct(g["brake_pct"], 10, op=">=")
        max_lateral_g = g["lateral_g"].max()
        gear_changes = count_gear_changes(g["gear"])
        overspeed_events = (g["speed_mps"] > args.overspeed_threshold).sum()
        lat_g_exceed = (g["lateral_g"] > args.lateral_g_threshold).sum()

        kpi_rows.append(
            {
                "lap_id": lap_id,
                "setup": setup,
                "lap_time_s": round(float(lap_time), 2),
                "mean_speed_mps": round(float(mean_speed), 3),
                "p95_speed_mps": round(float(p95_speed), 3),
                "throttle_duty_pct": round(100 * float(throttle_duty), 1),
                "brake_duty_pct": round(100 * float(brake_duty), 1),
                "max_lateral_g": round(float(max_lateral_g), 3),
                "gear_changes": int(gear_changes),
                "overspeed_events": int(overspeed_events),
                "lateral_g_exceed_count": int(lat_g_exceed),
            }
        )

    out = pd.DataFrame(kpi_rows).sort_values(["setup", "lap_id"])
    out.to_csv(args.output, index=False)
    print(f"Wrote KPIs to {args.output}")


if __name__ == "__main__":
    main()
