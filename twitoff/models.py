from flask_sqlalchemy import SQLAlchemy

# Create a DB Object
DB = SQLAlchemy()

# Make a User table by creating a User class


class User(DB.Model):
    """Creates a User table with sqlalchemy"""

    # id column

    id = DB.Column(DB.BigInteger, primary_key=True)

    # username column
    username = DB.Column(DB.String, nullable=False)

    # keeps track of id for the newest tweet said by user
    newest_tweet_id = DB.Column(DB.BigInteger)

    # we don't need a tweets attribute because this is
    # automatically being added by backref in the Tweet model
    def __repr__(self):
        return f"<User: {self.username}>"


# Make a Tweet table by creating a Tweet class
class Tweet(DB.Model):
    """Creates a Tweet table with sqlalchemy"""

    # id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # text column
    # Unicode allows for both text and links and emojis, etc
    text = DB.Column(DB.Unicode(300), nullable=False)
    # Create a relationship between a tweet and a user
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey("user.id"), nullable=False)
    # Finalizing the relationship making sure it goes both ways.
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))
    # be able to include a word embedding on a tweet
    vect = DB.Column(DB.PickleType, nullable=False)

    def __repr__(self):
        return f"<Tweet: {self.text}>"
