from sqlalchemy.exc import IntegrityError
import requests as requests
import sqlalchemy
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert, Column, Integer, String, select
from sqlalchemy.orm import declarative_base
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.secret_key = 'secret'
db = SQLAlchemy(app)

Base = declarative_base()


class City(db.Model):
    __tablename__ = "City"

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


@app.route('/')
def index():
    weathers = City.query.all()
    data_weathers = []

    for weather in weathers:
        print(str(weather.id) + " " + weather.name)
        data = get_city_weather(weather.name)
        data["city"] = weather.id
        data_weathers.append(data)

    return render_template("index.html", weathers=data_weathers)


@app.route('/delete/<city_id>', methods=['GET', 'POST'])
def delete(city_id):
    city = City.query.filter_by(id=city_id).first()
    db.session.delete(city)
    db.session.commit()
    return redirect('/')


@app.route('/', methods=['POST'])
def submit_city():
    city_name = request.form["city_name"]
    data = get_city_weather(city_name)
    if data["cod"] == "404":
        flash("The city doesn't exist!")
        return redirect('/')

    try:
        inserted = City(city_name)
        db.session.add(inserted)
        db.session.commit()
    except IntegrityError:
        flash("The city has already been added to the list!")
        return redirect('/')
    except Exception as e:
        print("db error", e.__class__, str(e))


    # return render_template("index.html", weather=data)
    return redirect(url_for('index'))


def get_city_weather(city_name):
    req_url = "http://api.openweathermap.org/data/2.5/weather?q=" + city_name + "&appid=removed"
    resp = requests.get(req_url)
    data = resp.json()
    return data


@app.route('/profile')
def profile():
    return 'This is profile page'


@app.route('/login')
def log_in():
    return 'This is login page'


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        if not sqlalchemy.inspect(db.get_engine()).has_table("City"):
            print('Recreating all db')
            db.create_all()
        app.run(host=arg_host, port=arg_port)
    else:
        if not sqlalchemy.inspect(db.get_engine()).has_table("City"):
            print('Recreating all db')
            db.create_all()
        app.run()
