
import requests
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

EXISTING_FILE = RAW_DIR / "madurai_nasa_power_data.csv"
OUTPUT_FILE = RAW_DIR / "madurai_complete_weather_data.csv"

# Madurai coordinates
LATITUDE = 9.9252
LONGITUDE = 78.1198

API_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

# Additional weather parameters
PARAMETERS = [
    "RH2M",          # Relative humidity (%)
    "PRECTOTCORR",   # Corrected precipitation (mm/day)
    "T2M_MAX",       # Maximum temperature (°C)
    "T2M_MIN"        # Minimum temperature (°C)
]

params = {
    "parameters": ",".join(PARAMETERS),
    "community": "RE",
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "start": "20150101",
    "end": "20251231",
    "format": "JSON"
}

try:
    print("Downloading additional weather data for Madurai...")

    response = requests.get(
        API_URL,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    parameter_data = data["properties"]["parameter"]

    # Convert additional data into DataFrame
    additional_df = pd.DataFrame(parameter_data)

    additional_df.index.name = "Date"
    additional_df = additional_df.reset_index()

    additional_df["Date"] = pd.to_datetime(
        additional_df["Date"],
        format="%Y%m%d"
    )

    # Rename columns
    additional_df = additional_df.rename(columns={
        "RH2M": "Humidity",
        "PRECTOTCORR": "Precipitation",
        "T2M_MAX": "Max_Temperature",
        "T2M_MIN": "Min_Temperature"
    })

    additional_df = additional_df.replace(
        -999, float("nan")
    )

    # Load previously downloaded dataset
    existing_df = pd.read_csv(EXISTING_FILE)
    existing_df["Date"] = pd.to_datetime(existing_df["Date"])

    # Combine datasets using Date
    complete_df = pd.merge(
        existing_df,
        additional_df,
        on="Date",
        how="left"
    )

    complete_df = complete_df.sort_values("Date")

    # Save enhanced dataset
    complete_df.to_csv(OUTPUT_FILE, index=False)

    print("\nAdditional data downloaded successfully!")

    print("\nNew parameters:")
    print([
        "Humidity",
        "Precipitation",
        "Max_Temperature",
        "Min_Temperature"
    ])

    print("\nComplete dataset shape:", complete_df.shape)

    print("\nFirst 5 records:")
    print(complete_df.head())

    print("\nMissing values:")
    print(complete_df.isnull().sum())

    print("\nSaved file:", OUTPUT_FILE)

except requests.exceptions.RequestException as error:
    print("\nAPI connection error:", error)

except (KeyError, ValueError) as error:
    print("\nData processing error:", error)

except Exception as error:
    print("\nUnexpected error:", error)
