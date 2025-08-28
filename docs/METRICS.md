# Metrics

**Lap KPIs** (per lap):
- **lap_time_s**: duration of lap in seconds.
- **mean_speed_mps**: average speed over lap.
- **p95_speed_mps**: 95th percentile of speed over lap.
- **throttle_duty_pct**: percentage of samples with throttle ≥ 80%.
- **brake_duty_pct**: percentage of samples with brake ≥ 10%.
- **max_lateral_g**: maximum lateral g observed in the lap.
- **gear_changes**: number of discrete gear transitions across samples.
- **overspeed_events**: count of samples with speed > threshold (default 65 m/s).
- **lateral_g_exceed_count**: count of samples with lateral_g > threshold (default 1.8 g).

**Event Types**:
- **overspeed**: `speed_mps` > configurable threshold.
- **lateral_g_exceed**: `lateral_g` > configurable threshold.
- **sensor_fault**: row flagged as fault (1).

**A/B**:
- Welch t-test between setups A and B on a selected per-lap metric.
- Reports mean, std, t, df≈, p (normal approx).

**Regression**:
- OLS using numpy least squares, with intercept.
- Response: `lap_time_s`.
- Predictors: `mean_speed_mps`, `throttle_duty_pct`, `brake_duty_pct` (duty cycles scaled to 0–1).
