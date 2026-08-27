import requests, json
from flask import Flask, render_template
from flask import request, redirect, url_for

app = Flask(__name__)

global_weather = None

def geolocation(city_name:str) -> tuple[float, float] | None:
    url = "https://geocoding-api.open-meteo.com/v1/search"

    # dict
    payload = {
        "name": city_name,
        "count": 1
    }

    response = requests.get(url, params=payload)

    if not response.ok:
        print(f"API status code not OK.\n - status code: {response.status_code}\n - text: {response.text}")
        return None

    resp = response.json() # pretvara JSON u dict

    lat = resp["results"][0].get("latitude")
    lon = resp["results"][0].get("longitude")

    return lat, lon

def get_weather(coords:tuple[float, float]) -> dict | None: 
    url = "https://api.open-meteo.com/v1/forecast"

    lat, lon = coords

    # dict
    payload = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,weather_code,pressure_msl,wind_speed_10m,wind_direction_10m",
    }

    response = requests.get(url, params=payload)

    if not response.ok:
        print(f"API status code not OK.\n - status code: {response.status_code}\n - text: {response.text}")
        return None

    resp = response.json() # pretvara JSON u dict

    result = {
        "temperature": resp["current"]["temperature_2m"],
        "pressure": resp["current"]["pressure_msl"],
        "weather": resp["current"]["weather_code"]
    }

    return result

weather_code_map = {
    0: "sunny",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense intensity drizzle",
    56: "freezin drizzle(light)",
    57: "freezin drizzle(dense)",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    66: "freezin rain(light)",
    67: "freezin rain(heavy)",
    71: "snow fall(slight)",
    73: "snow fall(moderate)",
    75: "snow fall(heavy)",
    77: "snow grains",
    80: "rain showers(slight)",
    81: "rain showers(moderate)",
    82: "rain showers(heavy)",
    85: "snow showers(slight)",
    86: "snow showers(heavy)",
    95: "thunderstorm(slight)",
    96: "thunderstorm(moderate)",
    99: "thunderstorm(heavy)"
}

@app.route("/")
def home():
    return render_template("home.html", message="Welcome to the forecast app!", weather=global_weather)

@app.route("/submit", methods=["POST"])
def submit():
    global global_weather
    city_name = request.form.get("city_name")
    if city_name:
        coords = geolocation(city_name)
        weather_data = get_weather(coords)
        weather_code = weather_data["weather"]
        weather = weather_code_map[weather_code]
        global_weather = weather
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)