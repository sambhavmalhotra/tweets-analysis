# I copied all this stuff from http://adilmoujahid.com/posts/2014/07/twitter-analytics/

# Import the necessary methods from tweepy library
import re
import json
import DB_Connect as Db
from tweepy import Stream
from textblob import TextBlob
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

file_to_write = open('data/iplStream.txt', 'a')
string_to_search = ""

# Variables that contains the user credentials to access Twitter API
access_token = "<access_token>"
access_token_secret = "<access_token_secret>"
consumer_key = "<consumer_key>"
consumer_secret = "<consumer_secret>"


def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


def save_tweet_to_db(data):
    d = json.loads(data)
    tweet = {}
    tweets_to_save = []
    global string_to_search
    if d['created_at'] is not None:
        tweet['tweet_id'] = d['id']
        tweet['user_id'] = d['user']['id']
        tweet['retweets'] = d['retweet_count']
        tweet['favorites'] = d['favorite_count']
        tweet['text'] = d['text']
        tweet['user_screen_name'] = d['user']['screen_name']
        tweet['user_name'] = d['user']['name']
        tweet['created_at'] = d['created_at']
        tweet['sentiment'] = get_tweet_sentiment(tweet['text'])
        tweet["group_key"] = string_to_search
        tweets_to_save.append(tweet)
    Db.save_tweets(tweets_to_save)


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        save_tweet_to_db(data)
        return True

    def on_error(self, status):
        print status


def stream_data(input_object):
    # This handles Twitter authentication and the connection to Twitter Streaming API
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)
    search_string = ""
    if 'or' in input_object["keywords"]:
        for x in input_object["keywords"]["or"]:
            # use spaces ' ' for AND and comma ',' for OR
            search_string += (x + ",")
    elif 'and' in input_object["keywords"]:
        for x in input_object["keywords"]["and"]:
            # use spaces ' ' for AND and comma ',' for OR
            search_string += (x + " ")
    search_string = search_string[:-1]
    global string_to_search
    string_to_search = search_string
    # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=[string_to_search])


if __name__ == '__main__':
    stream_data({
        "keywords": {
            "or": ["#rcbvsmi", "#mivsrcb"]
        }
    })
