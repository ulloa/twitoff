from .models import User
import numpy as np
from sklearn.linear_model import LogisticRegression
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet_text):
    """Take in two usernames,
    query forthe tweetvectorizations for those two users.
    Compile the vectorization into an x matrix generate a numpy array of labels
    (y variable) vectorize the hypothetical tweettext.
    fit logreg using x and y
    Generate and return
     a prediction
    """

    # Query for our two users
    user0 = User.query.filter(User.username == user0_name).one()
    user1 = User.query.filter(User.username == user1_name).one()

    # get thetweet vectorizations for the two users
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # combine the vectors into an x matrix
    X = np.vstack([user0_vects, user1_vects])
    # Generate labels of 0s and 1s for our y vector
    y = np.concatenate([np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])

    # fit our logistic regression model
    log_reg = LogisticRegression().fit(X, y)

    # vectorizeour hypothetical tweet text
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    # return the predicted label: (0 or 1)
    return log_reg.predict(hypo_tweet_vect.reshape(1, -1))
