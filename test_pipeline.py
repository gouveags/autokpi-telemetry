#!/usr/bin/env python3
"""
test_pipeline.py
----------------
Automated test script to verify that the entire pipeline works.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Executes a command and checks if it was successful."""
    print(f"🔄 {description}...")
    try:
        _result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {description} - Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed!")
        print(f"   Error: {e}")
        if e.stdout:
            print(f"   stdout: {e.stdout}")
        if e.stderr:
            print(f"   stderr: {e.stderr}")
        return False


def check_file_exists(filepath, description):
    """Checks if a file exists."""
    if Path(filepath).exists():
        print(f"✅ {description} - File found: {filepath}")
        return True
    else:
        print(f"❌ {description} - File not found: {filepath}")
        return False


def main():
    print("🚀 Starting AutoKPI Telemetry pipeline test...")
    print("=" * 60)

    # List of commands to test
    commands = [
        (
            "python scripts/compute_kpis.py --input data/synthetic_telemetry.csv --output data/kpis_per_lap.csv",
            "Computing KPIs per lap",
        ),
        (
            "python scripts/detect_events.py --input data/synthetic_telemetry.csv --output data/events.csv --overspeed_threshold 65 --lateral_g_threshold 1.8",
            "Detecting events",
        ),
        (
            "python scripts/count_exceedances.py --input data/synthetic_telemetry.csv --output data/exceedances.csv --channel lateral_g --threshold 1.8 --op '>'",
            "Counting exceedances",
        ),
        (
            "python scripts/compare_runs.py --input data/kpis_per_lap.csv --metric lap_time_s --output data/ab_lap_time.md",
            "A/B comparison - lap time",
        ),
        (
            "python scripts/compare_runs.py --input data/kpis_per_lap.csv --metric mean_speed_mps --output data/ab_mean_speed.md",
            "A/B comparison - mean speed",
        ),
        (
            "python scripts/regression.py --input data/kpis_per_lap.csv --output data/regression.txt",
            "Regression analysis",
        ),
        (
            "python scripts/generate_report.py --kpis data/kpis_per_lap.csv --ab1 data/ab_lap_time.md --ab2 data/ab_mean_speed.md --reg data/regression.txt --output data/report.md",
            "Generating final report",
        ),
    ]

    # Execute all commands
    success_count = 0
    for cmd, desc in commands:
        if run_command(cmd, desc):
            success_count += 1
        print()

    # Check output files
    print("📁 Checking output files...")
    output_files = [
        ("data/kpis_per_lap.csv", "KPIs per lap"),
        ("data/events.csv", "Detected events"),
        ("data/exceedances.csv", "Exceedance count"),
        ("data/ab_lap_time.md", "A/B comparison - time"),
        ("data/ab_mean_speed.md", "A/B comparison - speed"),
        ("data/regression.txt", "Regression analysis"),
        ("data/report.md", "Final report"),
    ]

    file_count = 0
    for filepath, desc in output_files:
        if check_file_exists(filepath, desc):
            file_count += 1

    # Final summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Scripts executed successfully: {success_count}/{len(commands)}")
    print(f"Output files found: {file_count}/{len(output_files)}")

    if success_count == len(commands) and file_count == len(output_files):
        print("\n🎉 ALL TESTS PASSED! The pipeline is working perfectly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
