# Data Dictionary

This document explains all the data channels (columns) present in the telemetry dataset and what they represent.

## Input Data Structure

The synthetic telemetry dataset contains racing car sensor data sampled at 5 Hz (5 times per second) across 8 laps with 2 different car setups (A and B).

### File: `data/synthetic_telemetry.csv`

| Column | Type | Description | Units | Range/Values |
|--------|------|-------------|-------|--------------|
| `timestamp` | datetime | ISO8601 timestamp of the measurement | ISO8601 format | 2024-01-01T12:00:00.000000 |
| `car_id` | string | Unique identifier for the vehicle | - | car_01 |
| `lap_id` | integer | Sequential lap number | - | 1, 2, 3, 4, 5, 6, 7, 8 |
| `setup` | string | Car configuration identifier | - | A, B |
| `sample_idx` | integer | Sample index within the lap | - | 0, 1, 2, ..., 299 |
| `speed_mps` | float | Vehicle speed | meters per second | 0.0 - 70.0+ |
| `rpm` | integer | Engine revolutions per minute | RPM | 8000 - 12000 |
| `throttle_pct` | float | Throttle pedal position | percentage | 0.0 - 100.0 |
| `brake_pct` | float | Brake pedal pressure | percentage | 0.0 - 100.0 |
| `gear` | integer | Current gear position | gear number | 1, 2, 3, 4, 5, 6 |
| `lateral_g` | float | Lateral acceleration (side-to-side) | g-force | -3.0 to +3.0 |
| `longitudinal_g` | float | Longitudinal acceleration (forward/backward) | g-force | -3.0 to +3.0 |
| `fluid_temp_c` | float | Engine fluid temperature | Celsius | 70.0 - 90.0 |
| `sensor_fault` | integer | Sensor fault indicator | binary | 0 (normal), 1 (fault) |

## Data Channel Explanations

### **Timestamp (`timestamp`)**
- **What it is**: Precise moment when the measurement was taken
- **Why it matters**: Essential for calculating lap times, event timing, and temporal analysis
- **Format**: ISO8601 with microsecond precision (e.g., `2024-01-01T12:00:00.200000`)

### **Car ID (`car_id`)**
- **What it is**: Unique identifier for the vehicle being monitored
- **Why it matters**: Allows tracking multiple vehicles in the same dataset
- **Current value**: Fixed as `car_01` in this synthetic dataset

### **Lap ID (`lap_id`)**
- **What it is**: Sequential number identifying each completed lap
- **Why it matters**: Enables per-lap analysis and comparison between different laps
- **Range**: 1-8 (4 laps with setup A, 4 laps with setup B)

### **Setup (`setup`)**
- **What it is**: Car configuration identifier for A/B testing
- **Why it matters**: Enables comparison between different car configurations
- **Values**:
  - `A`: First car setup configuration
  - `B`: Second car setup configuration (modified from A)

### **Sample Index (`sample_idx`)**
- **What it is**: Sequential number of the measurement within each lap
- **Why it matters**: Helps identify data quality issues and ensures proper ordering
- **Range**: 0-299 (300 samples per lap at 5 Hz = 60 seconds per lap)

### **Speed (`speed_mps`)**
- **What it is**: Vehicle velocity in meters per second
- **Why it matters**: Core performance metric, used for lap time calculations and overspeed detection
- **Conversion**: 1 m/s ≈ 3.6 km/h ≈ 2.24 mph
- **Typical range**: 0-70+ m/s depending on track layout

### **RPM (`rpm`)**
- **What it is**: Engine rotational speed in revolutions per minute
- **Why it matters**: Indicates engine performance, gear selection efficiency, and power delivery
- **Typical range**: 8000-12000 RPM for racing engines
- **Redline**: Usually around 12000 RPM

### **Throttle (`throttle_pct`)**
- **What it is**: Throttle pedal position as a percentage of full opening
- **Why it matters**: Indicates driver aggressiveness, power application, and fuel consumption
- **Range**: 0% (closed) to 100% (fully open)
- **Threshold**: 80%+ considered "high throttle" for duty cycle calculations

### **Brake (`brake_pct`)**
- **What it is**: Brake pedal pressure as a percentage of maximum braking force
- **Why it matters**: Shows braking zones, corner entry speeds, and driver technique
- **Range**: 0% (no brake) to 100% (maximum braking)
- **Threshold**: 10%+ considered "braking" for duty cycle calculations

### **Gear (`gear`)**
- **What it is**: Current transmission gear position
- **Why it matters**: Indicates driving efficiency, power delivery optimization, and driver skill
- **Range**: 1-6 (1st through 6th gear)
- **Analysis**: Gear changes are counted to measure driving smoothness

### **Lateral G (`lateral_g`)**
- **What it is**: Side-to-side acceleration force in g-force units
- **Why it matters**: Indicates cornering performance, tire grip, and driving technique
- **Range**: -3.0 to +3.0 g
- **Positive values**: Acceleration to the right
- **Negative values**: Acceleration to the left
- **Threshold**: 1.8g+ considered "high lateral force" for exceedance detection

### **Longitudinal G (`longitudinal_g`)**
- **What it is**: Forward/backward acceleration force in g-force units
- **Why it matters**: Shows acceleration and braking performance
- **Range**: -3.0 to +3.0 g
- **Positive values**: Forward acceleration
- **Negative values**: Braking/deceleration

### **Fluid Temperature (`fluid_temp_c`)**
- **What it is**: Engine coolant/oil temperature in Celsius
- **Why it matters**: Engine health monitoring and thermal management
- **Range**: 70-90°C (normal operating range)
- **Warning**: Values outside this range could indicate cooling system issues

### **Sensor Fault (`sensor_fault`)**
- **What it is**: Binary indicator of sensor malfunction
- **Why it matters**: Data quality control and system health monitoring
- **Values**:
  - `0`: Normal operation
  - `1`: Sensor fault detected
- **Impact**: Faulty data should be filtered out of analysis

## Data Quality Notes

- **Sampling rate**: 5 Hz (5 samples per second)
- **Lap duration**: ~60 seconds per lap
- **Total samples**: 2,400 samples (8 laps × 300 samples)
- **Missing data**: None in synthetic dataset
- **Timestamp precision**: Microsecond accuracy
- **Coordinate system**: Right-hand rule for lateral/longitudinal forces

## Channel Categories

### **Performance Metrics**
- `speed_mps`, `rpm`, `lap_time_s`

### **Driver Inputs**
- `throttle_pct`, `brake_pct`, `gear`

### **Vehicle Dynamics**
- `lateral_g`, `longitudinal_g`

### **System Health**
- `fluid_temp_c`, `sensor_fault`

### **Metadata**
- `timestamp`, `car_id`, `lap_id`, `setup`, `sample_idx`
