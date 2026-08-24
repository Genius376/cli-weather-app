# Flask Weather App

A lightweight Flask web application that fetches and displays live weather conditions for any city using the [Open-Meteo API](https.open-meteo.com).

## Features

- **Geocoding Search:** Converts city names into precise latitude and longitude coordinates.
- **Real-Time Forecasts:** Retrieves current temperature, sea-level pressure, and WMO weather codes.
- **Weather Code Mapping:** Translates numeric WMO codes into human-readable weather descriptions (e.g., sunny, moderate rain, heavy snow).

## Project Structure

```text
.
├── app.py              # Main Flask application script
├── templates/
│   └── home.html       # HTML template for inputting city & displaying weather
└── README.md
