import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from app.models import setup_db, Movie, Actor, db


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstoneDB_test"

        self.database_path = os.getenv("TEST_DATABASE_URL")
        setup_db(self.app, self.database_path, self.database_name)

        self.movie = Movie(title="instersteller", release_date="2014-4-4")
        self.actor = Actor(name="tom cruise", age=55, gender="M")

        self.casting_producer_jwt = os.getenv("CASTING_PRODUCER_JWT")
        self.casting_director_jwt = os.getenv("CASTING_DIRECTOR_JWT")
        self.casting_assistant_jwt = os.getenv("CASTING_ASSISTANT_JWT")

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
        res = self.client().post(
            "/movies", json=movie, headers={"Authorization": self.casting_producer_jwt}
        )
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])
        self.assertEqual(data["movie"].get("title"), "Instersteller")

    def test_401_add_new_movie_not_authorized(self):
        # Arrange
        movie = {"title": self.movie.title, "release_date": self.movie.release_date}
        # Act
        res = self.client().post("/movies", json=movie)
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_409_add_movie_duplicated(self):
        # Arrange
        movie = {"title": self.movie.title, "release_date": self.movie.release_date}
        res = self.client().post(
            "/movies", json=movie, headers={"Authorization": self.casting_producer_jwt}
        )

        # Act
        res = self.client().post(
            "/movies", json=movie, headers={"Authorization": self.casting_producer_jwt}
        )
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
        res = self.client().post(
            "/movies", json=movie, headers={"Authorization": self.casting_producer_jwt}
        )
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
        res = self.client().post(
            "/movies", json=movie, headers={"Authorization": self.casting_producer_jwt},
        )
        # Act
        res = self.client().get(
            "/movies", headers={"Authorization": self.casting_assistant_jwt}
        )
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    def test_404_get_movie_but_there_is_no_movies(self):
        # Arrange
        # Act
        res = self.client().get(
            "/movies", headers={"Authorization": self.casting_assistant_jwt}
        )
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
        res = self.client().post(
            "/movies", json=movie, headers={"Authorization": self.casting_producer_jwt}
        )
        data = json.loads(res.data)
        movie_id = data["movie"].get("id")
        # Act
        res = self.client().get(
            f"/movies/{movie_id}", headers={"Authorization": self.casting_producer_jwt}
        )
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])

    def test_404_get_single_movie_with_wrong_id(self):
        # Arrange
        movie_id = 56463464
        # Act
        res = self.client().get(
            f"/movies/{movie_id}", headers={"Authorization": self.casting_producer_jwt}
        )
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
        res = self.client().post(
            "/movies", json=movie, headers={"Authorization": self.casting_producer_jwt}
        )
        data = json.loads(res.data)
        movie_id = data["movie"].get("id")
        # Act
        res = self.client().delete(
            f"/movies/{movie_id}", headers={"Authorization": self.casting_producer_jwt}
        )
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])

    def test_404_delete_movie_with_wrong_id(self):
        # Arrange
        movie_id = 23497823
        # Act
        res = self.client().delete(
            f"/movies/{movie_id}", headers={"Authorization": self.casting_producer_jwt}
        )
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
        res = self.client().post(
            "/movies", json=movie, headers={"Authorization": self.casting_producer_jwt}
        )
        data = json.loads(res.data)
        movie_id = data["movie"].get("id")
        movie = {"title": "Brave Heart", "release_date": self.movie.release_date}

        # Act
        res = self.client().patch(
            f"/movies/{movie_id}",
            json=movie,
            headers={"Authorization": self.casting_producer_jwt},
        )
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
        res = self.client().patch(
            f"/movies/{movie_id}",
            json=movie,
            headers={"Authorization": self.casting_producer_jwt},
        )
        data = json.loads(res.data)

        # Assert
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    # Add actor
    def test_add_new_actor(self):
        # Arrange
        actor = {
            "name": self.actor.name,
            "age": self.actor.age,
            "gender": self.actor.gender,
        }
        # Act
        res = self.client().post(
            "/actors", json=actor, headers={"Authorization": self.casting_producer_jwt}
        )
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])
        self.assertEqual(data["actor"].get("name"), "Tom Cruise")

    def test_409_add_actor_duplicated(self):
        # Arrange
        actor = {
            "name": self.actor.name,
            "age": self.actor.age,
            "gender": self.actor.gender,
        }
        res = self.client().post(
            "/actors", json=actor, headers={"Authorization": self.casting_producer_jwt}
        )

        # Act
        res = self.client().post(
            "/actors", json=actor, headers={"Authorization": self.casting_producer_jwt}
        )
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 409)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 409)
        self.assertEqual(
            data["message"], "conflicts with some rule already established"
        )

    def test_400_add_actor_without_name(self):
        # Arrange
        actor = {
            "age": self.actor.age,
            "gender": self.actor.gender,
        }
        # Act
        res = self.client().post(
            "/actors", json=actor, headers={"Authorization": self.casting_producer_jwt}
        )
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 400)
        self.assertEqual(data["message"], "bad request")

    # Get actors
    def test_get_actors(self):
        # Arrange
        actor = {
            "name": self.actor.name,
            "age": self.actor.age,
            "gender": self.actor.gender,
        }
        res = self.client().post(
            "/actors", json=actor, headers={"Authorization": self.casting_producer_jwt}
        )
        # Act
        res = self.client().get(
            "/actors", headers={"Authorization": self.casting_director_jwt}
        )
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    def test_404_get_actor_but_there_is_no_actors(self):
        # Arrange
        # Act
        res = self.client().get(
            "/actors", headers={"Authorization": self.casting_producer_jwt}
        )
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    # Get single actor
    def test_get_single_actor(self):
        # Arrange
        actor = {
            "name": self.actor.name,
            "age": self.actor.age,
            "gender": self.actor.gender,
        }
        res = self.client().post(
            "/actors", json=actor, headers={"Authorization": self.casting_producer_jwt}
        )
        data = json.loads(res.data)
        actor_id = data["actor"].get("id")
        # Act
        res = self.client().get(
            f"/actors/{actor_id}", headers={"Authorization": self.casting_director_jwt}
        )
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])

    def test_404_get_single_actor_with_wrong_id(self):
        # Arrange
        actor_id = 56463464
        # Act
        res = self.client().get(
            f"/actors/{actor_id}", headers={"Authorization": self.casting_producer_jwt}
        )
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    # Delete actor
    def test_delete_actor(self):
        # Arrange
        actor = {
            "name": self.actor.name,
            "age": self.actor.age,
            "gender": self.actor.gender,
        }
        res = self.client().post(
            "/actors", json=actor, headers={"Authorization": self.casting_producer_jwt}
        )
        data = json.loads(res.data)
        actor_id = data["actor"].get("id")
        # Act
        res = self.client().delete(
            f"/actors/{actor_id}", headers={"Authorization": self.casting_producer_jwt}
        )
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])

    def test_404_delete_actor_with_wrong_id(self):
        # Arrange
        actor_id = 23497823
        # Act
        res = self.client().delete(
            f"/actors/{actor_id}", headers={"Authorization": self.casting_producer_jwt}
        )
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    # Patch actor
    def test_update_actor(self):
        # Arrange
        actor = {
            "name": self.actor.name,
            "age": self.actor.age,
            "gender": self.actor.gender,
        }
        res = self.client().post(
            "/actors", json=actor, headers={"Authorization": self.casting_producer_jwt}
        )
        data = json.loads(res.data)
        actor_id = data["actor"].get("id")
        actor = {
            "name": self.actor.name,
            "age": 60,
            "gender": self.actor.gender,
        }
        # Act
        res = self.client().patch(
            f"/actors/{actor_id}",
            json=actor,
            headers={"Authorization": self.casting_producer_jwt},
        )
        data = json.loads(res.data)
        # Assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])
        self.assertEqual(data["actor"].get("age"), 60)

    def test_404_update_actor_with_wrong_id(self):
        # Arrange
        actor = {
            "name": self.actor.name,
            "age": 60,
            "gender": self.actor.gender,
        }
        actor_id = 1234928
        # Act
        res = self.client().patch(
            f"/actors/{actor_id}",
            json=actor,
            headers={"Authorization": self.casting_producer_jwt},
        )
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
