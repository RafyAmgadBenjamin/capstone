import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json


database_path = os.getenv("DATABASE_PATH")
db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path, database_name="capstoneDB"):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    if database_name == "capstoneDB":
        migrate = Migrate(app, db)  # migrations instantiation
    else:
        db.create_all()


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

    def __init__(self, title, release_date):
        """Initialize the movie class with title and release_date
        """
        self.title = title
        self.release_date = release_date

    def save(self):
        """
        Save the movie object to database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete the movie object from the database
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """
        Update the movie object to database
        """
        db.session.commit()

    def format(self):
        """
        Format the movie
        """
        return {"id": self.id, "title": self.title, "release_date": self.release_date}


class Actor(db.Model):
    __tablename__ = "Actor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.CHAR(1), nullable=True)
    movies = db.relationship("Movie", secondary=ActorMovie, backref="actor", lazy=True)

    def __init__(self, name, age, gender):
        """
        Initialize the actor object with name, age and gender
        """
        self.name = name
        self.age = age
        self.gender = gender

    def save(self):
        """
        Save the actor object to database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete the actor object from the database
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """
        Update the actor object to database
        """
        db.session.commit()

    def format(self):
        """
        Format the actor
        """
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
        }

