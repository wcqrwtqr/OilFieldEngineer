from logging import debug
from flask import Flask, render_template, redirect, request, url_for
import os
from flask_sqlalchemy import SQLAlchemy
import aiohttp
import asyncio

app = Flask(__name__)
# app.config['SECRET_KEY'] =  os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = "changeme"

# Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
API_KEY = 'e94793880287043b0eed08919e5c2505'
# WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
# WEATHER_API_URL = 'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=hourly,daily&appid={api_key}'
# WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=e94793880287043b0eed08919e5c2505'
# 'https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid=e94793880287043b0eed08919e5c2505'
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'

# async def get_weather_data(city):
async def get_weather_data(lat, lon):
    async with aiohttp.ClientSession() as session:
        # url = WEATHER_API_URL.format(city=city, api_key=API_KEY)
        url = WEATHER_API_URL.format(lat=lat, lon=lon, api_key=API_KEY)
        print(url)
        async with session.get(url) as response:
            data = await response.json()
            return data

@app.route('/weather', methods=['GET', 'POST'])
async def weather():
    if request.method == 'POST':
        # city = request.form['city']
        lat = request.form['lat']
        lon = request.form['lon']
        # if city:
        if lat:
            try:
                # weather_data = await get_weather_data(city)
                weather_data = await get_weather_data(lat, lon)
                print(weather_data)
                weather_info = {
                    # 'city': city,
                    'description': weather_data['weather'][0]['description'],
                    'temperature': weather_data['main']['temp'],
                    'humidity': weather_data['main']['humidity'],
                    'name' : weather_data['name'],
                    'country' : weather_data['sys']['country'],
                }
                return render_template('weather_results.html', weather=weather_info)
            except KeyError:
                error_msg = f"Could not find weather data for {lat}."
                return render_template('error.html', error=error_msg)
    return render_template('weather.html')

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/conversion_temperature", methods=['GET', 'POST'])
def conversion_Temperature():
    if request.method == 'POST':
        input_val = float(request.form['inputval'])
        choice = request.form['selected_temp']
        if choice == '1':
            # Convert F to C
            result = format((input_val * 9/5 + 32), '.2f')
        elif choice == '2':
            # Convert C to F
            result = format(((input_val - 32) * 5/9), '.2f')
        else:
            result = 0

        return render_template("conversion_temperature.html", result=result, input_val=input_val, choice=choice)
    return render_template("conversion_temperature.html")

@app.route("/conversion_pressure", methods=['GET', 'POST'])
def conversion_pressure():
    if request.method == 'POST':
        input_val = float(request.form['inputval'])
        choice = request.form['selected_pressure']
        if choice == '1':
            # psi to bar
            result = format((input_val / 14.5), '.2f')
        elif choice == '2':
            # bar to psi
            result = format((input_val * 14.5), '.2f')
        else:
            result = 0

        return render_template("conversion_pressure.html", result=result, input_val=input_val, choice=choice)
    return render_template("conversion_pressure.html")

@app.route("/simulation", methods=['GET', 'POST'])
def simulation():
    return render_template("simulation.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
