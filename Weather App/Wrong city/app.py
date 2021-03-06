from flask import Flask, render_template, request
import requests
import sys
import json
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import abort, redirect, url_for
from flask import flash

API_key = "????"  # create api key on https://openweathermap.org/api
app = Flask(__name__)
app.secret_key = "super secret key"
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

        if datas["cod"] != 200:
            flash("The city doesn't exist!")
            db.session.delete(city)
            db.session.commit()
            return redirect("/")

        date = datetime.datetime.utcnow() + datetime.timedelta(seconds=datas['timezone'])
        date_time = date.time().hour

        idd = city.id  # we want to replace <city_id> with id

        background = "card day"  # default card background
        if date_time < 6:
            background = "card evening-morning"
        elif 6 < date_time < 18:
            background = "card day"
        elif 18 < date_time < 24:
            background = "card night"

        dict_with_weather_info = [{"degrees": datas["main"]["temp"], "state": datas["weather"][0]["main"],
                                   "city": datas["name"], "id": idd, "background": background}]
        dict_list.append(dict_with_weather_info)
    return render_template("index.html", weathers=dict_list)


@app.route("/", methods=["POST"])
def add_city():
    get_city_name = request.form["city_name"]
    check_city = City.query.filter_by(name=get_city_name).first()  # return None if city is non exist in db
    if check_city is None:
        db.session.add(City(name=get_city_name))
        db.session.commit()
        return redirect(url_for("index"))
    else:
        flash("The city has already been added to the list!")
        return redirect("/")


@app.route('/delete/<city_id>', methods=['GET', 'POST'])
def delete(city_id):
    city = City.query.filter_by(id=city_id).first()
    db.session.delete(city)
    db.session.commit()
    return redirect('/')


@app.route("/", methods=["GET", "POST"])
def get_id():
    city_id = request.form["id"]  # when click the delete-button get the id number and redirect to delete fonk.
    return redirect(url_for("delete", city_id=city_id))


# don't change the following way to run flask:
if __name__ == '__main__':
    db.create_all()
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
