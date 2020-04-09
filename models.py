import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_name = "capstoneDB"

database_path = "postgresql://{}:{}@{}/{}".format(
    "rafy", "admin", "localhost:5432", database_name
)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)  # migrations instantiation


ActorMovie = db.Table(
    "ActorMovie",
    db.Column("id", Integer, primary_key=True),
    db.Column("movieId", Integer, db.ForeignKey("Movie.id")),
    db.Column("actorId", Integer, db.ForeignKey("Actor.id")),
)


class Movie(db.Model):
    __tablename__ = "Movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    release_date = db.Column(db.DateTime(), nullable=True)
    actors = db.relationship("Actor", secondary=ActorMovie, backref="movie", lazy=True)


class Actor(db.Model):
    __tablename__ = "Actor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.CHAR(1), nullable=True)
    movies = db.relationship("Movie", secondary=ActorMovie, backref="actor", lazy=True)

