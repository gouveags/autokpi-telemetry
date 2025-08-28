#!/usr/bin/env python3
"""
regression.py
-------------
Fit a simple OLS regression at the lap level:
    lap_time_s ~ mean_speed_mps + throttle_duty_pct + brake_duty_pct

Inputs:
    - KPIs CSV from compute_kpis.py

Outputs:
    - Text summary with coefficients and R^2

Usage:
    python scripts/regression.py --input data/kpis_per_lap.csv --output data/regression.txt
"""

import argparse
import pandas as pd
import numpy as np

def ols(X, y):
    # Add intercept
    X = np.column_stack([np.ones(len(X)), X])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ beta
    resid = y - yhat
    ss_res = (resid**2).sum()
    ss_tot = ((y - y.mean())**2).sum()
    r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0.0
    return beta, r2

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    k = pd.read_csv(args.input)
    # Prepare features
    X = k[["mean_speed_mps", "throttle_duty_pct", "brake_duty_pct"]].values.astype(float)
    # scale throttle/brake to [0,1] for interpretability
    X[:,1] /= 100.0
    X[:,2] /= 100.0
    y = k["lap_time_s"].values.astype(float)

    beta, r2 = ols(X, y)
    # beta: [intercept, b_speed, b_throttle, b_brake]
    txt = []
    txt.append("OLS Regression: lap_time_s ~ mean_speed_mps + throttle_duty_pct + brake_duty_pct")
    txt.append("")
    txt.append(f"Intercept: {beta[0]:.4f}")
    txt.append(f"mean_speed_mps coef: {beta[1]:.4f}")
    txt.append(f"throttle_duty (0-1) coef: {beta[2]:.4f}")
    txt.append(f"brake_duty (0-1) coef: {beta[3]:.4f}")
    txt.append(f"R^2: {r2:.4f}")
    with open(args.output, "w") as f:
        f.write("\n".join(txt))
    print(f"Wrote regression summary to {args.output}")

if __name__ == "__main__":
    main()
