# Business Travel Weather Control Center 🌍✈️

A professional-grade weather analysis dashboard designed for business travelers. This system combines real-time weather monitoring with historical trend analysis using a robust automated data pipeline.

## 🚀 Live Demo
**[Insert your Streamlit link here]** *(Example: https://weather-automation-erez.streamlit.app/)*

## 📋 Project Description
This project provides a comprehensive "Control Center" for 40 major global destinations. It is built to help business travelers make data-driven decisions regarding packing and scheduling by analyzing long-term climate patterns alongside real-time updates.

### Key Features:
* **Automated Data Pipeline:** A background bot (`weather_logger.py`) executes hourly via GitHub Actions to collect metrics into a growing historical dataset of over 11,000 records.
* **Predictive Trends:** Uses **Linear Regression** (via Seaborn) to visualize temperature trends over the past 7 days and predict variations for the next 24 hours.
* **Smart Forecasting:** Provides a 5-day outlook synchronized with each destination's local timezone.
* **Engineering Logic:** Includes a dynamic "Packing Essentials" algorithm that provides recommendations based on specific real-time Celsius thresholds.
* **Interactive Mapping:** Geospatial visualization of destinations using high-accuracy coordinates.

## 🛠️ Technical Stack
* **Language:** Python 3.x
* **Framework:** Streamlit (UI/UX)
* **Libraries:** Pandas (Data Wrangling), Seaborn/Matplotlib (Statistical Visualization), Requests (API Integration).
* **Automation:** GitHub Actions (CI/CD for data logging).
* **Data Source:** OpenWeatherMap API.

## ⚙️ How to Use
1.  **Select Destination:** Use the hierarchical filters (Continent -> Country -> City) to choose a location.
2.  **Toggle Units:** Switch between Metric (°C) and Imperial (°F) using the interactive toggle.
3.  **Analyze Trends:** Review the regression plots to understand if the weather is warming up or cooling down over time.
4.  **Manage Favorites:** Save destinations to your sidebar list for quick access (persisted via `settings.json`).

## 📂 Execution Instructions
The primary entry point for the application is **`main.py`**.

### To run this project locally:
1.  **Install Dependencies:**
    ```bash
    pip install streamlit pandas requests seaborn matplotlib
    ```
2.  **Set API Key:**
    Configure your `WEATHER_API_KEY` in your environment variables or a local `.streamlit/secrets.toml` file.
3.  **Run the App:**
    ```bash
    streamlit run main.py
    ```

---
*Developed as an Engineering Project for Python Programming.*
