#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy

from seadaIngest.twitterTweet import Tweet


class TweetStreaming:

    def __init__(self, api, track_list, dataset_db, dataset_db_connection, dataset_directory,
                 elasticseach=True, dataset=False):
        self.api = api
        self.track_list = track_list
        self.elasticsearch = elasticseach
        self.dataset = dataset
        self.dataset_db = dataset_db
        self.dataset_db_connection = dataset_db_connection
        self.dataset_directory = dataset_directory

    def start(self, ):
        my_stream_listener = MyStreamListener(self.db, self.connection, self.dataset_directory)
        my_stream = tweepy.Stream(auth=self.api.auth, listener=my_stream_listener)
        my_stream.filter(track=self.track_list)  # filter to stream all tweets containing the word python
        # example: myStream.filter(follow=["2211149702"])  #filter to stream tweets by a specific user


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, db, connection, dataset_directory):
        super(MyStreamListener, self).__init__()
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