from flask import Flask, render_template, request
from weather import get_weather
from waitress import serve

app = Flask(__name__)   

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/weather')
def weather():
    city = request.args.get('city')
    if not bool(city.strip()):
        city = "Old Saybrook"
    weather_data = get_weather(city)

    # City is not found by API
    if not weather_data['cod'] == 200:
        return render_template('error.html', title="Error", message=weather_data['message'])

    return render_template('weather.html', title=weather_data['name'], status=weather_data['weather'][0]['description'].capitalize(), temp=f"{weather_data['main']['temp']:.2f}", feels_like=f"{weather_data['main']['feels_like']:.2f}", wind_speed=f"{weather_data['wind']['speed']:.2f}", wind_direction=f"{weather_data['wind']['deg']}°")

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)