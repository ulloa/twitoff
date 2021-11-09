"""Handles connection to Twitter API"""

from os import getenv
import tweepy
import spacy
from .models import DB, Tweet, User

# Get API Keys from .env
# make sure to add env in conda
# https://towardsdatascience.com/securing-api-keys-with-environment-variables-using-anaconda-d30a7c48b1fd
KEY = getenv("TWITTER_API_KEY")
SECRET = getenv("TWITTER_API_KEY_SECRET")

# Connect to the Twitter API
TWITTER_AUTH = tweepy.OAuthHandler(KEY, SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)


# load our pretrained SpaCy Word Embeddings model
# unsure why we do this
nlp = spacy.load("my_model/")


# Turn tweet text into word embeddings
def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


# function to query the API for a user
# and add the user to the DB.
def add_or_update_user(username):
    """
    Gets twitter user and tweets from twitter DB
    Gets user by "username" parameter.
    """
    try:
        # get a twitter user from the API
        twitter_user = TWITTER.get_user(screen_name=username)

        # Check to see if that user already exists in our database
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id, username=username
        )

        # add user, assuming it doesn't exist
        DB.session.add(db_user)

        tweets = twitter_user.timeline(
            count=200,
            exclude_replies=True,
            include_rts=False,
            tweet_mode="extended",
            since_id=db_user.newest_tweet_id,
        )

        # check to see if the newest tweet in the DB is equal to the
        # newest tweet from the Twitter API, if they're not equal then that
        # means that the user has posted new tweets that we should add to our
        # DB.
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # add indvidual tweets to the DB session
        for tweet in tweets:

            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text, vect=tweet_vector)

            # make sure the tweet is connected to our user
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

            # Commit / save changes to DB
            # DB.session.commit() # commit at end
    except Exception as e:
        print("Error processing {}: {}", format(username, e))
        raise e

    else:
        DB.session.commit()


def get_all_usernames():
    """get the usernames of all users that are already in the database"""
    usernames = []
    Users = User.query.all()
    for user in Users:
        usernames.append(user.username)

    return usernames
