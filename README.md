# AutoKPI Telemetry

*A lightweight open-source toolkit to turn raw sensor logs into basic KPIs (laps, events & limits).*

This repository contains a **synthetic dataset** and a set of **simple Python scripts** to compute basic KPIs from telemetry logs.
It mirrors a minimal workflow inspired by real engineering needs (e.g., lap segmentation, KPI calculation, event detection, exceedances, A/B comparison, and simple regression), while keeping everything public and anonymized.

> **Note**: The public repo and docs are in **English** to increase reach and reuse by the open-source community.

## Project Structure

```
autokpi-telemetry/
├── data/
│   └── synthetic_telemetry.csv
├── scripts/
│   ├── compute_kpis.py
│   ├── detect_events.py
│   ├── count_exceedances.py
│   ├── compare_runs.py
│   ├── regression.py
│   └── generate_report.py
└── docs/
    ├── USAGE.md
    ├── METRICS.md
    └── CHANGELOG.md
```

## Quickstart

Create a Python 3.10+ environment and install dependencies:

```bash
pip install pandas numpy
```

Run the full minimal pipeline:

```bash
# 1) Compute per-lap KPIs
python scripts/compute_kpis.py --input data/synthetic_telemetry.csv --output data/kpis_per_lap.csv

# 2) Detect simple events
python scripts/detect_events.py --input data/synthetic_telemetry.csv --output data/events.csv   --overspeed_threshold 65 --lateral_g_threshold 1.8

# 3) Count exceedances (example: lateral_g > 1.8)
python scripts/count_exceedances.py --input data/synthetic_telemetry.csv --output data/exceedances.csv   --channel lateral_g --threshold 1.8 --op >

# 4) A/B comparisons on lap KPIs
python scripts/compare_runs.py --input data/kpis_per_lap.csv --metric lap_time_s --output data/ab_lap_time.md
python scripts/compare_runs.py --input data/kpis_per_lap.csv --metric mean_speed_mps --output data/ab_mean_speed.md

# 5) Regression (lap_time vs. mean speed + duty cycles)
python scripts/regression.py --input data/kpis_per_lap.csv --output data/regression.txt

# 6) Aggregate report
python scripts/generate_report.py --kpis data/kpis_per_lap.csv   --ab1 data/ab_lap_time.md --ab2 data/ab_mean_speed.md --reg data/regression.txt   --output data/report.md
```

Outputs will be written to the `data/` folder.

## Dataset (synthetic)

- 8 laps (4 with setup **A**, 4 with setup **B**)
- 300 samples per lap (~60 s @ 5 Hz)
- Columns:
  - `timestamp` (ISO8601), `car_id`, `lap_id`, `setup` (A/B), `sample_idx`
  - `speed_mps`, `rpm`, `throttle_pct`, `brake_pct`, `gear`
  - `lateral_g`, `longitudinal_g`, `fluid_temp_c`, `sensor_fault`

## License

MIT — see `LICENSE`.
