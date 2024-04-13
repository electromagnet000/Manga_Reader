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
    def __init__(self, title):
        self.title = title


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html", manga_list=user_manga)


@app.route("/add_manga", methods=["GET", "POST"])
def add_manga():
    if request.method == "POST":
        manga_title = request.form.get("manga_chosen")
        try:
            new_manga = Manga(Api_add_manga(manga_title))
            user_manga.append(new_manga)
            return redirect(url_for("home"))

        except Exception as e:
            print(f"there was an error : {e}")


    return render_template("add_manga.html")


@app.route("/del_manga", methods=["DELETE"])
def del_manga():
    pass


@app.route("/upd_manga", methods=["POST"])
def upd_manga():
    pass


if __name__ in "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
