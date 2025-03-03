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


#* GUI
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # BG
        self.title('Python Weather app')
        self.eval('tk::PlaceWindow . center')
        self.resizable(width=False, height=False)
        self.geometry('350x180')
        self.grid_columnconfigure((0, 1, 2), weight=5)
        self.grid_rowconfigure((0, 1, 2), weight=5)

        # Text
        self.label = customtkinter.CTkLabel(self, text='Прогноз погоды:', font=('Arial', 18))
        self.label.grid(column=0 , row=0, sticky='w', padx=10, pady=4)

        self.weather_label = customtkinter.CTkLabel(self, text='', justify='left')
        self.weather_label.grid(row=1, column=0, sticky='w', padx=10)

        # Input boxes
        self.entry_city = customtkinter.CTkEntry(self, width=200, height=30, corner_radius=10, placeholder_text='Введите имя вашего города.')
        self.entry_city.grid(padx=5, pady=3, row=3, sticky='w')

        self.entry_code = customtkinter.CTkEntry(self, width=200, height=30, corner_radius=10, placeholder_text='Введите код вашей страны.')
        self.entry_code.grid(padx=5, row=4, column=0, sticky='w')

        # Buttons
        self.button = customtkinter.CTkButton(self, text='Узнать погоду', command=self.event, width=200, height=30)
        self.button.grid(padx=5, pady=5, row=5, column=0, sticky='w')
        
    # Functions

    def event(self):
        self.lat, self.lon = self.geocalc(self.entry_city.get(), self.entry_code.get())
        self.temp, self.desc = self.get_weather(self.lat, self.lon)
        return self.weather_label.configure(text=f'Температура: {self.temp}°С\nПогода: {self.desc}')

    def geocalc(self, city_name, country_code):
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
    def get_weather(self, lat, lon):
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


app = App()

if __name__ == '__main__':
    app.mainloop()