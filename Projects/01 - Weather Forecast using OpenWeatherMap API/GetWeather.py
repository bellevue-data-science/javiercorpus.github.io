# GetWeather.py
# Purpose: Get the weather of a given city/zip code
# Author: Javier Corpus
# Changelog:
# 11/03/2024 - Initial version

import json
import requests
import math
import re
import os
from requests.exceptions import (
    HTTPError,
    ConnectionError,
    Timeout,
    RequestException
)

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENMAP_API_KEY")                                 

# Constants:

GEOCODING_CITY_URL = 'https://api.openweathermap.org/geo/1.0/direct'
GEOCODING_ZIP_URL = 'https://api.openweathermap.org/geo/1.0/zip'
CURRENT_WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
HORIZONTAL_LINE = "-" * 80

# Global variables:
weather_unit = "imperial"
weather_info = {}
location = ""


# --------------------------------------------
# This function returns latitude and longitude
# of a given location (city/state/country)
# --------------------------------------------
def get_lat_lon_city(city: str):
    try:
        print(HORIZONTAL_LINE)
        print(f"Contacting Web Service to get coordinates for {city}...")
        geocoding_city_params = {'q': city, 'appid': API_KEY}
        geocoding_city_response = requests.get(GEOCODING_CITY_URL,
                                               geocoding_city_params)
        geocoding_city_data = geocoding_city_response.json()

        if geocoding_city_response.status_code == 200:
            print("Connection to web service successful.")

        if geocoding_city_response.text == "[]":
            # If Lat/Lon was not found for that city:
            return None

        else:
            # Lat/Lon found
            global location
            location = city
            return (geocoding_city_data[0]['lat'],
                    geocoding_city_data[0]['lon'])

    except HTTPError as http_error:
        # e.g., 404 Not Found
        print(f"\nAn HTTP error occurred: \n\n{http_error}")
        return None
    except ConnectionError as connection_error:
        # e.g., Network issues
        print(f"\nConnection error occurred. Please check your Internet "
              f"connection: \n\n{connection_error}")
        return None
    except Timeout:
        # e.g., Request timeout
        print("\nThe request has timed out")
        return None
    except RequestException as request_error:
        # Catch-all other request exceptions
        print(f"\nAn error occurred: \n\n{request_error}")
        return None
    except Exception as other_error:
        # Catch-all for other exceptions
        print(f"\nAn unexpected error occurred: \n\n{other_error}")


# -------------------------------------------------------------------------
# This function returns latitude and longitude of a given zip code/country
# -------------------------------------------------------------------------
def get_lat_lon_zip(zip_code: str):
    try:
        print(HORIZONTAL_LINE)
        print(f"Contacting Web Service to get coordinates for "
              f"zip code {zip_code}...")
        geocoding_zip_params = {'zip': zip_code, 'appid': API_KEY}
        geocoding_zip_response = requests.get(GEOCODING_ZIP_URL,
                                              geocoding_zip_params)

        if geocoding_zip_response.status_code != 200:
            # Lat/Lon not found for the given zip code

            if geocoding_zip_response.status_code == 404:
                print(f"Connection to web service successful, "
                      f"but no data found.")

            return None

        else:
            # Lat/Lon found
            print("Connection to web service successful.")
            geocoding_zip_data = geocoding_zip_response.json()
            global location
            location = f"zip code: {zip_code}"
            return geocoding_zip_data['lat'], geocoding_zip_data['lon']

    except HTTPError as http_error:
        # e.g., 404 Not Found
        print(f"\nAn HTTP error occurred: \n\n{http_error}")
        return None
    except ConnectionError as connection_error:
        # e.g., Network issues
        print(f"\nConnection error occurred. Please check your Internet "
              f"connection: \n\n{connection_error}")
        return None
    except Timeout:
        # e.g., Request timeout
        print("\nThe request has timed out")
        return None
    except RequestException as request_error:
        # Catch-all other request exceptions
        print(f"\nAn error occurred: \n\n{request_error}")
        return None
    except Exception as other_error:
        # Catch-all for other exceptions
        print(f"\nAn unexpected error occurred: \n\n{other_error}")


# ------------------------------------------------
# Main menu. Ask the user if they want to look up
# a city/state/country, a zip code, or quit
# ------------------------------------------------
def get_user_input():
    print("┌───────────────────────────────────────────────────────────┐")
    print("│                          MENU                             │")
    print("├───────────────────────────────────────────────────────────┤")
    print(f"│ 1 - Change weather units. Current selection: {weather_unit}",
          end="")
    print(" " * (12 - len(weather_unit)), "│")
    print("│ 2 - Lookup by City/State/Country.                         │")
    print("│ 3 - Lookup by Zip Code/Country.                           │")
    print("│ 4 - Show examples of how to use this program              │")
    print("│ 5 - Quit this program.                                    │")
    print("└───────────────────────────────────────────────────────────┘")

    user_input = input("\n   Please select an option: ")
    if user_input in ["1", "2", "3", "4", "5"]:
        return user_input
    else:
        return None


# ------------------------------------------------
# Print usage examples, explain different options.
# ------------------------------------------------
def usage_examples():
    print("\nUsage examples: ")
    print(HORIZONTAL_LINE)

    print("1 - Change weather units: Use this option to choose between "
          "Imperial (°F), Metric (°C) or Standard (°K).")

    print("2 - Lookup by city/state/country: Use this option to get the "
          "weather for the location specified. City and country are "
          "required, state is optional. For the US, state is required."
          "\n      Examples:"
          "\n       - Paris, FR"
          "\n       - Bellevue, NE, US")

    print("3 - Lookup by zip code/country: Use this option to get the "
          "weather for the zip code specified. Zip code and country are "
          "required."
          "\n      Examples:"
          "\n       - E14, GB"
          "\n       - 68005, US")

    print("4 - Print this help message.")
    print("5 - Quit this program.")


# --------------------------------------------
# Change the units used to display the weather
# --------------------------------------------
def set_weather_units():
    global weather_unit
    while True:

        print("┌──────────────────────────────┐")
        print(f"│ Current unit: {weather_unit}", end="")
        print(" " * (14 - len(weather_unit)), "│")
        print("├──────────────────────────────┤")
        print("│ 1 - Imperial (°F)            │")
        print("│ 2 - Metric (°C)              │")
        print("│ 3 - Standard (°K).           │")
        print("└──────────────────────────────┘")

        user_selection = input("\n   Select units to display the "
                               "temperature: ")
        if user_selection == "1":
            weather_unit = "imperial"
            break
        elif user_selection == "2":
            weather_unit = "metric"
            break
        elif user_selection == "3":
            weather_unit = "standard"
            break
        else:
            print("\n ----> Invalid input. Please enter 1, 2, or 3.")

    print(f"\n ----> Weather units changed to {weather_unit}")


# ------------------------------------
# Prints rows with weather information
# ------------------------------------
def print_table_row(str_param1: str, value_param1: str, str_param2: str,
                    value_param2: str, half_length_table: int):
    print(f"║ {str_param1:<{len(str_param1)}}", end="")
    print(" " * (half_length_table - len(str_param1)
                 - len(value_param1) - 2), end="")
    print(f"{value_param1} ║", end="")

    print(f" {str_param2:<{len(str_param2)}}", end="")
    print(" " * (half_length_table - len(str_param2)
                 - len(value_param2) - 2), end="")
    print(f"{value_param2} ║")


# -------------------------------------------------------------------
# Displays a table with the weather information for the given location
# -------------------------------------------------------------------
def print_weather_info(weather_info_dict: dict, unit: str):
    match unit:
        case "imperial":
            weather_symbol = "°F"
            wind_speed = "miles/hour"
        case "metric":
            weather_symbol = "°C"
            wind_speed = "meters/second"
        case "standard":
            weather_symbol = "°K"
            wind_speed = "meters/second"
        case _:  # Used to supress warning: var referenced before assignment
            weather_symbol = "°F"
            wind_speed = "miles/hour"

    # Defining strings to be used with dynamic print statements
    title = f"Displaying weather information for {location}"
    str_temperature = "Temperature"
    str_conditions = "Conditions"
    str_current = "Current:"
    str_feels_like = "Feels like:"
    str_min = "Min:"
    str_max = "Max:"
    str_description = "Description:"
    str_humidity = "Humidity:"
    str_wind_speed = "Wind speed:"
    str_pressure = "Pressure:"

    value_current = f"{weather_info_dict['main']['temp']}{weather_symbol}"
    value_feels_like = (f"{weather_info_dict['main']['feels_like']}"
                        f"{weather_symbol}")
    value_min = f"{weather_info_dict['main']['temp_min']}{weather_symbol}"
    value_max = f"{weather_info_dict['main']['temp_max']}{weather_symbol}"
    value_pressure = f"{weather_info_dict['main']['pressure']} hPa"
    value_description = f"{weather_info_dict['weather'][0]['description']}"
    value_humidity = f"{weather_info_dict['main']['humidity']}%"
    value_wind_speed = f"{weather_info_dict['wind']['speed']} {wind_speed}"

    length_table = len(title) + 25

    # Defining a minimum length to display the weather table
    if length_table < 73:
        length_table = 73

    if length_table % 2 == 0:
        length_table += 1

    half_length_table = math.floor(length_table / 2)

    print(HORIZONTAL_LINE)

    # --------------------------------------------------
    # Start of the weather table. This table is dynamic,
    # it changes with the width of the text
    # ---------------------------------------------------

    # Row - Table header / Location information
    print("╔", end="")
    print("═" * length_table, end="")
    print("╗")
    print(f"║{title:^{length_table}}║")

    print("╠", end="")
    print("═" * half_length_table, end="")
    print("╦", end="")
    print("═" * half_length_table, end="")
    print("╣")

    # Row - Temperature / Conditions
    print(f"║{str_temperature:^{half_length_table}}║"
          f"{str_conditions:^{half_length_table}}║")
    print("╠", end="")
    print("═" * half_length_table, end="")
    print("╬", end="")
    print("═" * half_length_table, end="")
    print("╣")

    # Row - Current / Description
    print_table_row(str_current, value_current, str_description,
                    value_description, half_length_table)

    # Row - Feels Like / Humidity
    print_table_row(str_feels_like, value_feels_like, str_humidity,
                    value_humidity, half_length_table)

    # Row - Min / Wind Speed
    print_table_row(str_min, value_min, str_wind_speed,
                    value_wind_speed, half_length_table)

    # Row - Max / Pressure
    print_table_row(str_max, value_max, str_pressure,
                    value_pressure, half_length_table)

    # End of table:
    print("╚", end="")
    print("═" * half_length_table, end="")
    print("╩", end="")
    print("═" * half_length_table, end="")
    print("╝")


# -------------------------------------------------------------
# This function returns the weather based on the given location
# -------------------------------------------------------------
def get_current_weather(lat: float, lon: float, unit: str):
    try:
        print(HORIZONTAL_LINE)
        print(f"Contacting Web Service to get weather for {lat}, {lon}...")

        current_weather_params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY,
            'units': unit
        }

        current_weather_response = requests.get(CURRENT_WEATHER_URL,
                                                current_weather_params)

        global weather_info
        weather_info = json.loads(current_weather_response.text)

        if weather_info:
            print("Connection to web service successful.")
            print_weather_info(weather_info, unit)

    except HTTPError as http_error:
        # e.g., 404 Not Found
        print(f"\nAn HTTP error occurred: \n\n{http_error}")
        return None
    except ConnectionError as connection_error:
        # e.g., Network issues
        print(f"\nConnection error occurred. Please check your Internet "
              f"connection: \n\n{connection_error}")
        return None
    except Timeout:
        # e.g., Request timeout
        print("\nThe request has timed out")
        return None
    except RequestException as request_error:
        # Catch-all other request exceptions
        print(f"\nAn error occurred: \n\n{request_error}")
        return None
    except Exception as other_error:
        # Catch-all for other exceptions
        print(f"\nAn unexpected error occurred: \n\n{other_error}")


# ------------------------------------
# Get city/state/county from the user
# ------------------------------------
def get_city():
    print("┌──────────────────────────────────┐")
    print("│ 2 - Lookup by City/State/Country │")
    print("└──────────────────────────────────┘")

    # Get City
    while True:
        city = input("   Enter city name: ")

        # Validate city name. It can contain only letters and blank spaces
        if re.fullmatch(r"[a-zA-Z ]+", city):
            break
        else:
            print(" ----> ERROR: Please enter a valid city name only.")
            continue

    # Get State (optional, unless it's the US)
    while True:
        state = input("   Enter state, or <enter> for none: ")
        if re.fullmatch(r"[a-zA-Z ]+", state) or state == "":
            break
        else:
            print(" ----> ERROR: Please enter a valid state only.")
            continue

    # Get Country. If it's the US, check for a valid state
    while True:
        country = input("   Enter two letter country code (e.g. US): ")
        if country.upper() == "US" and (state == "" or len(state) > 2):
            print(f" ----> ERROR: For US, a two-letter state is required "
                  f"(e.g. NY).")
            while True:
                state = input("Enter state (e.g. NY): ")
                if state.isalpha() and len(state) == 2:
                    break
                else:
                    print(f" ----> ERROR: Please enter a valid state "
                          f"(two letter code).")
                    continue

        if country.isalpha() and len(country) == 2:
            break
        else:
            print(" ----> ERROR: Please enter a valid country code only.")
            continue

    # Capitalize City, State and Country
    if state:
        if len(state) == 2:
            state = state.upper()
        else:
            state = state.title()
        place = ",".join([city.title(), state, country.upper()])
    else:
        place = ",".join([city.title(), country.upper()])

    return place


# ----------------------------------
# Get zip code/country from the user
# ----------------------------------
def get_zip_code():
    print("┌──────────────────────────────────┐")
    print("│ 3 - Lookup by zip code/Country.  │")
    print("└──────────────────────────────────┘")

    while True:
        zip_code = input("   Enter zip code: ")
        if zip_code.isalnum():
            break
        else:
            print(" ----> ERROR: Please enter a valid zip code only.")
            continue

    while True:
        country = input("   Enter two letter country code (e.g. US): ")
        if country.isalpha() and len(country) == 2:
            break
        else:
            print(" ----> ERROR: Please enter a valid country code only.")
            continue

    place = ",".join([zip_code, country.upper()])

    return place


# ------------------------------------
# Main function
# ------------------------------------
def main():
    while True:
        user_input = get_user_input()

        # 1 - Change weather units
        if user_input == "1":
            set_weather_units()

        # 2 - Lookup by City/State/County
        elif user_input == "2":
            city = get_city()
            if city:
                coords = get_lat_lon_city(city)
                if coords is not None:
                    param_lat, param_lon = coords
                    get_current_weather(param_lat, param_lon, weather_unit)

                else:
                    print(f"{HORIZONTAL_LINE}")
                    print(f" ----> Data not found for city {city}. "
                          f"Make sure to enter a valid city/state/country "
                          f"combination, or check your Internet "
                          f"connection.")
            else:
                print(" ----> ERROR: Please enter city, state, country")

        # 3 - Lookup by zip code/Country
        elif user_input == "3":
            zip_code = get_zip_code()
            if zip_code:
                coords = get_lat_lon_zip(zip_code)
                if coords is not None:
                    param_lat, param_lon = coords

                    get_current_weather(param_lat, param_lon, weather_unit)

                else:
                    print(f"{HORIZONTAL_LINE}")
                    print(f" ----> Data not found for zip code {zip_code}. "
                          f"Make sure to enter a valid zip code/country "
                          f"combination, or check your Internet connection.")

        # 4 - Show examples of how to use this program
        elif user_input == "4":
            usage_examples()

        # 5 - Quit this program
        elif user_input == "5":

            print("\n▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░")
            print("┌──────────────────────────────────────────────┐")
            print("│ Thank you for using this program! Quitting...│")
            print("└──────────────────────────────────────────────┘")

            exit()
        else:
            print("\n ----> ERROR: Invalid input. "
                  "Please enter 1, 2, 3, 4 or 5")


# ---------
# Main body
# ---------
if __name__ == "__main__":
    main()
