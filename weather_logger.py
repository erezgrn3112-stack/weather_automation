import requests
import csv
import os
from datetime import datetime, timedelta, timezone


def run_weather_logger():
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        print("Error: WEATHER_API_KEY not found.")
        return

    # רשימת 40 ערים בפריסה עולמית
    cities = [
        # צפון אמריקה
        {"name": "New York", "lat": 40.7128, "lon": -74.0060, "continent": "North America", "country": "USA"},
        {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437, "continent": "North America", "country": "USA"},
        {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194, "continent": "North America", "country": "USA"},
        {"name": "Toronto", "lat": 43.6532, "lon": -79.3832, "continent": "North America", "country": "Canada"},
        {"name": "Mexico City", "lat": 19.4326, "lon": -99.1332, "continent": "North America", "country": "Mexico"},
        # אירופה
        {"name": "London", "lat": 51.5074, "lon": -0.1278, "continent": "Europe", "country": "UK"},
        {"name": "Paris", "lat": 48.8566, "lon": 2.3522, "continent": "Europe", "country": "France"},
        {"name": "Berlin", "lat": 52.5200, "lon": 13.4050, "continent": "Europe", "country": "Germany"},
        {"name": "Amsterdam", "lat": 52.3676, "lon": 4.9041, "continent": "Europe", "country": "Netherlands"},
        {"name": "Zurich", "lat": 47.3769, "lon": 8.5417, "continent": "Europe", "country": "Switzerland"},
        {"name": "Madrid", "lat": 40.4168, "lon": -3.7038, "continent": "Europe", "country": "Spain"},
        {"name": "Rome", "lat": 41.9028, "lon": 12.4964, "continent": "Europe", "country": "Italy"},
        {"name": "Athens", "lat": 37.9838, "lon": 23.7275, "continent": "Europe", "country": "Greece"},
        {"name": "Ljubljana", "lat": 46.0569, "lon": 14.5058, "continent": "Europe", "country": "Slovenia"},
        {"name": "Zagreb", "lat": 45.8150, "lon": 15.9819, "continent": "Europe", "country": "Croatia"},
        # אסיה
        {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503, "continent": "Asia", "country": "Japan"},
        {"name": "Hong Kong", "lat": 22.3193, "lon": 114.1694, "continent": "Asia", "country": "China"},
        {"name": "Singapore", "lat": 1.3521, "lon": 103.8198, "continent": "Asia", "country": "Singapore"},
        {"name": "Seoul", "lat": 37.5665, "lon": 126.9780, "continent": "Asia", "country": "South Korea"},
        {"name": "Shanghai", "lat": 31.2304, "lon": 121.4737, "continent": "Asia", "country": "China"},
        {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777, "continent": "Asia", "country": "India"},
        {"name": "Bangkok", "lat": 13.7563, "lon": 100.5018, "continent": "Asia", "country": "Thailand"},
        {"name": "Dubai", "lat": 25.2048, "lon": 55.2708, "continent": "Asia", "country": "UAE"},
        {"name": "Tel Aviv", "lat": 32.0853, "lon": 34.7818, "continent": "Asia", "country": "Israel"},
        # אפריקה
        {"name": "Abuja", "lat": 9.0765, "lon": 7.3986, "continent": "Africa", "country": "Nigeria"},
        {"name": "Rabat", "lat": 34.0209, "lon": -6.8416, "continent": "Africa", "country": "Morocco"},
        {"name": "Cairo", "lat": 30.0444, "lon": 31.2357, "continent": "Africa", "country": "Egypt"},
        {"name": "Johannesburg", "lat": -26.2041, "lon": 28.0473, "continent": "Africa", "country": "South Africa"},
        {"name": "Nairobi", "lat": -1.2921, "lon": 36.8219, "continent": "Africa", "country": "Kenya"},
        # דרום אמריקה
        {"name": "Buenos Aires", "lat": -34.6037, "lon": -58.3816, "continent": "South America",
         "country": "Argentina"},
        {"name": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729, "continent": "South America", "country": "Brazil"},
        {"name": "Santiago", "lat": -33.4489, "lon": -70.6693, "continent": "South America", "country": "Chile"},
        {"name": "Bogota", "lat": 4.7110, "lon": -74.0721, "continent": "South America", "country": "Colombia"},
        {"name": "Lima", "lat": -12.0464, "lon": -77.0428, "continent": "South America", "country": "Peru"},
        # אוקיאניה
        {"name": "Sydney", "lat": -33.8688, "lon": 151.2093, "continent": "Oceania", "country": "Australia"},
        {"name": "Melbourne", "lat": -37.8136, "lon": 144.9631, "continent": "Oceania", "country": "Australia"},
        {"name": "Auckland", "lat": -36.8485, "lon": 174.7633, "continent": "Oceania", "country": "New Zealand"},
        # יעדים נוספים ואיים
        {"name": "Reykjavik", "lat": 64.1265, "lon": -21.8174, "continent": "Europe", "country": "Iceland"},
        {"name": "Honolulu", "lat": 21.3069, "lon": -157.8583, "continent": "Oceania", "country": "USA"},
        {"name": "Cape Town", "lat": -33.9249, "lon": 18.4241, "continent": "Africa", "country": "South Africa"}
    ]

    fieldnames = ['timestamp', 'local_time', 'city', 'country', 'continent', 'temp', 'humidity', 'description']
    file_exists = os.path.isfile('weather_data.csv')

    with open('weather_data.csv', mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        for city in cities:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={city['lat']}&lon={city['lon']}&units=metric&lang=en&appid={api_key}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                weather_row = {
                    'timestamp': data.get('dt'),
                    'local_time': (datetime.fromtimestamp(data.get('dt'), timezone.utc).replace(tzinfo=None) +
                                   timedelta(seconds=data.get('timezone'))).strftime('%Y-%m-%d %H:%M:%S'),
                    'city': city['name'],
                    'country': city['country'],  # הוספת המדינה לשורה
                    'continent': city['continent'],
                    'temp': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'description': data['weather'][0]['description']
                }
                writer.writerow(weather_row)
            except Exception as e:
                print(f"Failed for {city['name']}: {e}")

    print(f"Logged data for {len(cities)} cities successfully.")


if __name__ == "__main__":
    run_weather_logger()