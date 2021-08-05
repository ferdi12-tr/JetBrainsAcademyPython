from flask import Flask, render_template, request
import requests
import sys
import json
import datetime

API_key = "5a06af075345ab2460f215b788e49541"
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def add_city():
    city_name = request.form["city_name"]
    data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={API_key}")
    datas = json.loads(data.text)

    date = datetime.datetime.utcnow() + datetime.timedelta(seconds=datas['timezone'])
    date_time = date.time().hour  # set a background image according to the current city time

    if date_time < 6:
        background = "card evening-morning"
    elif 6 < date_time < 18:
        background = "card day"
    elif 18 < date_time < 24:
        background = "card night"

    dict_with_weather_info = [{"degrees": datas["main"]["temp"], "state": datas["weather"][0]["main"],
                               "city": datas["name"]}]

    return render_template("index.html", weathers=dict_with_weather_info, background=background)


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
