import tkinter as tk
import requests

class searchForm:
    def __init__(self, master, on_search_callback):
        self.frame = tk.Frame(master)
        self.on_search = on_search_callback

        self.search_label = tk.Label(self.frame, text="Enter city:")
        self.search_label.pack()
        self.search_entry = tk.Entry(self.frame)
        self.search_entry.pack(pady=(5, 10))
        self.search_button = tk.Button(self.frame, text="Search", command=self.search_weather)
        self.search_button.pack()

        self.frame.pack(pady=10)

    def search_weather(self):
        city = self.search_entry.get()
        self.on_search(city)

class displayArea:
    def __init__(self, master):
        self.frame = tk.Frame(master)

        self.city_label = tk.Label(self.frame, text="City:")
        self.city_label.pack()
        self.temperature_label = tk.Label(self.frame, text="Temperature:")
        self.temperature_label.pack()
        self.condition_label = tk.Label(self.frame, text="Condition:")
        self.condition_label.pack()
        self.humidity_label = tk.Label(self.frame, text="Humidity:")
        self.humidity_label.pack()
        self.wind_label = tk.Label(self.frame, text="Wind:")
        self.wind_label.pack()

        self.frame.pack(pady=10)

    def update(self, weather_data):
        self.city_label.config(text=f"City: {weather_data['city']}")
        self.temperature_label.config(text=f"Temperature: {weather_data['temperature']} °C")
        self.condition_label.config(text=f"Condition: {weather_data['condition'].capitalize()}")
        self.humidity_label.config(text=f"Humidity: {weather_data['humidity']}%")
        self.wind_label.config(text=f"Wind: {weather_data['wind']} m/s")

    def show_error(self, message):
        self.city_label.config(text=message)
        self.temperature_label.config(text="")
        self.condition_label.config(text="")
        self.humidity_label.config(text="")
        self.wind_label.config(text="")

class weatherApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Weather App")
        self.master.geometry("600x400")

        self.search_form = searchForm(master, self.fetch_and_display_weather)
        self.display_area = displayArea(master)

        self.api_key = "Enter AP Key Here"
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def fetch_and_display_weather(self, city):
        self.search_form.search_button.config(state=tk.DISABLED)
        self.display_area.city_label.config(text="Loading...")
        self.master.update_idletasks()

        city = city.strip()
        if not city:
            self.display_area.show_error("Please enter a city name.")
            self.search_form.search_button.config(state=tk.NORMAL)
            return

        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            weather_data = {
                "city": data.get("name", "N/A"),
                "temperature": data["main"]["temp"],
                "condition": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
            }

            self.display_area.update(weather_data)

        except requests.exceptions.HTTPError:
            self.display_area.show_error("City not found. Please try again.")
        except Exception as e:
            self.display_area.show_error(f"Error: {str(e)}")
        finally:
            self.search_form.search_button.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = weatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
