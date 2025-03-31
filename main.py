import requests
import matplotlib.pyplot as plt
from datetime import datetime

# 🌎 API Key & Location
API_KEY = "241afeb4b9c30f7efa3f3eb048427cd7"  # Your OpenWeatherMap API key
CITY = "Verona, US"

# 🌤️ API Endpoints
CURRENT_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

# 🌥️ API Request Parameters
params = {
    "q": CITY,
    "appid": API_KEY,
    "units": "imperial"  # "metric" for Celsius
}

# 🚀 Fetch Current Weather & Forecast
current_response = requests.get(CURRENT_URL, params=params)
forecast_response = requests.get(FORECAST_URL, params=params)

if current_response.status_code == 200 and forecast_response.status_code == 200:
    current_data = current_response.json()
    forecast_data = forecast_response.json()

    # 🌤️ Extract Current Weather
    current_temp = current_data["main"]["temp"]
    current_humidity = current_data["main"]["humidity"]
    current_weather = current_data["weather"][0]["description"]
    current_time = datetime.now().strftime("%a %I:%M %p")

    # 🌥️ Extract Forecast Data
    dates = [current_time]
    temps = [current_temp]
    humidities = [current_humidity]
    descriptions = [f"{datetime.now().strftime('%A %I%p')} {current_weather}"]

    for forecast in forecast_data["list"][:56]:  # 7 days (every 3 hours = 56 entries)
        dt_txt = forecast["dt_txt"]
        temp = forecast["main"]["temp"]
        humidity = forecast["main"]["humidity"]
        weather = forecast["weather"][0]["description"]

        # Convert to readable date format
        date_obj = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
        dates.append(date_obj.strftime("%a %I:%M %p"))
        temps.append(temp)
        humidities.append(humidity)

        # Append to paragraph-style description
        descriptions.append(f"{date_obj.strftime('%A %I%p')} {weather}")

    # 📈 Plotting the graph with cloudy blue background
    fig, ax1 = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor("#d0e4f7")  # Cloudy blue background

    # 🌡️ Temperature Line
    ax1.plot(dates, temps, marker='o', color='royalblue', label='Temperature (°F)', linewidth=2)

    # 💦 Humidity Line
    ax1.plot(dates, humidities, marker='s', color='orange', label='Humidity (%)', linestyle='-.', linewidth=1.5)

    # 🎯 Labels & Titles
    ax1.set_xlabel("Date & Time", fontsize=12, fontweight='bold', color='#333')
    ax1.set_ylabel("Temperature (°F) & Humidity (%)", fontsize=12, fontweight='bold', color='#333')
    plt.title("Weather BRO", fontsize=20, fontweight='bold', color='#222')

    # 🛠️ Styling
    plt.xticks(rotation=45, fontsize=10, color='#555')
    plt.yticks(fontsize=10, color='#555')

    # 🎯 Grid & Legends
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    ax1.legend(loc='upper left')

    # 🔥 Beautify layout
    plt.tight_layout()
    plt.show()

    # 📜 Print the paragraph-style description
    print("\n🌥️ **7-Day Weather Description:**")
    print(", ".join(descriptions))

else:
    print(f"Failed to retrieve data: {current_response.status_code}, {forecast_response.status_code}")