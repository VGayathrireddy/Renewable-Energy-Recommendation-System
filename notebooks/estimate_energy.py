
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR / "data" / "processed" /
    "madurai_final_dataset.csv"
)

OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(INPUT_FILE)

# --------------------------------
# SOLAR GENERATION ESTIMATION
# --------------------------------

# Illustrative solar panel assumptions
PANEL_AREA = 10
PANEL_EFFICIENCY = 0.20
PERFORMANCE_RATIO = 0.80

# NASA daily solar radiation is already kWh/m2/day.
# Therefore, no division by 3.6 is required.

df["Solar_Generation_kWh"] = (
    df["Solar_Radiation"]
    * PANEL_AREA
    * PANEL_EFFICIENCY
    * PERFORMANCE_RATIO
)

# --------------------------------
# WIND POTENTIAL INDICATOR
# --------------------------------

# Normalize wind speed between 0 and 1.
# This is a relative indicator, NOT electricity generation.

minimum = df["Wind_Speed"].min()
maximum = df["Wind_Speed"].max()

if maximum > minimum:
    df["Wind_Potential_Index"] = (
        (df["Wind_Speed"] - minimum) /
        (maximum - minimum)
    )
else:
    df["Wind_Potential_Index"] = 0.0

# --------------------------------
# SUMMARY
# --------------------------------

print("CORRECTED ENERGY ESTIMATION")
print("--------------------------------")

print("\nSolar generation estimate:")
print(df["Solar_Generation_kWh"].describe().round(2))

print(
    "\nAverage daily solar generation:",
    round(df["Solar_Generation_kWh"].mean(), 2),
    "kWh"
)

print("\nWind potential index:")
print(df["Wind_Potential_Index"].describe().round(3))

print(
    "\nAverage wind potential index:",
    round(df["Wind_Potential_Index"].mean(), 3)
)

# Save corrected dataset
OUTPUT_FILE = (
    OUTPUT_DIR / "madurai_energy_estimates_corrected.csv"
)

df.to_csv(OUTPUT_FILE, index=False)

print("\nCorrected estimates saved successfully!")
print("File:", OUTPUT_FILE)

print("\nFirst five records:")
print(
    df[
        [
            "Date",
            "Solar_Generation_kWh",
            "Wind_Speed",
            "Wind_Potential_Index"
        ]
    ].head()
)
