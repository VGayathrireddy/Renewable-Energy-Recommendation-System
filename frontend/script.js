
const API_URL = "https://renewable-energy-recommendation-system.onrender.com";

let weatherCharts = [];

// ========================================
// 1. RENEWABLE ENERGY RECOMMENDATION
// ========================================

async function getRecommendation() {

    const demandInput = document.getElementById("demand");
    const button = document.getElementById("recommendBtn");
    const errorMessage = document.getElementById("errorMessage");

    const demand = Number(demandInput.value);

    errorMessage.textContent = "";

    if (!demandInput.value || !Number.isFinite(demand) || demand <= 0) {
        errorMessage.textContent =
            "Please enter a valid electricity demand greater than zero.";
        return;
    }

    button.disabled = true;
    button.innerHTML = "Analyzing...";

    try {

        const response = await fetch(`${API_URL}/recommend`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                daily_demand_kwh: demand
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Unable to generate recommendation.");
        }

        if (!data.success || !data.result) {
            throw new Error("Invalid response received from the server.");
        }

        const result = data.result;

        // Recommendation
        document.getElementById("recommendedEnergy").textContent =
            result.recommended_energy;

        document.getElementById("recommendationReason").textContent =
            result.reason;

        // Energy metrics
        document.getElementById("demandResult").textContent =
            Number(result.daily_demand_kwh).toFixed(2);

        document.getElementById("solarResult").textContent =
            Number(result.predicted_solar_generation_kwh).toFixed(2);

        document.getElementById("windResult").textContent =
            Number(result.predicted_wind_speed_mps).toFixed(2);

        document.getElementById("coverageResult").textContent =
            Number(result.solar_coverage_percent).toFixed(2) + "%";

        // Additional information
        document.getElementById("locationResult").textContent =
            result.location;

        document.getElementById("dateResult").textContent =
            result.latest_weather_date;

        document.getElementById("windIndexResult").textContent =
            result.wind_potential_index;

        document.getElementById("coverageDetail").textContent =
            Number(result.solar_coverage_percent).toFixed(2) + "%";

        document.getElementById("resultNote").textContent =
            result.note;

        // Display result section
        const resultsSection = document.getElementById("resultsSection");

        resultsSection.classList.remove("hidden");

        resultsSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    } catch (error) {

        errorMessage.textContent =
            error.message || "Unable to connect to the backend.";

    } finally {

        button.disabled = false;
        button.innerHTML = 'Analyze & Recommend <span>→</span>';

    }
}


// ========================================
// 2. LOAD HISTORICAL WEATHER ANALYTICS
// ========================================

async function loadWeatherAnalytics() {

    const errorElement = document.getElementById("analyticsError");

    try {

        const response = await fetch(`${API_URL}/analytics`);

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Unable to load analytics.");
        }

        if (!data.success || !Array.isArray(data.monthly_data)) {
            throw new Error("Invalid analytics data received.");
        }

        const monthlyData = data.monthly_data;

        if (monthlyData.length === 0) {
            throw new Error("No historical weather records available.");
        }

        // Display period and record information
        document.getElementById("analyticsPeriod").textContent =
            `Data period: ${data.period} | ${data.records} daily records | Source: ${data.data_source}`;

        // Calculate yearly monthly averages
        const average = (key) =>
            monthlyData.reduce((sum, item) => sum + Number(item[key]), 0)
            / monthlyData.length;

        // Display summary cards
        document.getElementById("avgSolar").textContent =
            average("solar_radiation").toFixed(2);

        document.getElementById("avgTemperature").textContent =
            average("temperature").toFixed(2);

        document.getElementById("avgWind").textContent =
            average("wind_speed").toFixed(2);

        document.getElementById("avgGeneration").textContent =
            average("solar_generation").toFixed(2);

        // Chart labels
        const labels = monthlyData.map(item => item.month);

        // Chart datasets
        const solarRadiation = monthlyData.map(
            item => item.solar_radiation
        );

        const temperature = monthlyData.map(
            item => item.temperature
        );

        const windSpeed = monthlyData.map(
            item => item.wind_speed
        );

        const solarGeneration = monthlyData.map(
            item => item.solar_generation
        );

        // Remove old charts if analytics reloads
        weatherCharts.forEach(chart => chart.destroy());
        weatherCharts = [];

        // Common chart configuration
        const commonOptions = {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: "index"
            },
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: "#edf1ee"
                    },
                    ticks: {
                        font: {
                            size: 10
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 0,
                        font: {
                            size: 9
                        }
                    }
                }
            }
        };

        // 1. Solar Radiation Chart
        weatherCharts.push(
            new Chart(document.getElementById("solarChart"), {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Solar Radiation",
                        data: solarRadiation,
                        borderColor: "#e9a52c",
                        backgroundColor: "rgba(233, 165, 44, 0.15)",
                        fill: true,
                        tension: 0.35,
                        pointRadius: 3
                    }]
                },
                options: {
                    ...commonOptions,
                    scales: {
                        ...commonOptions.scales,
                        y: {
                            ...commonOptions.scales.y,
                            title: {
                                display: true,
                                text: "kWh/m²/day"
                            }
                        }
                    }
                }
            })
        );

        // 2. Temperature Chart
        weatherCharts.push(
            new Chart(document.getElementById("temperatureChart"), {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Temperature",
                        data: temperature,
                        backgroundColor: "#e98b63",
                        borderRadius: 5
                    }]
                },
                options: {
                    ...commonOptions,
                    scales: {
                        ...commonOptions.scales,
                        y: {
                            ...commonOptions.scales.y,
                            title: {
                                display: true,
                                text: "Temperature (°C)"
                            }
                        }
                    }
                }
            })
        );

        // 3. Wind Speed Chart
        weatherCharts.push(
            new Chart(document.getElementById("windChart"), {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Wind Speed",
                        data: windSpeed,
                        borderColor: "#438acb",
                        backgroundColor: "rgba(67, 138, 203, 0.15)",
                        fill: true,
                        tension: 0.35,
                        pointRadius: 3
                    }]
                },
                options: {
                    ...commonOptions,
                    scales: {
                        ...commonOptions.scales,
                        y: {
                            ...commonOptions.scales.y,
                            title: {
                                display: true,
                                text: "Wind Speed (m/s)"
                            }
                        }
                    }
                }
            })
        );

        // 4. Solar Generation Chart
        weatherCharts.push(
            new Chart(document.getElementById("generationChart"), {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Estimated Solar Generation",
                        data: solarGeneration,
                        backgroundColor: "#23965b",
                        borderRadius: 5
                    }]
                },
                options: {
                    ...commonOptions,
                    scales: {
                        ...commonOptions.scales,
                        y: {
                            ...commonOptions.scales.y,
                            title: {
                                display: true,
                                text: "Estimated Generation (kWh/day)"
                            }
                        }
                    }
                }
            })
        );

    } catch (error) {

        errorElement.textContent =
            "Weather analytics error: " + error.message;

        console.error("Analytics error:", error);

    }
}


// ========================================
// 3. LOAD DASHBOARD DATA WHEN PAGE OPENS
// ========================================

document.addEventListener("DOMContentLoaded", () => {

    loadWeatherAnalytics();

});
