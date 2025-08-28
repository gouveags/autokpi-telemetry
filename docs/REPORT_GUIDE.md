# Report Guide

This document explains in detail what each final report contains and how to interpret the results to understand what's happening with your racing telemetry data.

## Overview

The AutoKPI Telemetry pipeline generates several reports that provide different perspectives on your racing performance. Each report serves a specific purpose and together they give you a complete picture of your car's behavior and driver performance.

## 1. KPIs Per Lap Report (`data/kpis_per_lap.csv`)

**What it is**: A comprehensive summary of key performance indicators calculated for each individual lap.

**What it tells you**: How each lap performed across multiple dimensions - speed, driver inputs, vehicle dynamics, and efficiency.

### **Columns Explained:**

#### **Lap Identification**
- `lap_id`: Which lap this data represents (1-8)n
- `setup`: Car configuration used (A or B)

#### **Performance Metrics**
- `lap_time_s`: **Total lap time in seconds**
  - **What it means**: How fast you completed the lap
  - **How to interpret**: Lower is better. Compare between setups to see which configuration is faster
  - **Example**: 58.8s means the lap took 58.8 seconds to complete

- `mean_speed_mps`: **Average speed throughout the lap**
  - **What it means**: Overall pace maintained during the lap
  - **How to interpret**: Higher is generally better, but depends on track layout
  - **Example**: 54.487 m/s ≈ 196 km/h average speed

- `p95_speed_mps`: **95th percentile speed**
  - **What it means**: Speed you maintained for 95% of the lap (excluding top 5% speeds)
  - **How to interpret**: More consistent than mean, shows your sustained pace
  - **Example**: 62.812 m/s means you were above 62.8 m/s for most of the lap

#### **Driver Input Analysis**
- `throttle_duty_pct`: **Percentage of time with high throttle (≥80%)**
  - **What it means**: How aggressively you're applying power
  - **How to interpret**:
    - **High values (20%+)**: Aggressive driving, lots of full-throttle sections
    - **Low values (<15%)**: Conservative driving, more partial throttle
  - **Example**: 18.3% means you were at 80%+ throttle for 18.3% of the lap

- `brake_duty_pct`: **Percentage of time braking (≥10%)**
  - **What it means**: How much time you spend in braking zones
  - **How to interpret**:
    - **High values (70%+)**: Many braking zones, technical track
    - **Low values (<60%)**: Few braking zones, high-speed track
  - **Example**: 71.5% means you were braking for 71.5% of the lap

#### **Vehicle Dynamics**
- `max_lateral_g`: **Maximum lateral acceleration experienced**
  - **What it means**: Highest cornering force during the lap
  - **How to interpret**:
    - **High values (2.0g+)**: Aggressive cornering, high tire grip
    - **Low values (<1.5g)**: Conservative cornering, or low-grip conditions
  - **Example**: 2.095g means you experienced 2.095 times Earth's gravity in cornering

- `gear_changes`: **Number of gear shifts during the lap**
  - **What it means**: How smooth your driving is
  - **How to interpret**:
    - **High values (50+)**: Many gear changes, technical track or aggressive driving
    - **Low values (<30)**: Few gear changes, smooth driving or simple track
  - **Example**: 34 gear changes means you shifted 34 times during the lap

#### **Event Counts**
- `overspeed_events`: **Number of times you exceeded speed threshold**
  - **What it means**: How often you went above the safety speed limit
  - **How to interpret**: Lower is better for safety, but may indicate conservative driving
  - **Example**: 0 means you never exceeded the 65 m/s threshold

- `lateral_g_exceed_count`: **Number of times you exceeded lateral G threshold**
  - **What it means**: How often you experienced high cornering forces
  - **How to interpret**:
    - **High values (10+)**: Aggressive cornering, pushing limits
    - **Low values (<5)**: Conservative cornering, staying within comfort zone
  - **Example**: 9 means you exceeded 1.8g lateral force 9 times during the lap

## 2. Events Report (`data/events.csv`)

**What it is**: Detailed log of specific events that occurred during your laps.

**What it tells you**: Exactly when and where important events happened, allowing you to analyze specific moments.

### **Columns Explained:**
- `timestamp`: When the event occurred
- `lap_id`: Which lap the event happened in
- `setup`: Car configuration used
- `event`: Type of event detected
- `value`: Actual measured value when event occurred
- `threshold`: Threshold value that was exceeded

### **Event Types:**

#### **Overspeed Events**
- **What it means**: You exceeded the speed safety threshold (65 m/s)
- **Why it matters**: Safety concern, may indicate pushing too hard
- **Example**: `overspeed, 67.2, 65` means you hit 67.2 m/s when 65 m/s was the limit

#### **Lateral G Exceedances**
- **What it means**: You experienced cornering forces above the threshold (1.8g)
- **Why it matters**: Shows aggressive cornering, may indicate pushing tire limits
- **Example**: `lateral_g_exceed, 1.806, 1.8` means you hit 1.806g when 1.8g was the threshold

#### **Sensor Faults**
- **What it means**: Data quality issues detected
- **Why it matters**: May indicate sensor problems or data corruption
- **Example**: `sensor_fault, 1, 0` means sensor fault detected when it should be 0

## 3. Exceedances Report (`data/exceedances.csv`)

**What it is**: Summary count of how many times each lap exceeded specific thresholds.

**What it tells you**: Which laps had the most extreme behavior and how setups compare.

### **Columns Explained:**
- `lap_id`: Which lap
- `setup`: Car configuration
- `channel`: What was measured (e.g., lateral_g)
- `op`: Comparison operator (e.g., >)
- `threshold`: Value that was exceeded
- `count`: How many times it happened

### **How to Interpret:**
- **High counts**: More aggressive driving or pushing limits
- **Low counts**: More conservative driving or staying within comfort zone
- **Setup differences**: Compare A vs B to see which configuration allows more aggressive driving

## 4. A/B Comparison Reports

**What it is**: Statistical comparison between car setups A and B for specific metrics.

**What it tells you**: Whether changing the car setup actually made a measurable difference.

### **Example Report Structure:**
```
# A/B Comparison for `lap_time_s`

| Setup | N | Mean | Std |
|------:|--:|-----:|----:|
| A | 4 | 58.800 | 1.960 |
| B | 4 | 59.100 | 2.783 |

Welch t-test: t = -0.176, df ≈ 5.4, p ≈ 0.8601 (normal approx).
```

### **How to Interpret:**

#### **Sample Size (N)**
- **What it means**: How many laps were analyzed for each setup
- **Example**: 4 laps each means you have good statistical power

#### **Mean Values**
- **What it means**: Average performance for each setup
- **Example**: Setup A averaged 58.8s, Setup B averaged 59.1s
- **Interpretation**: Setup A was slightly faster on average

#### **Standard Deviation (Std)**
- **What it means**: How consistent the performance was
- **Example**: Setup A: 1.96s, Setup B: 2.78s
- **Interpretation**: Setup A was more consistent (lower variation)

#### **Statistical Test Results**
- **t-statistic**: How different the means are (higher absolute value = more different)
- **degrees of freedom (df)**: Statistical power of the test
- **p-value**: Probability that the difference occurred by chance
  - **p < 0.05**: Statistically significant difference
  - **p > 0.05**: No significant difference (difference could be random)

### **Example Interpretation:**
- **Setup A**: Faster (58.8s vs 59.1s) and more consistent (1.96s vs 2.78s std)
- **Statistical significance**: p = 0.8601 > 0.05, so the difference is NOT statistically significant
- **Conclusion**: Setup A appears slightly better, but the difference could be due to random variation

## 5. Regression Analysis Report (`data/regression.txt`)

**What it is**: Mathematical model showing how different factors affect lap time.

**What it tells you**: Which aspects of your driving have the biggest impact on performance.

### **Report Structure:**
```
OLS Regression: lap_time_s ~ mean_speed_mps + throttle_duty_pct + brake_duty_pct

Intercept: 42.5064
mean_speed_mps coef: -0.1506
throttle_duty (0-1) coef: 55.7398
brake_duty (0-1) coef: 19.5032
```

### **How to Interpret:**

#### **Model Equation**
- **Response variable**: `lap_time_s` (what we're trying to predict)
- **Predictors**: `mean_speed_mps`, `throttle_duty_pct`, `brake_duty_pct`

#### **Coefficients**
- **Intercept (42.5064)**: Base lap time when all predictors are zero
- **mean_speed_mps (-0.1506)**: For every 1 m/s increase in average speed, lap time decreases by 0.15 seconds
- **throttle_duty (55.7398)**: For every 1% increase in throttle duty cycle, lap time increases by 0.56 seconds
- **brake_duty (19.5032)**: For every 1% increase in brake duty cycle, lap time increases by 0.20 seconds

#### **Practical Interpretation**
- **Speed impact**: Higher average speed = faster lap times (negative coefficient)
- **Throttle impact**: More aggressive throttle = slower lap times (positive coefficient)
- **Brake impact**: More braking = slower lap times (positive coefficient)

#### **Why This Happens**
- **Speed**: Higher speed directly reduces lap time
- **Throttle**: Aggressive throttle may indicate technical sections where you can't maintain high speed
- **Brake**: More braking zones mean more time spent slowing down

## 6. Final Consolidated Report (`data/report.md`)

**What it is**: Complete summary combining all the above analyses into one comprehensive document.

**What it tells you**: The complete picture of your performance across all dimensions.

### **What's Included:**
1. **KPIs table**: All lap-by-lap metrics in one view
2. **A/B comparisons**: Statistical analysis of setup differences
3. **Regression insights**: What factors most affect your lap time
4. **Summary statistics**: Key takeaways and recommendations

## How to Use These Reports

### **For Setup Optimization:**
1. Look at A/B comparisons to see which setup performs better
2. Check if differences are statistically significant
3. Consider consistency (standard deviation) alongside performance

### **For Driver Improvement:**
1. Analyze throttle and brake duty cycles
2. Look for patterns in gear changes
3. Identify laps with extreme lateral G forces

### **For Safety Analysis:**
1. Monitor overspeed events
2. Check lateral G exceedances
3. Review sensor fault patterns

### **For Performance Tuning:**
1. Use regression analysis to identify biggest performance factors
2. Focus training on areas with highest impact
3. Balance speed vs. consistency based on your goals

## Key Performance Indicators to Watch

### **Green Zone (Good Performance):**
- Lap times: Decreasing trend
- Mean speed: Increasing trend
- Lateral G: High but controlled (1.5-2.0g)
- Gear changes: Appropriate for track complexity

### **Yellow Zone (Monitor):**
- High brake duty (>80%)
- Frequent overspeed events
- Inconsistent lap times (high std deviation)
- Extreme lateral G (>2.5g)

### **Red Zone (Action Required):**
- Sensor faults
- Very high brake duty (>90%)
- Frequent extreme lateral G events
- Significant performance degradation between setups

This comprehensive analysis gives you the data-driven insights needed to optimize both your car setup and driving technique for maximum performance.
