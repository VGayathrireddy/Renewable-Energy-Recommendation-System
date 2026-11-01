
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pathlib import Path
import pandas as pd

from backend.recommendation import recommend_energy


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR / "data" / "processed" /
    "madurai_energy_estimates_corrected.csv"
)


# Create FastAPI application
app = FastAPI(
    title="Renewable Energy Recommendation System",
    description="API for renewable energy prediction, recommendation and weather analytics.",
    version="1.1.0"
)


# Allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Recommendation input
class EnergyRequest(BaseModel):
    daily_demand_kwh: float = Field(
        gt=0,
        description="Daily electricity requirement in kWh"
    )


# Load historical dataset
def load_weather_data():
    data = pd.read_csv(DATA_PATH)
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.sort_values("Date")
    return data


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Renewable Energy Recommendation System API",
        "status": "Running"
    }


# Recommendation endpoint
@app.post("/recommend")
def get_recommendation(request: EnergyRequest):

    try:
        result = recommend_energy(request.daily_demand_kwh)

        return {
            "success": True,
            "result": result
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# Historical weather analytics endpoint
@app.get("/analytics")
def get_weather_analytics():

    try:
        data = load_weather_data()

        # Calculate monthly averages across all available years
        data["Month"] = data["Date"].dt.month

        monthly = (
            data.groupby("Month")
            .agg(
                Solar_Radiation=("Solar_Radiation", "mean"),
                Temperature=("Temperature", "mean"),
                Wind_Speed=("Wind_Speed", "mean"),
                Solar_Generation_kWh=("Solar_Generation_kWh", "mean")
            )
            .reindex(range(1, 13))
            .reset_index()
        )

        month_names = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]

        monthly_data = []

        for _, row in monthly.iterrows():
            monthly_data.append({
                "month": month_names[int(row["Month"]) - 1],
                "solar_radiation": round(float(row["Solar_Radiation"]), 2),
                "temperature": round(float(row["Temperature"]), 2),
                "wind_speed": round(float(row["Wind_Speed"]), 2),
                "solar_generation": round(
                    float(row["Solar_Generation_kWh"]), 2
                )
            })

        return {
            "success": True,
            "location": "Madurai, Tamil Nadu",
            "data_source": "NASA POWER",
            "period": (
                f"{data['Date'].min().date()} to "
                f"{data['Date'].max().date()}"
            ),
            "records": int(len(data)),
            "monthly_data": monthly_data
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to load weather analytics: {str(error)}"
        )
