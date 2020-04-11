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

    # Add movie
    def test_add_new_movie(self):
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

    def test_409_add_movie_duplicated(self):
        # Arrange
        movie = {"title": self.movie.title, "release_date": self.movie.release_date}
        res = self.client().post("/movies", json=movie)

        # Act
        res = self.client().post("/movies", json=movie)
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 409)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 409)
        self.assertEqual(
            data["message"], "conflicts with some rule already established"
        )

    def test_400_add_movie_without_title(self):
        # Arrange
        movie = {"release_date": self.movie.release_date}
        # Act
        res = self.client().post("/movies", json=movie)
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 400)
        self.assertEqual(data["message"], "bad request")

    # Get movies
    def test_get_movies(self):
        # Arrange
        movie = {"title": self.movie.title, "release_date": self.movie.release_date}
        res = self.client().post("/movies", json=movie)
        # Act
        res = self.client().get("/movies")
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    def test_404_get_movie_but_there_is_no_movies(self):
        # Arrange
        # Act
        res = self.client().get("/movies")
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    # Get single movie
    def test_get_single_movie(self):
        # Arrange
        movie = {"title": self.movie.title, "release_date": self.movie.release_date}
        res = self.client().post("/movies", json=movie)
        data = json.loads(res.data)
        movie_id = data["movie"].get("id")
        # Act
        res = self.client().get(f"/movies/{movie_id}")
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])

    def test_404_get_single_movie_with_wrong_id(self):
        # Arrange
        movie_id = 56463464
        # Act
        res = self.client().get(f"/movies/{movie_id}")
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    # Delete movie
    def test_delete_movie(self):
        # Arrange
        movie = {"title": self.movie.title, "release_date": self.movie.release_date}
        res = self.client().post("/movies", json=movie)
        data = json.loads(res.data)
        movie_id = data["movie"].get("id")
        # Act
        res = self.client().delete(f"/movies/{movie_id}")
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])

    def test_404_delete_movie_with_wrong_id(self):
        # Arrange
        movie_id = 23497823
        # Act
        res = self.client().delete(f"/movies/{movie_id}")
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    # Patch movie
    def test_update_movie(self):
        # Arrange
        movie = {"title": self.movie.title, "release_date": self.movie.release_date}
        res = self.client().post("/movies", json=movie)
        data = json.loads(res.data)
        movie_id = data["movie"].get("id")
        movie = {"title": "Brave Heart", "release_date": self.movie.release_date}

        # Act
        res = self.client().patch(f"/movies/{movie_id}", json=movie)
        data = json.loads(res.data)

        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])
        self.assertEqual(data["movie"].get("title"), "Brave Heart")

    def test_404_update_movie_with_wrong_id(self):
        # Arrange
        movie = {"title": self.movie.title, "release_date": self.movie.release_date}
        movie_id = 1234928
        # Act
        res = self.client().patch(f"/movies/{movie_id}", json=movie)
        data = json.loads(res.data)

        # Assert
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
