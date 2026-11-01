
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "madurai_nasa_power_data.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(INPUT_FILE)

df["Date"] = pd.to_datetime(df["Date"])

print("Original dataset shape:", df.shape)

# Extract date-based features
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day
df["DayOfYear"] = df["Date"].dt.dayofyear
df["DayOfWeek"] = df["Date"].dt.dayofweek

# Define Indian meteorological seasons
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

# Remove duplicate records if any
df = df.drop_duplicates()

# Handle missing values
numeric_columns = [
    "Solar_Radiation",
    "Temperature",
    "Wind_Speed"
]

df[numeric_columns] = df[numeric_columns].replace(
    -999, float("nan")
)

df[numeric_columns] = df[numeric_columns].interpolate(
    method="linear"
)

# Remove rows that still contain missing values
df = df.dropna()

# Save processed dataset
output_file = OUTPUT_DIR / "madurai_processed_data.csv"

df.to_csv(output_file, index=False)

print("\nPreprocessing completed!")

print("\nProcessed dataset shape:", df.shape)

print("\nUpdated columns:")
print(df.columns.tolist())

print("\nSeason distribution:")
print(df["Season"].value_counts())

print("\nMissing values after preprocessing:")
print(df.isnull().sum())

print("\nSaved processed dataset:", output_file)

print("\nFirst 5 processed records:")
print(df.head())
