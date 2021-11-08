from flask import Flask

# initializes our app
app = Flask(__name__)


# Listen to a "route"
# '/' is the home page route
@app.route("/")
def root():
    # what I want to happen when somebody goes to the home page
    return "Hello World!"


# kind of like what jinja2 does to our web pages
app_title = "Twitoff DS32"


@app.route("/test")
def test():
    # what I want to happen when somebody goes to the home page
    return f"A page from the {app_title} app"
