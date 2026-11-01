
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "raw" / "madurai_nasa_power_data.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_FILE)

df["Date"] = pd.to_datetime(df["Date"])

print("========== DATASET INFORMATION ==========")

print("\nFirst 5 records:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumn information:")
print(df.info())

print("\nStatistical summary:")
print(df.describe())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate records:")
print(df.duplicated().sum())

# Extract month and year
df["Month"] = df["Date"].dt.month
df["Year"] = df["Date"].dt.year

# Monthly average values
monthly_data = df.groupby("Month")[
    ["Solar_Radiation", "Temperature", "Wind_Speed"]
].mean()

print("\n========== MONTHLY AVERAGES ==========")
print(monthly_data.round(2))

# 1. Visualize yearly weather patterns
fig, axes = plt.subplots(3, 1, figsize=(14, 12))

features = [
    ("Solar_Radiation", "Solar Radiation"),
    ("Temperature", "Temperature"),
    ("Wind_Speed", "Wind Speed")
]

for ax, (column, label) in zip(axes, features):
    ax.plot(df["Date"], df[column])
    ax.set_title(f"{label} Over Time - Madurai")
    ax.set_xlabel("Year")
    ax.set_ylabel(label)
    ax.grid(True)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "weather_patterns.png",
    dpi=300
)

plt.show()

# 2. Visualize monthly averages
monthly_data.plot(
    kind="bar",
    figsize=(12, 6)
)

plt.title("Monthly Average Weather Conditions - Madurai")
plt.xlabel("Month")
plt.ylabel("Average Value")
plt.xticks(rotation=0)
plt.grid(axis="y")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "monthly_averages.png",
    dpi=300
)

plt.show()

# 3. Distribution of weather features
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for ax, (column, label) in zip(axes, features):
    ax.hist(df[column], bins=30)
    ax.set_title(f"{label} Distribution")
    ax.set_xlabel(label)
    ax.set_ylabel("Frequency")
    ax.grid(True)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "feature_distributions.png",
    dpi=300
)

plt.show()

print("\nAll visualizations saved successfully!")
print("Check the outputs folder.")
