import requests
import json

class WeatherDay:
    def __init__(self, name, temp, wSpeed, wDir, dForecast, hurl):
        self.name = name
        self.temp = temp
        self.wSpeed = wSpeed
        self.wDir = wDir
        self.dForecast = dForecast
        self.hourly_url = hurl

    def get_hourly(self):
        response = requests.get(hourly_url)



def get_weather(longitude, latitude):

    properties = json.loads(requests.get('https://api.weather.gov/points/%f,%f' % (longitude, latitude)).text)['properties']

    if properties:
        forecast_url  = properties['forecast']
        hForecase_url = properties['forecastHourly']

        response = requests.get(forecast_url)

        if response:
            forecast = json.loads(response.text)['properties']['periods']

            curr_days   = []
            week_days   = []
            week_nights = []

            # Change the string appearance.
            # Replace Night with N.
            for day in forecast:
                if day['name'] != "Today":
                    day['name'] = day['name'].replace("day", "")

                if "Wednes" in day['name']:
                    day['name'] = day['name'].replace("nes", "")
                
                if "Satur" in day['name']:
                    day['name'] = day['name'].replace("ur", "")

                day['windSpeed'] = day['windSpeed'].replace(" to ", "-")

                if day['name'] == "Today" or day['name'] == "Tonight" or day['name'] == "This Afternoon":
                    curr_days.append(WeatherDay(day['name'], day['temperature'], day['windSpeed'], day['windDirection'], day['detailedForecast'], hForecase_url))
                elif "Night" in day['name']:
                    week_nights.append(WeatherDay(day['name'], day['temperature'], day['windSpeed'], day['windDirection'], day['detailedForecast'], hForecase_url))
                else:
                    week_days.append(WeatherDay(day['name'], day['temperature'], day['windSpeed'], day['windDirection'], day['detailedForecast'], hForecase_url))
        else:
            return None
    else:
        return None

    return (curr_days, week_days, week_nights)