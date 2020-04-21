"""In the data modeling course, you learned how to use migrations to manage 
your database schema and changes that you make to it. Heroku can run all 
your migrations to the database you have hosted on the platform, but in order 
to do so,your application needs to include a manage.py file"""
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app, models
from app.models import db

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)


if __name__ == "__main__":
    manager.run()
