
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "madurai_complete_weather_data.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load complete weather dataset
df = pd.read_csv(INPUT_FILE)

df["Date"] = pd.to_datetime(df["Date"])

print("Original dataset shape:", df.shape)

# Extract date features
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day
df["DayOfYear"] = df["Date"].dt.day_of_year
df["DayOfWeek"] = df["Date"].dt.day_of_week

# Add seasonal information
def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    else:
        return "Post-Monsoon"

df["Season"] = df["Month"].apply(get_season)

# Replace NASA missing-value markers
df = df.replace(-999, np.nan)

# Handle missing numerical values
numeric_columns = [
    "Solar_Radiation",
    "Temperature",
    "Wind_Speed",
    "Humidity",
    "Precipitation",
    "Max_Temperature",
    "Min_Temperature"
]

df[numeric_columns] = df[numeric_columns].interpolate(
    method="linear",
    limit_direction="both"
)

df = df.dropna(subset=numeric_columns)

# Remove duplicate records
df = df.drop_duplicates(subset=["Date"])

# Create normalized suitability indicators
def normalize(series):
    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(0.0, index=series.index)

    return (series - minimum) / (maximum - minimum)

df["Solar_Energy_Potential"] = normalize(
    df["Solar_Radiation"]
)

df["Wind_Energy_Potential"] = normalize(
    df["Wind_Speed"]
)

# Save final processed dataset
OUTPUT_FILE = OUTPUT_DIR / "madurai_final_dataset.csv"

df.to_csv(OUTPUT_FILE, index=False)

print("\nFinal preprocessing completed!")

print("\nDataset shape:", df.shape)

print("\nFinal columns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nSolar and wind potential averages:")
print(
    df[
        ["Solar_Energy_Potential", "Wind_Energy_Potential"]
    ].mean().round(3)
)

print("\nSaved final dataset:", OUTPUT_FILE)

print("\nFirst 5 records:")
print(df.head())
