import sqlalchemy
import jinja2
import tkinter as tk
import os
from API_Json import API_manga_functionality
from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, text, ForeignKey, insert, select, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import MetaData

Api_add_manga = API_manga_functionality.Api_add_manga

"""
OS paths
"""
current_directory = os.path.dirname(os.path.abspath(__file__))
relative_path = os.path.join(current_directory, "sqlite_data", "User_data_manga_website.db")

"""
Global Variable
"""
app = Flask(__name__)
engine = create_engine(f"sqlite:///{relative_path}", echo=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{relative_path}"
app.config['SECRET_KEY'] = "super_secret_key"
db = SQLAlchemy()
db.init_app(app)



"""
Manga Class
"""


class Manga(db.Model):

    __tablename__ = "Manga_bookshelf"

    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    year = db.Column(db.Integer)
    description = db.Column(db.String)
    cover_art_id = db.Column(db.String)
    filename = db.Column(db.String)
    author = db.Column(db.String)

    def __repr__(self):
        return f"{self.title}"


"""
SQLITE DATA MANAGER
"""



def create_app():
    with app.app_context():
        db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    user_manga = reversed(Manga.query.all())
    return render_template("home.html", manga_list=user_manga)


@app.route("/add_manga", methods=["POST"])
def add_manga():
    if request.method == "POST":
        manga_title = request.form.get("manga_chosen")
        existing_manga = Manga.query.filter_by(title=manga_title).first()
        if existing_manga:
            flash("Movie already exists in the database.", "warning")
        else:
            try:
                new_manga = Api_add_manga(manga_title)
                if new_manga:
                    print(new_manga)
                    manga = Manga(id=new_manga['id'], title=new_manga['title'], year=new_manga['year'],
                                            description=new_manga['description'], cover_art_id=new_manga['cover_art_id'],
                                            filename=new_manga['cover_art_filename'], author=new_manga['author'])
                    db.session.add(manga)
                    db.session.commit()
                    return redirect(url_for("home"))
                else:
                    flash(f"{manga_title} not found")
            except Exception as e:
                flash(f"there was an error : {e}")
                return redirect(url_for("home"))


@app.route("/del_manga/<string:manga_id>", methods=["GET"])
def del_manga(manga_id):
    manga = Manga.query.get(manga_id)
    if manga:
        db.session.delete(manga)
        db.session.commit()
    return redirect(url_for("home"))


if __name__ in "__main__":
    #create_app()
    app.run(host="localhost", port=5000, debug=True)
