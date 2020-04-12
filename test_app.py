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
        self.actor = Actor(name="tom cruise", age=55, gender="M")

        self.casting_producer_jwt = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1ESkVPRVpEUmpGRk1qSTVRelUyUVRVd1JFRkJRVGhDTnpjeU1FVXpORU0xUmpnelJEaEdOUSJ9.eyJpc3MiOiJodHRwczovL2Rldi04a3l6OXAxeS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDU5MTU2MjIwMDIyNjA4NjM2ODgiLCJhdWQiOlsicHJvZHVjdGlvbiIsImh0dHBzOi8vZGV2LThreXo5cDF5LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODY3MjcwMTAsImV4cCI6MTU4NjgxMzQxMCwiYXpwIjoianRrOW15N0h2aU5YRE13RUF5MVlVeThLd1ZoMnRHYzciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsImdldDpzaW5nbGUtYWN0b3IiLCJnZXQ6c2luZ2xlLW1vdmllIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.MQyBmcXAFEfSl2ChTpEPpyFyk_cWb_Zxoxnpd9HAY9aoYwZpTp5r9fVeuW_-D7CUEYIdx5uJ7BuZYamxrp1MuINreJqalCqjkKIMInJTBtSoGr-2w1f-GiJd1sSXqeB7ZqIHHSQkPZnxWrK3yNaocEet3CmdR90MUOE452u7HXqDeKFu5VgLkAPp7Oy6jgBm6oU3KSxgTqX4IE36OMoy2DuYgJhSSpZdRSA7cOxj1TvSAcZtR1EYWEKxhx-7G0e43udnm_74mS4-TPSNo-raoM0F4Neser7829LgQah2HPgk2FoUuQjeWD3_Hd_UNn5y85yZBw4YTTh_-Hr-N7SEVA"
        self.casting_director_jwt = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1ESkVPRVpEUmpGRk1qSTVRelUyUVRVd1JFRkJRVGhDTnpjeU1FVXpORU0xUmpnelJEaEdOUSJ9.eyJpc3MiOiJodHRwczovL2Rldi04a3l6OXAxeS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDU2MDE0NjQyOTg0MjY4ODU4NDciLCJhdWQiOlsicHJvZHVjdGlvbiIsImh0dHBzOi8vZGV2LThreXo5cDF5LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODY3Mjg4NjQsImV4cCI6MTU4NjgxNTI2NCwiYXpwIjoianRrOW15N0h2aU5YRE13RUF5MVlVeThLd1ZoMnRHYzciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwiZ2V0OnNpbmdsZS1hY3RvciIsImdldDpzaW5nbGUtbW92aWUiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.L9Px4BMcrg_MCmNH_rQ9fXHx0JkTFiUFbpRXIWqT_uTwRdJxigOxuyJuk8XMWh5DTa2A6g2EPAET0gz1sZLCJRIZ41xOuseaaMoxe_tsZwSNaZ2iWC1IkH6dp_eNXgObXLGeUZ4dCvUg8C63vVxjj6NsZ-CknNCgARSxaqOUFowHI6iv0Ce1eLB5lehjf2Z90fbPn2glB9czqScDHG9SCmbSMVnPeksrJOWnPE_U9zkslbnk9yhqRHCN5kR8Qaxxz9dQWQ2xy1cEsLim7F1iAYuvQGqrHBonwwkIsw4sIpW9zAp_E_8DBsY3fZ8t_tLWXwqgQHSx_ANdnbzm8umc-g"
        self.casting_assistant_jwt = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1ESkVPRVpEUmpGRk1qSTVRelUyUVRVd1JFRkJRVGhDTnpjeU1FVXpORU0xUmpnelJEaEdOUSJ9.eyJpc3MiOiJodHRwczovL2Rldi04a3l6OXAxeS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTQzNjU1NzY3MzQxOTExODEwMTIiLCJhdWQiOlsicHJvZHVjdGlvbiIsImh0dHBzOi8vZGV2LThreXo5cDF5LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODY3MjY3MDcsImV4cCI6MTU4NjgxMzEwNywiYXpwIjoianRrOW15N0h2aU5YRE13RUF5MVlVeThLd1ZoMnRHYzciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJnZXQ6c2luZ2xlLWFjdG9yIiwiZ2V0OnNpbmdsZS1tb3ZpZSJdfQ.GsEJOtVAkYLwVU22owmlHILgfwYVW9CFUm6-Vk-YBQMWDgOSVDZhtBCnLoriyYqYvSt_iRidCi1Uespj826sVLSJG70Wzx5L0hWeZANDHGIdPAkLFPnwku-ZCTwaaPppW3Pkt3cKdR2kk8HHjxjKZH3sB_tJRLbKO5b8rwA1UlcCaFtWPqqVbADCY4T65UB8XYd5fHP8ZhiHAyWhR-JMkk4_akWgadlL2YgksXLD1Ga5i6NtW705YqI81IknGBqXkNciE0ycgpVMymc0WM5mAYQD6WUefLQSW-VRqlznutU9TuYxNMhBuaRYmXp8P8M6K8Q6SGSo5FryXKMkDSB2iA"

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
