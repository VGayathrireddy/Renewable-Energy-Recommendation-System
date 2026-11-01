
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

from pathlib import Path

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# -----------------------------------
# PROJECT PATHS
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR / "data" / "processed" /
    "madurai_energy_estimates_corrected.csv"
)

MODEL_DIR = BASE_DIR / "models"
OUTPUT_DIR = BASE_DIR / "outputs"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------
# LOAD DATASET
# -----------------------------------

df = pd.read_csv(INPUT_FILE)

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

# -----------------------------------
# FEATURE ENGINEERING
# -----------------------------------

# Calendar features
df["Month"] = df["Date"].dt.month
df["DayOfYear"] = df["Date"].dt.day_of_year

# Cyclical encoding represents the repeating yearly pattern
df["Day_Sin"] = np.sin(
    2 * np.pi * df["DayOfYear"] / 365.25
)

df["Day_Cos"] = np.cos(
    2 * np.pi * df["DayOfYear"] / 365.25
)

# Features available on the current day
feature_columns = [
    "Solar_Radiation",
    "Temperature",
    "Wind_Speed",
    "Humidity",
    "Precipitation",
    "Max_Temperature",
    "Min_Temperature",
    "Month",
    "Day_Sin",
    "Day_Cos"
]

# Predict the following day's values
df["Next_Day_Solar_Generation"] = (
    df["Solar_Generation_kWh"].shift(-1)
)

df["Next_Day_Wind_Speed"] = (
    df["Wind_Speed"].shift(-1)
)

df = df.dropna().reset_index(drop=True)

X = df[feature_columns]

y_solar = df["Next_Day_Solar_Generation"]
y_wind = df["Next_Day_Wind_Speed"]

# -----------------------------------
# CHRONOLOGICAL TRAIN-TEST SPLIT
# -----------------------------------

# First 80% for training, final 20% for testing
split_index = int(len(df) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_solar_train = y_solar.iloc[:split_index]
y_solar_test = y_solar.iloc[split_index:]

y_wind_train = y_wind.iloc[:split_index]
y_wind_test = y_wind.iloc[split_index:]

print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# -----------------------------------
# SOLAR PREDICTION MODEL
# -----------------------------------

print("\nTraining Solar Prediction Model...")

solar_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=12,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)

solar_model.fit(X_train, y_solar_train)

solar_predictions = solar_model.predict(X_test)

# -----------------------------------
# WIND PREDICTION MODEL
# -----------------------------------

print("\nTraining Wind Prediction Model...")

wind_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=12,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)

wind_model.fit(X_train, y_wind_train)

wind_predictions = wind_model.predict(X_test)

# -----------------------------------
# MODEL EVALUATION
# -----------------------------------

def evaluate_model(actual, predicted, model_name):

    mae = mean_absolute_error(actual, predicted)

    rmse = np.sqrt(
        mean_squared_error(actual, predicted)
    )

    r2 = r2_score(actual, predicted)

    print(f"\n{model_name} Results")
    print("-----------------------------")
    print(f"MAE  : {mae:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"R2   : {r2:.4f}")

    return {
        "Model": model_name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }


solar_results = evaluate_model(
    y_solar_test,
    solar_predictions,
    "Solar Generation Prediction"
)

wind_results = evaluate_model(
    y_wind_test,
    wind_predictions,
    "Wind Speed Prediction"
)

# -----------------------------------
# SAVE TRAINED MODELS
# -----------------------------------

joblib.dump(
    solar_model,
    MODEL_DIR / "solar_prediction_model.pkl"
)

joblib.dump(
    wind_model,
    MODEL_DIR / "wind_prediction_model.pkl"
)

# Save feature information
joblib.dump(
    feature_columns,
    MODEL_DIR / "model_features.pkl"
)

# Save evaluation results
results_df = pd.DataFrame([
    solar_results,
    wind_results
])

results_df.to_csv(
    OUTPUT_DIR / "model_evaluation.csv",
    index=False
)

# -----------------------------------
# SAVE TEST PREDICTIONS
# -----------------------------------

predictions_df = pd.DataFrame({
    "Date": df["Date"].iloc[split_index:],
    "Actual_Solar_Generation_kWh": y_solar_test.values,
    "Predicted_Solar_Generation_kWh": solar_predictions,
    "Actual_Wind_Speed": y_wind_test.values,
    "Predicted_Wind_Speed": wind_predictions
})

predictions_df.to_csv(
    OUTPUT_DIR / "model_predictions.csv",
    index=False
)

# -----------------------------------
# VISUALIZE SOLAR PREDICTIONS
# -----------------------------------

plt.figure(figsize=(14, 6))

plt.plot(
    predictions_df["Date"],
    predictions_df["Actual_Solar_Generation_kWh"],
    label="Actual Solar Generation"
)

plt.plot(
    predictions_df["Date"],
    predictions_df["Predicted_Solar_Generation_kWh"],
    label="Predicted Solar Generation"
)

plt.title("Actual vs Predicted Solar Generation")
plt.xlabel("Date")
plt.ylabel("Solar Generation (kWh)")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "solar_prediction.png",
    dpi=300
)

plt.show()

# -----------------------------------
# VISUALIZE WIND PREDICTIONS
# -----------------------------------

plt.figure(figsize=(14, 6))

plt.plot(
    predictions_df["Date"],
    predictions_df["Actual_Wind_Speed"],
    label="Actual Wind Speed"
)

plt.plot(
    predictions_df["Date"],
    predictions_df["Predicted_Wind_Speed"],
    label="Predicted Wind Speed"
)

plt.title("Actual vs Predicted Wind Speed")
plt.xlabel("Date")
plt.ylabel("Wind Speed (m/s)")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "wind_prediction.png",
    dpi=300
)

plt.show()

print("\n===================================")
print("MACHINE LEARNING TRAINING COMPLETED")
print("===================================")

print("\nModels saved inside:", MODEL_DIR)
print("Evaluation saved inside:", OUTPUT_DIR)
print("Prediction graphs saved inside:", OUTPUT_DIR)
