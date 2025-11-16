## Weather Forecast using OpenWeatherMap API.

The Weather Program is a Python 3 application designed to provide users with real-time weather information for any location in the world using either city/state or zip code input. The program interacts with the OpenWeatherMap web service, performing a GEO lookup to obtain latitude and longitude before retrieving detailed weather data for the specified location. Users can choose their preferred temperature unit (Celsius, Fahrenheit, or Kelvin) and view a readable summary that includes the location, current temperature, "feels like" temperature, low/high temperatures, pressure, humidity, and a weather description (e.g., clouds).

User experience and robustness are key features of this program. Input validation ensures that incorrect or unexpected inputs are handled gracefully, preventing crashes and guiding the user to correct errors. The program is structured with multiple functions, and it leverages Python’s Requests library for web service communication. Exception handling is implemented using specific try blocks to provide meaningful feedback if a connection to the web service fails. The code follows PEP8 standards for readability and maintainability and is thoroughly commented to assist other developers in understanding and modifying the application.

To run the program, users need an OpenWeatherMap API key. The application allows multiple weather lookups per session, supporting both zip code and city/state queries. This project showcases real-world programming practices.

### Skills
 - Python 3 programming
 - Working with web APIs (OpenWeatherMap)
 - Using the Requests library for HTTP requests
 - Exception handling and error reporting (try blocks, specific exceptions)
 - Input validation and user input handling
 - Designing readable and user-friendly output formats
 - Implementing program flow with multiple functions.
 - Following coding conventions (PEP8)
 - Writing meaningful code comments
 - Understanding and applying geolocation (GEO lookup)
 - Robust handling of "non-happy path" scenarios and invalid user input
