import time
import random
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from http.client import responses
from tkinter.font import names
import requests
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from forms import FeedbackForm
from schema import engine
from schema import Base
from poll import poll_data
from flask import Flask, render_template, request, redirect, url_for, abort
from flask.json import dumps
from time import time

app = Flask(__name__)  # main

# я дивився в ютубі додаткові речі
app.config['SECRET_KEY'] = 'qg777'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedbacks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
API_KEY = "392a36267f4eeab2b9ca07b3a4e523bf"
filename = "data.txt"

db = SQLAlchemy(app)


def weather(city, date):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    weather_data = requests.get(url).json()
    temperature = weather_data["main"]["temp"]  # тут ми отримуємо температуру
    description = weather_data["weather"][0]["description"]  # отримуємо опис погоди
    return {
        "temp": temperature,
        "description": description}


def recommend_pizza(weather_desc):
    if "clear sky" in weather_desc:
        return "Сонячно! Спробуйте нічого "
    elif "rain" in weather_desc:
        return "Дощ? Візьміть гроші"
    elif "clouds" in weather_desc:
        return "Хмарно? Рекомендуємо носок"


@app.get("/weather/")
def weather_info():
    city = "Kyiv"
    date = "2024-11-28"  # щоб працювало треба міняти дату на той день який зараз. я не знаю як зробити по іншому(
    weather_data = weather(city, date)
    pizza_recommendation = recommend_pizza(weather_data["description"])
    return render_template("weather.html", weather=weather_data, recommend=pizza_recommendation)


@app.get("/")
def home_world():
    return render_template('index.2.html')


def create_menu_table():
    connect = sqlite3.connect("database.db")
    try:
        connect.execute("""
            CREATE TABLE IF NOT EXISTS menu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                price INTEGER NOT NULL
            )
        """)
        connect.commit()
    except sqlite3.Error as e:
        print(f"Помилка при створенні таблиці: {e}")
    finally:
        connect.close()


create_menu_table()


@app.get("/menu")
def menu():
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM menu ORDER BY name")
        dishes = cursor.fetchall()
    return render_template('menu.html', dishes=dishes)


@app.get("/admin/add")
def add_dish():
    return render_template('add_pizza.html')


@app.post("/admin/add")
def submit_add_dish():
    name = request.form["name"]
    description = request.form["description"]
    price = request.form["price"]

    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO menu (name, description, price)
            VALUES (?, ?, ?)
        """, (name, description, price))
        db.commit()

    return redirect("/menu")


@app.get("/admin/edit/<int:id>")
def edit_dish(id):
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM menu WHERE id = ?", (id,))
        dish = cursor.fetchone()

    return render_template('edit_pizza.html', dish=dish)


@app.post("/admin/edit/<int:id>")
def submit_edit_dish(id):
    name = request.form["name"]
    description = request.form["description"]
    price = request.form["price"]

    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        cursor.execute("""
            UPDATE menu
            SET name = ?, description = ?, price = ?
            WHERE id = ?
        """, (name, description, price, id))
        db.commit()

    return redirect("/menu")


@app.post("/admin/delete/<int:id>")
def delete_dish(id):
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM menu WHERE id = ?", (id,))
        db.commit()

    return redirect("/menu")


@app.get("/home/")
def hello_world():
    return render_template("index3.html", title="ПіццаУпаняно")


@app.get("/login/")
def get_login():
    return render_template("login.html")


@app.post("/login/")
def post_login():
    user = request.form["name"]
    info = request.user_agent
    if user == "aboba":
        abort(401)
    if user == "admin":
        return f"Are you is {user}from {info}"
    else:
        return redirect(url_for("get_login"), code=302)


@app.get("/info/")
def info():
    return (f"URL:\n{url_for("index")}\n"
            f"{url_for("choice")}\n"
            f"{url_for("get_login")}\n"
            f"{url_for("info")}\n")


@app.errorhandler(404)
def page_not_found(error):
    return ""


max_score = 100
test_name = "Python Challenge"
students = [
    {"name": "Vlad", "score": 100},
    {"name": "Sviatoslav", "score": 99},
    {"name": "Юстин", "score": 100},
    {"name": "Viktor", "score": 79},
    {"name": "Ярослав", "score": 93},
]


@app.get('/results')
def results():
    context = {
        "title": "Results",
        "students": students,
        "test_name": test_name,
        "max_score": max_score,

    }
    return render_template("results2.html", **context)


@app.get("/add/")
def index():
    create_table()
    return render_template("index.html")


def create_table():
    connect = sqlite3.connect("database.db")
    connect.execute("""
        CREATE TABLE IF NOT EXISTS PARTICIPANTS  (name TEXT, ingredients TEXT, price INTEGER)
    """)


@app.get("/join/")
def get_join():
    return render_template("join.html")


@app.post("/join/")
def post_join():
    name = request.form["name"]
    price = request.form["price"]
    ingridients = request.form["ingridients"]
    with sqlite3.connect("database.db") as users:
        cursor = users.cursor()

        try:
            cursor.execute("""
                     CREATE TABLE IF NOT EXISTS PARTICIPANTS (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT,
                         ingredients TEXT,
                         price INTEGER
                     )
                     """)
        except sqlite3.Error as e:
            print("Помилка", e)

        data = (name, price, ingridients)
        try:
            cursor.execute("""
                    INSERT INTO PARTICIPANTS (name, ingredients, price)
                    VALUES (?, ?, ?)""", data)
            users.commit()
            pizza_id = cursor.lastrowid  # подивився документацію це потрібно для того щоб отримувати айди конкретної піцци
        except sqlite3.Error as e:
            print("Помилка", e)
            return "Виникла помилка", 500

    return redirect(url_for("pizza_details", pizza_id=pizza_id))


@app.get("/find_pizza/<int:pizza_id>")
def pizza_details(pizza_id):
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()

        try:
            cursor.execute("""
            SELECT name, price, ingredients FROM PARTICIPANTS WHERE id = ?
            """, (pizza_id,))
            pizza = cursor.fetchone()  # теж подивився в документації. це щоб отримати результат
        except sqlite3.Error as e:
            print("Помилка при зчитуванні даних:", e)
            return "Виникла помилка при зчитуванні даних з бази.", 500

    if pizza:
        return render_template("participants.html", data=[pizza])
    else:
        return "Піцу не знайдено", 404


@app.get("/participants")
def get_participants():
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM PARTICIPANTS")
            participants = cursor.fetchall()
        except sqlite3.Error as e:
            print("Помилка", e)
            return "Виникла", 500

    return render_template("participants.html", data=participants)


@app.get("/vote/")
def votess():
    return render_template("poll.html", data=poll_data)


@app.get("/poll/")
def poll():
    vote = request.args.get("field")
    if vote:
        with open(filename, "a") as out:
            out.write(vote + "\n")
            return redirect(url_for("/result"))
    return vote


@app.get("/result/")
def result():
    votes = {}
    if os.path.exists(filename):
        with open(filename, "r") as file:
            lines = file.read().splitlines()
            for vote in lines:
                if vote:
                    votes[vote] = votes.get(vote, 0) + 1

    return render_template("result.html", data=poll_data, votes=votes)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    feedback = db.Column(db.String(500), nullable=False)


@app.get('/feedback')
def feedback_get():
    form = FeedbackForm()
    return render_template('feedback.html', form=form)


@app.post('/feedback')
def feedback_post():
    form = FeedbackForm()
    if form.validate_on_submit():
        new_feedback = Feedback(name=form.name.data, feedback=form.feedback.data)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Ur feedback send succefuly!', 'success')
        return redirect(url_for('feedback_get'))
    return render_template('feedback.html', form=form)


@app.get('/feedbacks')
def feedbacks_page():
    all_feedbacks = Feedback.query.all()
    return render_template('feedbacks.html', feedbacks=all_feedbacks)


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=8010, debug=True)
