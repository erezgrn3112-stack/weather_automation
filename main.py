import requests
import csv
import os
from datetime import datetime, timedelta, timezone


def run_weather_logger():
    # שליפת המפתח מה-Secret של GitHub (או מהמחשב המקומי)
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        print("Error: WEATHER_API_KEY not found. Make sure it's set in GitHub Secrets.")
        return

    cities = [
        {"name": "Paris", "lat": 48.8566, "lon": 2.3522, "continent": "Europe"},
        {"name": "London", "lat": 51.5074, "lon": -0.1278, "continent": "Europe"},
        {"name": "Hong Kong", "lat": 22.3193, "lon": 114.1694, "continent": "Asia"},
        {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503, "continent": "Asia"},
        {"name": "Abuja", "lat": 9.0765, "lon": 7.3986, "continent": "Africa"},
        {"name": "Rabat", "lat": 34.0209, "lon": -6.8416, "continent": "Africa"},
        {"name": "Buenos Aires", "lat": -34.6037, "lon": -58.3816, "continent": "South America"},
        {"name": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729, "continent": "South America"},
        {"name": "New York", "lat": 40.7128, "lon": -74.0060, "continent": "North America"},
        {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437, "continent": "North America"},
        {"name": "Sydney", "lat": -33.8688, "lon": 151.2093, "continent": "Oceania"}
    ]

    fieldnames = ['timestamp', 'local_time', 'city', 'continent', 'temp', 'humidity', 'description']
    file_exists = os.path.isfile('weather_data.csv')

    with open('weather_data.csv', mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        for city in cities:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={city['lat']}&lon={city['lon']}&units=metric&lang=en&appid={api_key}"
            try:
                response = requests.get(url)
                response.raise_for_status()  # בדיקה שהבקשה הצליחה
                data = response.json()

                weather_row = {
                    'timestamp': data.get('dt'),
                    'local_time': (datetime.fromtimestamp(data.get('dt'), timezone.utc).replace(tzinfo=None) +
                                   timedelta(seconds=data.get('timezone'))).strftime('%Y-%m-%d %H:%M:%S'),
                    'city': city['name'],
                    'continent': city['continent'],
                    'temp': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'description': data['weather'][0]['description']
                }
                writer.writerow(weather_row)
                print(f"Successfully logged data for {city['name']}")
            except Exception as e:
                print(f"Failed to log data for {city['name']}: {e}")


if __name__ == "__main__":
    run_weather_logger()