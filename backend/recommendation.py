
import pandas as pd
import joblib
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "madurai_energy_estimates_corrected.csv"
SOLAR_MODEL_PATH = BASE_DIR / "models" / "solar_prediction_model.pkl"
WIND_MODEL_PATH = BASE_DIR / "models" / "wind_prediction_model.pkl"
FEATURES_PATH = BASE_DIR / "models" / "model_features.pkl"

# Solar panel assumptions
PANEL_AREA = 10
PANEL_EFFICIENCY = 0.20
PERFORMANCE_RATIO = 0.80


def load_project_data():
    """Load historical weather and energy-estimation data."""

    data = pd.read_csv(DATA_PATH)
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.sort_values("Date")

    return data


def get_latest_weather(data):
    """Get the latest available weather record."""

    latest = data.iloc[-1].copy()

    return latest


def prepare_model_input(latest, feature_columns):
    """Prepare weather features for next-day prediction."""

    month = latest["Date"].month
    day_of_year = latest["Date"].day_of_year

    model_input = {
        "Solar_Radiation": latest["Solar_Radiation"],
        "Temperature": latest["Temperature"],
        "Wind_Speed": latest["Wind_Speed"],
        "Humidity": latest["Humidity"],
        "Precipitation": latest["Precipitation"],
        "Max_Temperature": latest["Max_Temperature"],
        "Min_Temperature": latest["Min_Temperature"],
        "Month": month,
        "Day_Sin": __import__("math").sin(2 * __import__("math").pi * day_of_year / 365),
        "Day_Cos": __import__("math").cos(2 * __import__("math").pi * day_of_year / 365),
    }

    return pd.DataFrame(
        [[model_input[column] for column in feature_columns]],
        columns=feature_columns
    )


def recommend_energy(daily_demand):
    """Predict renewable energy potential and recommend an energy source."""

    if daily_demand <= 0:
        raise ValueError("Daily electricity demand must be greater than zero.")

    # Load data and models
    data = load_project_data()
    solar_model = joblib.load(SOLAR_MODEL_PATH)
    wind_model = joblib.load(WIND_MODEL_PATH)
    feature_columns = joblib.load(FEATURES_PATH)

    # Latest available weather
    latest = get_latest_weather(data)

    # Prepare model input
    model_input = prepare_model_input(latest, feature_columns)

    # Predict next-day values
    predicted_solar_generation = float(
        solar_model.predict(model_input)[0]
    )

    predicted_wind_speed = float(
        wind_model.predict(model_input)[0]
    )

    # Prevent negative predictions
    predicted_solar_generation = max(0, predicted_solar_generation)
    predicted_wind_speed = max(0, predicted_wind_speed)

    # Calculate solar coverage
    solar_coverage = (
        predicted_solar_generation / daily_demand
    ) * 100

    # Wind is evaluated as a resource indicator, not electricity generation.
    wind_potential = float(latest["Wind_Potential_Index"])

    # Recommendation rules
    if solar_coverage >= 80 and wind_potential < 0.60:
        recommendation = "Solar Energy"

        reason = (
            "Solar energy is recommended because estimated solar "
            "generation can cover most of the daily electricity demand."
        )

    elif wind_potential >= 0.60 and solar_coverage < 50:
        recommendation = "Wind Energy"

        reason = (
            "Wind energy is recommended for further assessment because "
            "the recorded wind resource indicator is relatively high. "
            "Actual turbine generation must be checked separately."
        )

    elif solar_coverage >= 50 and wind_potential >= 0.60:
        recommendation = "Hybrid Energy"

        reason = (
            "A hybrid system may be worth evaluating because both solar "
            "coverage and the wind resource indicator are relatively high."
        )

    else:
        recommendation = "Solar Energy"

        reason = (
            "Solar energy is the initial recommendation based on the "
            "available solar generation estimate. Additional capacity "
            "or another energy source may be needed to meet demand."
        )

    return {
        "location": "Madurai, Tamil Nadu",
        "latest_weather_date": latest["Date"].strftime("%Y-%m-%d"),
        "daily_demand_kwh": round(float(daily_demand), 2),
        "predicted_solar_generation_kwh": round(
            predicted_solar_generation, 2
        ),
        "predicted_wind_speed_mps": round(
            predicted_wind_speed, 2
        ),
        "wind_potential_index": round(wind_potential, 3),
        "solar_coverage_percent": round(solar_coverage, 2),
        "recommended_energy": recommendation,
        "reason": reason,
        "note": (
            "Solar generation is an estimate based on assumed panel "
            "specifications. Wind potential is not actual wind electricity "
            "generation. The latest historical weather record is used "
            "as input for next-day model predictions."
        )
    }


if __name__ == "__main__":

    print("\nRENEWABLE ENERGY RECOMMENDATION SYSTEM")
    print("-------------------------------------")

    try:
        demand = float(input("Enter daily electricity demand (kWh): "))

        result = recommend_energy(demand)

        print("\nRECOMMENDATION RESULTS")
        print("---------------------")

        for key, value in result.items():
            print(f"{key}: {value}")

    except ValueError as error:
        print("Input error:", error)

    except Exception as error:
        print("An error occurred:", error)
