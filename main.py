import sqlalchemy
import jinja2
from API_Json import API_manga_functionality
from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, text, ForeignKey, insert, select, func
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import MetaData

Api_add_manga = API_manga_functionality.Api_add_manga

app = Flask(__name__)
user_manga = []
db = SQLAlchemy()

"""
Manga Class
"""


class Manga:
    def __init__(self, id, title, year, description, cover_art_id, filename, author):
        self.title = title
        self.id = id
        self.title = title
        self.year = year
        self.description = description
        self.cover_art_id = cover_art_id
        self.filename = filename
        self.author = author


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html", manga_list=user_manga)


@app.route("/add_manga", methods=["GET", "POST"])
def add_manga():
    if request.method == "POST":
        manga_title = request.form.get("manga_chosen")
        try:
            new_manga = Api_add_manga(manga_title)
            print(new_manga)
            user_manga.append(Manga(id=new_manga['id'], title=new_manga['title'], year=new_manga['year'], description=new_manga['description'], cover_art_id=new_manga['cover_art_id'], filename=new_manga['cover_art_filename'], author=new_manga['author']))
            print("works")
            return redirect(url_for("home"))

        except Exception as e:
            print(f"there was an error : {e}")

    return render_template("add_manga.html")


@app.route("/del_manga/<string:manga_id>", methods=["GET"])
def del_manga(manga_id):
    for manga in user_manga:
        if manga.id == manga_id:
            user_manga.remove(manga)

    return redirect(url_for("home"))


if __name__ in "__main__":
    app.run(host="localhost", port=5000, debug=True)
