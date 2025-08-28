# Usage

This document shows how to use each script and what to expect from the outputs.

## 1) `compute_kpis.py`

**Purpose:** Compute per-lap KPIs from raw telemetry.

**KPIs produced:**

- `lap_time_s`: max(timestamp) - min(timestamp) per lap
- `mean_speed_mps`, `p95_speed_mps`
- `throttle_duty_pct`: % of samples with throttle >= 80%
- `brake_duty_pct`: % of samples with brake >= 10%
- `max_lateral_g`
- `gear_changes`: count of transitions between gear values
- `overspeed_events`: count of samples with `speed_mps` > threshold
- `lateral_g_exceed_count`: count of samples with `lateral_g` > threshold

**Run:**

```bash
python scripts/compute_kpis.py --input data/synthetic_telemetry.csv --output data/kpis_per_lap.csv
```

---

## 2) `detect_events.py`

**Purpose:** Row-level event detection for overspeed, lateral-g exceedances, and sensor faults.

**Run:**

```bash
python scripts/detect_events.py --input data/synthetic_telemetry.csv --output data/events.csv   --overspeed_threshold 65 --lateral_g_threshold 1.8
```

**Output columns:** `timestamp`, `lap_id`, `setup`, `event`, `value`, `threshold`

---

## 3) `count_exceedances.py`

**Purpose:** Per-lap exceedance counts for any numeric channel.

**Run:**

```bash
python scripts/count_exceedances.py --input data/synthetic_telemetry.csv --output data/exceedances.csv   --channel lateral_g --threshold 1.8 --op >
```

**Output columns:** `lap_id`, `setup`, `channel`, `op`, `threshold`, `count`

---

## 4) `compare_runs.py`

**Purpose:** Compare a per-lap metric between setups A and B using a Welch t-test (p-value approximated with normal CDF).

**Run:**

```bash
python scripts/compare_runs.py --input data/kpis_per_lap.csv --metric lap_time_s --output data/ab_lap_time.md
python scripts/compare_runs.py --input data/kpis_per_lap.csv --metric mean_speed_mps --output data/ab_mean_speed.md
```

**Output:** Markdown summary with table, t-statistic, df (approx), and p-value (approx).

---

## 5) `regression.py`

**Purpose:** Simple OLS on lap-level KPIs:

```
lap_time_s ~ mean_speed_mps + throttle_duty_pct + brake_duty_pct
```

**Run:**

```bash
python scripts/regression.py --input data/kpis_per_lap.csv --output data/regression.txt
```

**Output:** Text file with coefficients and R².

---

## 6) `generate_report.py`

**Purpose:** Combine KPIs, A/B results, and regression summary into a single Markdown report.

**Run:**

```bash
python scripts/generate_report.py --kpis data/kpis_per_lap.csv   --ab1 data/ab_lap_time.md --ab2 data/ab_mean_speed.md --reg data/regression.txt   --output data/report.md
```

**Output:** `data/report.md` with a compact, human-readable summary.
