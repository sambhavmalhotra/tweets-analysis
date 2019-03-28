# I copied all this stuff from http://adilmoujahid.com/posts/2014/07/twitter-analytics/

# Import the necessary methods from tweepy library
# import re
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

file_to_write = open('iplStream.txt', 'a')

# Variables that contains the user credentials to access Twitter API
access_token = "1100014282685636613-UMfeFM5srsAZy0ENodCWaqN2NqVKw5"
access_token_secret = "nZXbILijLsVyakFezHRnkzDGMPH8wEd68zKt6LPHiYjuS"
consumer_key = "HrnFlaAdG6aY7xfd7I1T7ENj4"
consumer_secret = "TV4bWR7BZJBTomEKf0kAc7hQaLjfgaKmErQzWyBMqSFWch2gtU"


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):

        d = json.loads(data)
        print d['text']
        json.dump(d, file_to_write)
        file_to_write.write("\n")
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
    # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=[search_string])


if __name__ == '__main__':
    stream_data({
        "keywords": {
            "and": ["#ipl", "#mivsrcb"]
        }
    })
