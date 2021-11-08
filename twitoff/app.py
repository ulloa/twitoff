from flask import Flask, render_template
from .models import DB, User, Tweet


def create_app():
    # initializes our app
    app = Flask(__name__)

    # Database configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    # Listen to a "route"
    # '/' is the home page route
    @app.route("/")
    def root():
        # query the db for all users
        users = User.query.all()
        # what I want to happen when somebody goes to the home page
        return render_template("base.html", title="Home", users=users)

    @app.route("/populate")
    def populate():
        # find a way to auto increment
        ryan = User(id=1, username="Ryan")
        DB.session.add(ryan)
        julian = User(id=2, username="Julian")
        DB.session.add(julian)
        tweet1 = Tweet(id=1, text="tweet text", user=ryan)
        DB.session.add(tweet1)
        tweet2 = Tweet(id=2, text="julian's tweet", user=julian)
        DB.session.add(tweet2)

        DB.session.commit()
        return "populate"

    @app.route("/reset")
    def reset():
        # remove everything from the database
        DB.drop_all()
        # creates the database file initially
        DB.create_all()
        return "reset"

    return app
