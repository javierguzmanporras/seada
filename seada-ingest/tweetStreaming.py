#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy

from twitterTweet import Tweet


class TweetStreaming:

    def __init__(self):
        pass

    def start(self, api, track_list, args, db, connection, dataset_directory):
        my_stream_listener = MyStreamListener(args, db, connection, dataset_directory)
        my_stream = tweepy.Stream(auth=api.auth, listener=my_stream_listener)
        my_stream.filter(track=track_list)  # filter to stream all tweets containing the word python
        # myStream.filter(follow=["2211149702"])  #filter to stream tweets by a specific user


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, args, db, connection, dataset_directory):
        super(MyStreamListener, self).__init__()
        self.args = args
        self.db = db
        self.connection = connection
        self.dataset_directory = dataset_directory
        self.ntweets = 0

    def on_status(self, status):
        """"
        To retrieve, process and organize tweets to get structured data and inject data into database or elasticsearch.
        :param status:
        :return:
        """
        t = Tweet()
        t.set_tweet_information(status)
        self.db.create_tweet(self.connection, t.get_tuple_output_without_raw())
        self.ntweets = self.ntweets + 1
        print("[MyStreamListener] Add new tweet: " + str(self.ntweets))

        return True

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False

        # returning non-False reconnects the stream, with backoff.