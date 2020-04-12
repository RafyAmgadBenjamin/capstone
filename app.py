import os
from flask import Flask, request, abort, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from datetime import datetime


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)

    # Load
    setup_db(app)

    # Enable CORS
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    # Endpoints

    # Movie endpoints
    @app.route("/movies", methods=["GET"])
    def get_movies():
        movies = Movie.query.order_by(Movie.id).all()
        if len(movies) == 0:
            abort(404)
        movies_formated = [movie.format() for movie in movies]
        return jsonify({"success": True, "movies": movies_formated})

    @app.route("/movies/<int:movie_id>", methods=["GET"])
    def get_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if not movie:
            abort(404)
        return jsonify({"success": True, "movie": movie.format()})

    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    def delete_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if not movie:
            abort(404)
        try:
            movie.delete()
            return jsonify({"success": True, "movie": movie.format()})
        except Exception:
            abort(422)

    @app.route("/movies/<int:movie_id>", methods=["PATCH"])
    def update_movie(movie_id):
        body = request.get_json()

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        # If there is no movie with this ID abort
        if not movie:
            abort(404)
        # Validate the either title or release_date in the body
        if not "title" in body and not "release_date" in body:
            abort(400)

        if "title" in body:
            movie.title = body.get("title")
        try:
            if "release_date" in body:
                release_date = datetime.strptime(body.get("release_date"), "%Y-%m-%d")
                movie.release_date = release_date
        except Exception:
            abort(400)
        try:
            movie.update()
            return jsonify({"success": True, "movie": movie.format()})
        except Exception:
            abort(422)

    @app.route("/movies", methods=["POST"])
    def add_movie():
        body = request.get_json()
        # Make sure the the request body have title and release_date
        if not "title" in body or not "release_date" in body:
            abort(400)
        # Remove spaces and give it standard format to be saved in database
        movie_title = body.get("title").strip().title()
        # Make sure that the added title is not there
        movie = Movie.query.filter(Movie.title == movie_title).one_or_none()
        # Abort as this movie already exist with the same name and it is duplication
        if movie:
            abort(409)
        # Format the date to be in the required format and in type for the database
        try:
            movie_release_date = datetime.strptime(body.get("release_date"), "%Y-%m-%d")
        except Exception:
            abort(400)
        try:
            movie = Movie(title=movie_title, release_date=movie_release_date)
            movie.save()
            return jsonify({"success": True, "movie": movie.format()})
        except Exception:
            abort(422)

    # Actor endpoints
    @app.route("/actors", methods=["GET"])
    def get_actors():
        actors = Actor.query.order_by(Actor.id).all()
        if len(actors) == 0:
            abort(404)
        actors_formated = [actor.format() for actor in actors]
        return jsonify({"success": True, "actors": actors_formated})

    @app.route("/actors/<int:actor_id>", methods=["GET"])
    def get_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if not actor:
            abort(404)
        return jsonify({"success": True, "actor": actor.format()})

    @app.route("/actors/<int:actor_id>", methods=["DELETE"])
    def delete_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if not actor:
            abort(404)
        try:
            actor.delete()
            return jsonify({"success": True, "actor": actor.format()})
        except Exception:
            abort(422)

    @app.route("/actors/<int:actor_id>", methods=["PATCH"])
    def update_actor(actor_id):
        body = request.get_json()
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        # If no actor with this ID abort
        if not actor:
            abort(404)
        # validate that the body at least one attribute
        if not "name" in body and not "age" in body and not "gender" in body:
            abort(400)

        if "name" in body:
            actor.name = body.get("name")

        if "age" in body:
            actor.age = int(body.get("age"))

        if "gender" in body:
            gender = body.get("gender").upper()
            if gender == "M" or gender == "F":
                actor.gender = gender
            else:
                abort(400)
        try:
            actor.update()
            return jsonify({"success": True, "actor": actor.format()})
        except Exception:
            abort(422)

    @app.route("/actors", methods=["POST"])
    def add_actor():
        body = request.get_json()
        # Make sure the the request body have title and release_date
        if not "name" in body or not "age" in body or not "gender" in body:
            abort(400)

        # Remove spaces and give it standard format to be saved in database
        actor_name = body.get("name").strip().title()
        # Make sure that the added name is not there
        actor = Actor.query.filter(Actor.name == actor_name).one_or_none()
        # Abort as this actor already exist with the same name and it is duplication
        if actor:
            abort(409)

        # Validate the gender
        if "gender" in body:
            gender = body.get("gender").upper()
            if gender == "M" or gender == "F":
                actor_gender = gender
            else:
                abort(400)

        try:
            actor = Actor(
                name=actor_name, age=int(body.get("age")), gender=actor_gender
            )
            actor.save()
            return jsonify({"success": True, "actor": actor.format()})
        except Exception:
            abort(422)

    @app.route("/login")
    def login():
        # TODO move them to config. file
        auth0 = {}
        auth0["url"] = "dev-8kyz9p1y.auth0.com"
        auth0["audience"] = "production"
        auth0["clientId"] = "jtk9my7HviNXDMwEAy1YUy8KwVh2tGc7"
        auth0["callbackURL"] = "http://localhost:5000/welcome"

        link = "https://"
        link += auth0["url"] + ".auth0.com"
        link += "/authorize?"
        link += "audience=" + auth0["audience"] + "&"
        link += "response_type=token&"
        link += "client_id=" + auth0["clientId"] + "&"
        link += "redirect_uri=" + auth0["callbackURL"]
        return redirect(link, code=302)

    @app.route("/welcome")
    def welcome():
        return "welcome to our application"

    ## Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}),
            400,
        )

    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "not allowed"}),
            405,
        )

    @app.errorhandler(409)
    def conflict(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 409,
                    "message": "conflicts with some rule already established",
                }
            ),
            409,
        )

    @app.errorhandler(401)
    def unauthorized(error):
        return (
            jsonify({"success": False, "error": 401, "message": "not authorized",}),
            401,
        )

    @app.errorhandler(403)
    def forbidden(error):
        return (
            jsonify({"success": False, "error": 403, "message": "forbidden",}),
            403,
        )

    return app


APP = create_app()

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=8080, debug=True)

