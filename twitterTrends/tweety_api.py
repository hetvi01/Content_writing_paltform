# Authenticate with Twitter API
import os

from tweepy import OAuth1UserHandler, API

auth = OAuth1UserHandler(
    consumer_key=os.environ.get('CONSUMER_KEY'),
    consumer_secret=os.environ.get('CONSUMER_SECRET'),
    access_token=os.environ.get('ACCESS_TOKEN'),
    access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET')
)

# Create API object
api = API(auth)
