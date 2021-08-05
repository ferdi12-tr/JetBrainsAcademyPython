from flask import Flask, render_template, request
import requests
import sys
import json
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import abort, redirect, url_for

API_key = "5a06af075345ab2460f215b788e49541"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"City('{self.name}')"


@app.route("/")
def index():
    dict_list = []
    city_list = City.query.all()
    for city in city_list:
        data = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city.name}&units=metric&appid={API_key}")
        datas = json.loads(data.text)
        date = datetime.datetime.utcnow() + datetime.timedelta(seconds=datas['timezone'])
        date_time = date.time().hour

        if date_time < 6:
            background = "card evening-morning"
        elif 6 < date_time < 18:
            background = "card day"
        elif 18 < date_time < 24:
            background = "card night"

        dict_with_weather_info = [{"degrees": datas["main"]["temp"], "state": datas["weather"][0]["main"],
                                   "city": datas["name"], "background": background}]
        dict_list.append(dict_with_weather_info)
    return render_template("index.html", weathers=dict_list)


@app.route("/", methods=["POST"])
def add_city():
    get_city_name = request.form["city_name"]
    db.session.add(City(name=get_city_name))
    db.session.commit()
    return redirect(url_for("index"))


# don't change the following way to run flask:
if __name__ == '__main__':
    db.create_all()
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
