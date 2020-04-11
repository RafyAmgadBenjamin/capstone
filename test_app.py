import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor, db


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstoneDB_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "rafy", "admin", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path, self.database_name)

        self.movie = Movie(title="instersteller", release_date="2014-4-4")

        # binds the app to the current context
        with self.app.app_context():
            db = SQLAlchemy()
            db.init_app(self.app)
            # create all tables
            db.create_all()

    def test_add_movie(self):
        # Arrange
        movie = {"title": self.movie.title, "release_date": self.movie.release_date}
        # Act
        res = self.client().post("/movies", json=movie)
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])
        self.assertEqual(data["movie"].get("title"), "Instersteller")

    # def test_get_movies(self):
    #     # Arrange
    #     # Act
    #     res = self.client().get("/movies")
    #     data = json.loads(res.data)
    #     # Assert
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["movies"])

    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
