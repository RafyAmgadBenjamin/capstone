import os
from flask import Flask, request, abort, jsonify
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

    @app.route("/movies/<int:movie_id>", methods=["PATCH"])
    def update_movie(movie_id):
        body = request.get_json()
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if not movie:
                abort(404)

            if "title" in body:
                movie.title = body.get("title")
            # TODO validate the date to be in the right format
            if "release_date" in body:
                release_date = datetime.strptime(body.get("release_date"), "%Y-%m-%d")
                movie.release_date = release_date

            movie.update()
            return jsonify({"success": True, "movie": movie.format()})
        except Exception:
            abort(400)

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

