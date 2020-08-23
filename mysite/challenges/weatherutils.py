import requests
import json

class WeatherDay:
    def __init__(self, name, precip, temp, wSpeed, wDir, dForecast, hurl):
        self.name = name
        self.precip = precip
        self.temp = temp
        self.wSpeed = wSpeed
        self.wDir = wDir
        self.dForecast = dForecast
        self.hourly_url = hurl

    def get_hourly(self):
        return requests.get(self.hourly_url)

def get_precip(detailedForecast):

    chance = 0

    if 'precipitation is' in detailedForecast:
        index = detailedForecast.find('precipitation is') + 17
        chance = detailedForecast[index : index + 4].replace('%', '').replace('.', '').replace(' ', '')
    
    if chance == 0:
        chance = "< 10"

    return chance

def get_weather(longitude, latitude):

    try:
        properties = json.loads(requests.get('https://api.weather.gov/points/%f,%f' % (longitude, latitude)).text)['properties']

        if properties:
            forecast_url  = properties['forecast']
            hForecase_url = properties['forecastHourly']
            relative_city = properties['relativeLocation']['properties']['city']

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
                        curr_days.append(WeatherDay(day['name'], get_precip(day['detailedForecast']), day['temperature'], day['windSpeed'], day['windDirection'], day['detailedForecast'], hForecase_url))
                    elif "Night" in day['name']:
                        day['name'] = day['name'].replace("Night", "N")
                        week_nights.append(WeatherDay(day['name'], get_precip(day['detailedForecast']), day['temperature'], day['windSpeed'], day['windDirection'], day['detailedForecast'], hForecase_url))
                    else:
                        week_days.append(WeatherDay(day['name'], get_precip(day['detailedForecast']), day['temperature'], day['windSpeed'], day['windDirection'], day['detailedForecast'], hForecase_url))
                
                result = (curr_days, week_days, week_nights, relative_city)
                
            else:
                return "No response from second api request"
        else:
            return "No response from first api request"

    except:
        result = "Json was invalid"

    return result

    