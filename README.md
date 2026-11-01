# ☀ RenewableAI – Renewable Energy Recommendation System

## 1. Project Overview

RenewableAI is an AI-powered Renewable Energy Recommendation System that analyzes historical weather conditions and estimates renewable energy potential.

The system studies solar radiation, temperature, humidity, precipitation and wind speed to estimate solar energy generation and predict wind speed.

Based on the estimated solar generation and the user's daily electricity demand, the system recommends a suitable renewable energy source.

The project currently focuses on **Madurai, Tamil Nadu**, using historical weather data collected from NASA POWER.

## 2. Project Objectives

- Analyze historical solar and wind weather conditions.
- Study the relationship between weather conditions and renewable energy potential.
- Estimate possible solar electricity generation.
- Predict next-day solar generation estimates and wind speed using machine learning.
- Recommend a suitable renewable energy source based on electricity demand.
- Present weather analysis and recommendation results through an interactive dashboard.
- Support better renewable energy planning and resource utilization.

## 3. Features

### Weather Data Analysis
- Historical weather data from NASA POWER.
- Solar radiation analysis.
- Temperature and humidity analysis.
- Wind speed and precipitation analysis.
- Monthly weather pattern visualization.

### Energy Estimation
- Estimates solar electricity generation using solar radiation and assumed solar panel specifications.
- Calculates a relative wind potential index using historical wind speed.

### Machine Learning
- Random Forest Regression for next-day solar generation estimation.
- Random Forest Regression for next-day wind speed prediction.
- Model evaluation using MAE, RMSE and R².

### Energy Recommendation
- Accepts daily electricity demand from the user.
- Compares estimated solar generation with electricity demand.
- Calculates solar demand coverage.
- Recommends a suitable renewable energy source using predefined recommendation rules.

### Interactive Dashboard
- Displays energy recommendations.
- Shows estimated energy metrics.
- Visualizes historical weather patterns.
- Displays monthly solar radiation, temperature, wind speed and estimated solar generation.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data processing and analysis |
| NumPy | Numerical calculations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Scikit-learn | Machine learning |
| Random Forest | Prediction models |
| Joblib | Saving and loading trained models |
| FastAPI | Backend API development |
| Uvicorn | Running the backend server |
| HTML | Frontend structure |
| CSS | Frontend styling |
| JavaScript | Frontend functionality |
| Chart.js | Interactive charts |
| NASA POWER API | Historical weather data source |

## 5. Dataset Information

**Data Source:** NASA POWER

**Location:** Madurai, Tamil Nadu, India

**Coordinates:**
- Latitude: 9.9252
- Longitude: 78.1198

**Data Period:** 01 January 2015 – 31 December 2025

**Total Records:** 4,018 daily records

### Weather Parameters

| Parameter | Description |
|---|---|
| Solar Radiation | Daily solar energy received per square metre |
| Temperature | Daily average temperature |
| Wind Speed | Daily average wind speed at 10 metres |
| Humidity | Relative humidity |
| Precipitation | Daily precipitation |
| Maximum Temperature | Daily maximum temperature |
| Minimum Temperature | Daily minimum temperature |

The dataset is collected from NASA POWER and processed before being used for energy estimation and machine learning.

## 6. Machine Learning Models

The project uses two Random Forest Regression models.

### Model 1: Solar Generation Prediction

Predicts the next day's estimated solar electricity generation based on weather information.

The estimated generation is calculated using:

Solar Generation (kWh/day) = Solar Radiation × Panel Area × Panel Efficiency × Performance Ratio

Assumed specifications:
- Panel Area = 10 m²
- Panel Efficiency = 20%
- Performance Ratio = 80%

### Model 2: Wind Speed Prediction

Predicts the next day's wind speed using historical weather parameters.

Wind speed is used to understand wind resource potential. It is not treated as actual wind electricity generation.

### Model Evaluation

| Evaluation Metric | Solar Model | Wind Model |
|---|---:|---:|
| MAE | 0.9875 | 0.4714 |
| RMSE | 1.3434 | 0.6197 |
| R² Score | 0.5441 | 0.6534 |

The models use a chronological training and testing split to preserve the time order of the historical data.

## 7. Project Folder Structure

```text
Renewable-Energy-Project/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── recommendation.py
│   ├── fetch_weather_data.py
│   └── fetch_additional_weather_data.py
│
├── data/
│   ├── raw/
│   │   ├── madurai_nasa_power_data.csv
│   │   └── madurai_complete_weather_data.csv
│   │
│   └── processed/
│       ├── madurai_final_dataset.csv
│       └── madurai_energy_estimates_corrected.csv
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── models/
│   ├── solar_prediction_model.pkl
│   ├── wind_prediction_model.pkl
│   └── model_features.pkl
│
├── notebooks/
│   ├── explore_data.py
│   ├── preprocess_data.py
│   ├── final_preprocessing.py
│   ├── estimate_energy.py
│   └── train_models.py
│
├── outputs/
│   ├── model_evaluation.csv
│   ├── model_predictions.csv
│   ├── solar_prediction.png
│   ├── wind_prediction.png
│   ├── weather_patterns.png
│   ├── monthly_averages.png
│   └── feature_distributions.png
│
├── requirements.txt
└── README.md
```

## 8. Installation and Setup

### Step 1: Clone the Repository

```bash
git clone <your-github-repository-url>
```

Navigate to the project folder:

```bash
cd Renewable-Energy-Project
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 3: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 4: Install Required Libraries

```bash
pip install -r requirements.txt
```

### Step 5: Run the Backend Server

From the project root directory:

```bash
python -m uvicorn backend.main:app --reload
```

Backend URL:

http://127.0.0.1:8000

API Documentation:

http://127.0.0.1:8000/docs

### Step 6: Run the Frontend

Open another terminal, navigate to the project root directory and activate the virtual environment if needed.

Run:

```bash
python -m http.server 5500 --directory frontend
```

Open the dashboard:

http://127.0.0.1:5500

Both backend and frontend servers must be running to use the complete application.

## 9. API Endpoints

The project uses FastAPI to connect the frontend with the backend.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Checks backend status |
| POST | `/recommend` | Generates an energy recommendation |
| GET | `/analytics` | Returns historical monthly weather analytics |

### Recommendation API Example

Request:

```json
{
    "daily_demand_kwh": 10
}
```

The API returns:
- Recommended energy source.
- Estimated solar generation.
- Predicted wind speed.
- Solar demand coverage.
- Location and weather date.
- Recommendation explanation.

## 10. How the System Works

1. Historical weather data is collected from NASA POWER.
2. The collected data is cleaned and processed.
3. Weather parameters are analyzed to understand renewable energy patterns.
4. Solar electricity generation is estimated using assumed panel specifications.
5. Machine learning models predict next-day solar generation estimates and wind speed.
6. The user enters their daily electricity demand.
7. The recommendation engine compares the estimated solar generation with the entered demand and evaluates wind potential.
8. The system displays the recommendation and analysis results through the dashboard.

## 11. Limitations

- The current implementation supports Madurai, Tamil Nadu, only.
- Solar generation is an estimate based on assumed panel specifications, not actual measured electricity output.
- Wind speed prediction does not directly calculate wind turbine electricity generation.
- Historical weather data ends on 31 December 2025.
- The current prediction uses the latest available historical record as input; it is not a live weather forecast.
- Electricity demand is entered by the user. Historical electricity consumption data is not currently integrated.
- Recommendation rules use predefined thresholds and are intended for an academic prototype.

## 12. Future Enhancements

- Support multiple geographical locations.
- Add location-based weather data collection.
- Integrate actual electricity consumption datasets.
- Improve solar and wind energy forecasting.
- Include wind turbine specifications and power curves for wind generation estimates.
- Add live weather data integration.
- Improve recommendation logic using additional technical and economic factors.
- Estimate installation costs and potential energy savings.

## 13. Conclusion

RenewableAI demonstrates how historical weather data, machine learning and data analysis can support renewable energy planning.

By analyzing solar radiation, temperature, humidity and wind speed, the system estimates solar energy generation and evaluates wind resource potential.

It then compares estimated solar availability with user-provided electricity demand and recommends a suitable renewable energy source.

The project provides an interactive platform for understanding renewable energy potential and demonstrates the application of AI and machine learning in sustainable energy planning.

---

**Project Name:** RenewableAI – Renewable Energy Recommendation System

**Data Source:** NASA POWER

**Primary Location:** Madurai, Tamil Nadu, India
