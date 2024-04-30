import requests
import logging
from logging.handlers import RotatingFileHandler
import subprocess
from secrets import *


def run_bandit(directory="."):
    try:
        myResult = subprocess.run(["bandit", "-r", directory], capture_output=True, text=True)
        return myResult
    except FileNotFoundError:
        print("Error: Bandit is not installed. Please install it using 'pip install bandit'.")
        return None


def setup_logging():
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)

    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler = RotatingFileHandler(filename='weather_app.log', maxBytes=1024, backupCount=5)
    log_handler.setFormatter(log_formatter)
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(log_handler)
    log_handler.close()


def get_weather(zipcode, api_key):
    website = "https://api.openweathermap.org/data/2.5/forecast?"
    complete_url = f"{website}zip={zipcode},us&appid={api_key}"
    response = requests.get(complete_url)

    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Failed to retrieve weather data for zipcode: {zipcode}. Status code: {response.status_code}")
        return None


def format_weather_data(weather_data):
    if weather_data["cod"] == "200":
        forecast_list = weather_data['list']
        formatted_data = []

        for i in range(4, 24, 8):
            area_date = forecast_list[i]['dt_txt']
            curr_temp = forecast_list[i]['main']['temp']
            curr_temp = (9 / 5) * (curr_temp - 273.15) + 32
            low_temp = forecast_list[i - 4]['main']['temp_min']
            low_temp = (9 / 5) * (low_temp - 273.15) + 32
            max_temp = forecast_list[i + 4]['main']['temp_max']
            max_temp = (9 / 5) * (max_temp - 273.15) + 32
            weat_desc = forecast_list[i]['weather'][0]["description"]

            formatted_data.append({
                "date": area_date,
                "current_temp": round(curr_temp, 2),
                "low_temp": round(low_temp, 2),
                "high_temp": round(max_temp, 2),
                "weather_description": weat_desc
            })

        return formatted_data
    else:
        logging.error(f"Invalid data in the response: {weather_data}")
        return None


def main():
    setup_logging()
    zipcode = input("Enter zipcode: ")
    logging.info(f"Fetching weather data for zipcode: {zipcode}")

    weather_data = get_weather(zipcode, api_key)

    if weather_data:
        formatted_data = format_weather_data(weather_data)
        if formatted_data:
            for data in formatted_data:
                print(f"The zip code location is: {zipcode}")
                print(f"The date is: {data['date']}")
                print(f"The Temperature is {data['current_temp']}°F")
                print(f"with a high of {data['high_temp']}°F")
                print(f"and a low of {data['low_temp']}°F")
                print(f"with {data['weather_description']}\n")
        else:
            print("Invalid data in the response.")
    else:
        print("Error in the API request.")


if __name__ == "__main__":
    main()
    result = run_bandit()
    if result:
        print(result.stdout)
        with open("bandit_report.txt", "w") as file:
            file.write(result.stdout)
        print("Bandit analysis completed. Report saved to bandit_report.txt")
    else:
        print("Bandit analysis failed.")
