
import requests
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Madurai location
LATITUDE = 9.9252
LONGITUDE = 78.1198

# NASA POWER API
API_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

PARAMETERS = [
    "ALLSKY_SFC_SW_DWN",  # Solar radiation
    "T2M",                # Temperature at 2 metres
    "WS10M"               # Wind speed at 10 metres
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
    print("Downloading NASA POWER data for Madurai...")

    response = requests.get(
        API_URL,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    # Extract parameter data
    parameter_data = data["properties"]["parameter"]

    # Convert JSON data into a DataFrame
    df = pd.DataFrame(parameter_data)

    # Convert date index into a column
    df.index.name = "Date"
    df = df.reset_index()

    df["Date"] = pd.to_datetime(
        df["Date"],
        format="%Y%m%d"
    )

    # Rename columns
    df = df.rename(columns={
        "ALLSKY_SFC_SW_DWN": "Solar_Radiation",
        "T2M": "Temperature",
        "WS10M": "Wind_Speed"
    })

    # Replace NASA missing-value markers
    df = df.replace(-999, float("nan"))

    # Sort by date
    df = df.sort_values("Date")

    # Save CSV file
    output_file = RAW_DATA_DIR / "madurai_nasa_power_data.csv"
    df.to_csv(output_file, index=False)

    print("\nData downloaded successfully!")
    print("Location: Madurai, Tamil Nadu")
    print("Total records:", len(df))
    print("Columns:", list(df.columns))
    print("\nFirst 5 records:")
    print(df.head())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nSaved file:", output_file)

except requests.exceptions.RequestException as error:
    print("API connection error:", error)

except (KeyError, ValueError) as error:
    print("Data processing error:", error)

except Exception as error:
    print("Unexpected error:", error)
