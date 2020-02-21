import tweepy
from MyStreamListener import *


class TweetStreaming():

    def __init__(self):
        pass

    def start(self, api):
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.filter(track=['#paro'])        #filter to stream all tweets containing the word python
        #myStream.filter(follow=["2211149702"])  #filter to stream tweets by a specific user