import logging
import os
import platform
import sys
from datetime import datetime, timedelta, timezone

import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(message)s")


def get_system_info() -> dict:
    return {
        "os_name": platform.system(),
        "os_release": platform.release(),
        "python_version": platform.python_version(),
    }


def fetch_weather_data(city_name: str, api_key: str) -> dict:
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": api_key, "units": "metric", "lang": "ua"}

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            logging.error(f"Error: City '{city_name}' not found.")
        elif response.status_code == 401:
            logging.error("Error: Invalid API Key.")
        else:
            logging.error(f"HTTP Error: {err}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error occurred: {e}")
        sys.exit(1)


def format_timezone(offset_seconds: int) -> str:
    hours = offset_seconds // 3600
    minutes = (abs(offset_seconds) % 3600) // 60
    return f"UTC{hours:+03d}:{minutes:02d}"


def process_and_display_weather(data: dict, user_city: str):
    db_city = data.get("name", "Unknown")

    tz_offset_sec = data.get("timezone", 0)
    tz_str = format_timezone(tz_offset_sec)

    target_tz = timezone(timedelta(seconds=tz_offset_sec))
    local_time = datetime.now(target_tz)

    sys_data = data.get("sys", {})
    sunrise = sys_data.get("sunrise", 0)
    sunset = sys_data.get("sunset", 0)
    day_duration_sec = sunset - sunrise

    duration_hours = day_duration_sec // 3600
    duration_minutes = (day_duration_sec % 3600) // 60

    weather_desc = (
        data["weather"][0]["description"] if data.get("weather") else "No description"
    )
    main_data = data.get("main", {})
    wind_data = data.get("wind", {})

    print(f"\nПогода у місті {user_city.capitalize()} (База: {db_city}):")
    print(f"Часова зона: {tz_str}")
    print(
        f"Дата і час запиту (локальний час міста): {local_time.strftime('%Y-%m-%d %H:%M')}"
    )
    print(f"Тривалість дня: {duration_hours:02d}:{duration_minutes:02d} (г:хв)")
    print(f"Опис: {weather_desc}")
    print(
        f"Температура: {main_data.get('temp', 0)}°C (відчувається як {main_data.get('feels_like', 0)}°C)"
    )
    print(f"Вологість: {main_data.get('humidity', 0)}%")
    print(f"Швидкість вітру: {wind_data.get('speed', 0)} м/с\n")


def main():
    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY")

    sys_info = get_system_info()
    print(f"Операційна система: {sys_info['os_name']}")
    print(f"Версія ядра/системи: {sys_info['os_release']}")
    print(f"Python: {sys_info['python_version']}\n")

    if not api_key:
        logging.error(
            "CRITICAL: OPENWEATHER_API_KEY is not set in environment variables."
        )
        sys.exit(1)

    try:
        user_city = input("Введіть назву міста: ").strip()
        if not user_city:
            raise ValueError("City name cannot be empty.")

        weather_data = fetch_weather_data(user_city, api_key)
        process_and_display_weather(weather_data, user_city)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting gracefully...")
        sys.exit(0)
    except ValueError as ve:
        logging.error(f"Input Error: {ve}")


if __name__ == "__main__":
    main()
