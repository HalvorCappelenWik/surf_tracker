import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("STORMGLASS_API_KEY")

# Example lat/lon for Ericeira — ideally you should map beach names to coordinates
BEACH_COORDS = {
    "Ericeira": {"lat": 38.96, "lng": -9.42},
    "Nazare": {"lat": 39.60, "lng": -9.07},
    "Peniche": {"lat": 39.36, "lng": -9.38}
}


# surf_alert.py (mock version with quality score)

def check_conditions(beach, min_wave):
    # Mocked forecast data
    wave_height = 1.9        # meters
    wind_speed = 6.5         # knots
    wind_direction = 45      # degrees
    swell_period = 12        # seconds

    # --- Scoring System ---
    score = 0

    # Wave height scoring (ideal: 1.5 - 2.5m)
    if 1.5 <= wave_height <= 2.5:
        score += 4
    elif 1.0 <= wave_height < 1.5 or 2.5 < wave_height <= 3.0:
        score += 2

    # Wind speed scoring (lower = better)
    if wind_speed <= 8:
        score += 3
    elif wind_speed <= 12:
        score += 1

    # Swell period scoring
    if swell_period >= 10:
        score += 3
    elif swell_period >= 8:
        score += 1

    # Result message
    message = (
        f"📊 Surf Quality Score for {beach}: {score}/10\n\n"
        f"🌊 Wave height: {wave_height:.1f}m\n"
        f"💨 Wind: {wind_speed:.1f} knots, dir: {wind_direction:.0f}°\n"
        f"🌊 Swell period: {swell_period:.1f}s\n"
    )

    if score >= 7:
        message += "\n✅ Conditions look great!"
    elif score >= 4:
        message += "\n☑️ Conditions are okay — could go either way."
    else:
        message += "\n❌ Probably not worth it today."

    return message


"""
def check_conditions(beach, min_wave):
    coords = BEACH_COORDS.get(beach)

    if not coords:
        return "Unknown beach."

    lat = coords["lat"]
    lng = coords["lng"]

    today = datetime.utcnow().isoformat()

    url = "https://api.stormglass.io/v2/weather/point"
    params = {
        "lat": lat,
        "lng": lng,
        "params": "waveHeight,windSpeed,windDirection,swellPeriod",
        "start": today,
        "end": today,
        "source": "noaa"
    }

    headers = {
        "Authorization": API_KEY
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return f"Error: {response.text}"

    data = response.json()

    try:
        forecast = data["hours"][0]  # First hourly forecast

        wave_height = forecast["waveHeight"]["noaa"]
        wind_speed = forecast["windSpeed"]["noaa"]
        wind_direction = forecast["windDirection"]["noaa"]
        swell_period = forecast["swellPeriod"]["noaa"]

        # You can adjust these thresholds
        good_wind = wind_speed <= 8  # knots
        good_swell = swell_period >= 10  # seconds

        if wave_height >= min_wave and good_wind and good_swell:
            return (
                f"🌊 Good conditions at {beach}!\n"
                f"Wave height: {wave_height:.1f}m\n"
                f"Wind: {wind_speed:.1f} knots, dir: {wind_direction:.0f}°\n"
                f"Swell period: {swell_period:.1f}s"
            )
        else:
            return (
                f"😕 Not ideal at {beach}:\n"
                f"Wave: {wave_height:.1f}m\n"
                f"Wind: {wind_speed:.1f} knots\n"
                f"Swell: {swell_period:.1f}s"
            )

    except Exception as e:
        return f"Error processing data: {e}"
"""