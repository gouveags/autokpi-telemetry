# AutoKPI Telemetry — Synthetic Report

## Per-lap KPIs (excerpt)

|   lap_id | setup   |   lap_time_s |   mean_speed_mps |   p95_speed_mps |   throttle_duty_pct |   brake_duty_pct |   max_lateral_g |   gear_changes |   overspeed_events |   lateral_g_exceed_count |
|---------:|:--------|-------------:|-----------------:|----------------:|--------------------:|-----------------:|----------------:|---------------:|-------------------:|-------------------------:|
|        1 | A       |         58.8 |           54.487 |          62.812 |                18.3 |             71.5 |           2.095 |             34 |                  0 |                        9 |
|        2 | A       |         61.2 |           52.875 |          61.052 |                22.8 |             73.9 |           2.109 |             69 |                  0 |                       11 |
|        3 | A       |         56.4 |           49.716 |          58.035 |                18   |             72.4 |           2.049 |             18 |                  0 |                       12 |
|        4 | A       |         58.8 |           52.064 |          60.44  |                15.9 |             73.6 |           2.4   |             55 |                  0 |                       13 |
|        5 | B       |         61.6 |           56.958 |          65.361 |                22   |             73.1 |           2.276 |             22 |                 22 |                       11 |
|        6 | B       |         61.2 |           52.766 |          61.153 |                19.9 |             69.1 |           2.362 |             64 |                  0 |                       11 |
|        7 | B       |         55.8 |           59.024 |          67.19  |                19.6 |             67.9 |           2.276 |             28 |                 62 |                       13 |
|        8 | B       |         57.8 |           51.702 |          59.822 |                16.2 |             68.3 |           2.451 |             37 |                  0 |                       17 |

## A/B — Lap Time

# A/B Comparison for `lap_time_s`

| Setup | N | Mean | Std |
|------:|--:|-----:|----:|
| A | 4 | 58.800 | 1.960 |
| B | 4 | 59.100 | 2.783 |

Welch t-test: t = -0.176, df ≈ 5.4, p ≈ 0.8601 (normal approx).


## A/B — Mean Speed

# A/B Comparison for `mean_speed_mps`

| Setup | N | Mean | Std |
|------:|--:|-----:|----:|
| A | 4 | 52.285 | 1.987 |
| B | 4 | 55.112 | 3.457 |

Welch t-test: t = -1.418, df ≈ 4.8, p ≈ 0.1562 (normal approx).


## Regression Summary

```
OLS Regression: lap_time_s ~ mean_speed_mps + throttle_duty_pct + brake_duty_pct

Intercept: 42.5064
mean_speed_mps coef: -0.1506
throttle_duty (0-1) coef: 55.7398
brake_duty (0-1) coef: 19.5032
R^2: 0.4573
```