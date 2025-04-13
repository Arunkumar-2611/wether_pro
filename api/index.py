from flask import Flask, request, render_template
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_api_key = "5be7cb07d96d28f23a74b4f584b2f2de"
        location = request.form.get("location")
        complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={user_api_key}"
        api_link = requests.get(complete_api_link)
        api_data = api_link.json()

        if api_link.status_code != 200 or api_data.get("cod") != 200:
            return render_template("index.html", error="Invalid city name or unable to fetch weather data.")
        else:
            location = api_data['name']
            temp_city = api_data['main']['temp'] - 273.15
            weather_desc = api_data['weather'][0]['description']
            hmdt = api_data['main']['humidity']
            wind_speed = api_data['wind']['speed']
            date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
            day = datetime.now().strftime("%A")

            return render_template("weather.html",
                                   location=location,
                                   day=day,
                                   date_time=date_time,
                                   temp_city=round(temp_city),
                                   weather_desc=weather_desc,
                                   hmdt=hmdt,
                                   wind_speed=wind_speed)

    return render_template("home.html")

# Vercel handler
def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)

if __name__ == "__main__":
    app.run(debug=True)
