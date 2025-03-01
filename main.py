import requests
import json
import customtkinter
from configparser import ConfigParser

#! YOU NEED YOUR OWN API FROM OPENWEATHERMAP API 2.5

#* API
config_file = "config.ini"
config = ConfigParser() 
config.read(config_file) 
api = config['gfg']['api']

# Gets lat and lon of city from an API
def geocalc(city_name, country_code):
    geocalc = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}, {country_code}&appid={api}")
    location_response = json.dumps(geocalc.json(), indent=4)
    with open("location.json", "w") as outfile2:
        outfile2.write(location_response)
    with open("location.json", "r") as report2:
        location = json.load(report2)
    if location and isinstance(location, list):
        lat = location[0]['lat']
        lon = location[0]['lon']
        if lat and lon is not None:
            return lat, lon
    else:
        print('Error: Invalid API data structure')

# Gets weather and temperature from API
def get_weather(lat, lon):
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api}&units=metric&lang=ru")
    weather_response = json.dumps(response.json(), indent=4)
    with open("weather.json", "w") as outfile:
        outfile.write(weather_response)
    with open("weather.json", "r") as report:
        weather = json.load(report)
    if isinstance(weather, dict):
        main_data = weather.get('main')
        weather_data = weather.get('weather')
        temp = None
        desc = None
        if main_data and isinstance(main_data, dict):
            temp = int(main_data.get('temp'))
        if weather_data and isinstance(weather_data, list):
            desc = weather_data[0].get('description')
        return temp, desc   
    print("Error: Invalid API data structure")
    return None

city_name = str(input('Enter your city name:\n'))
country_code = str(input('Enter your country code(ISO-3166 format):\n'))
if city_name and country_code != '':
    lat, lon = geocalc(city_name,country_code)
    temp, desc = get_weather(lat, lon)
    print(f"Температура: {temp}°С, Погода: {desc}")


# TODO: Decent looking GUI

# lass App(customtkinter.CTk):
#     def __init__(self):
#         super().__init__()
#        
#         self.title('Python Weather app')
#         self.geometry('350x100')
#         self.grid_columnconfigure((0, 1), weight=1)
#         self.grid_rowconfigure((0, 1), weight=1)
#        
#         self.button = customtkinter.CTkButton(self, text='Get weather', command=self.get_weather(), width=150, height=30)
#         self.button.grid(padx=5, pady=5, row=2, column=0, sticky='w')
#        
#     # Getting weather from an API
#     def get_weather(self):
#         # weather_response = json.dumps(response.json(), indent=4)
#         # with open("weather.json", "w") as outfile:
#         #     outfile.write(weather_response)
#         with open("weather.json", "r") as report:
#             weather = json.load(report)
#         if isinstance(weather, dict):
#             main_data = weather.get('main')
#             weather_data = weather.get('weather')
#             temp = None
#             desc = None
#             if main_data and isinstance(main_data, dict):
#                 temp = main_data.get('temp')
#             if weather_data and isinstance(weather_data, list):
#                 desc = weather_data[0].get('description')
#             return {
#                 'Temperature': temp , 
#                 'Weather': desc   
#             }
#         print("Error: Invalid weather data structure")
#         return None

# app = App()

# if __name__ == '__main__':
#     app.mainloop()