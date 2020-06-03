#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import logging
import requests
import datetime

from seadaIngest.twitterTweet import Tweet


class TweetStream:

    def __init__(self, api, track_list, dataset_db, dataset_db_connection, dataset_directory,
                 elasticseach, dataset=False):
        self.api = api
        self.track_list = track_list
        self.es = elasticseach
        self.dataset = dataset
        self.dataset_db = dataset_db
        self.dataset_db_connection = dataset_db_connection
        self.dataset_directory = dataset_directory

    def start(self):
        print('[+] SEADA streaming starting...')

        self.es.create_index(index_name=self.es.twitter_streaming_tweet_index_name,
                             mapping_file=self.es.twitter_streaming_tweet_mapping_file, debug=False)

        my_stream_listener = MyStreamListener(self.es, self.dataset_db, self.dataset_db_connection,
                                              self.dataset_directory)

        while True:
            try:
                my_stream = tweepy.Stream(auth=self.api.auth, listener=my_stream_listener)
                my_stream.filter(track=self.track_list)  # filter to stream all tweets containing the word python
                # example: myStream.filter(follow=["2211149702"])  #filter to stream tweets by a specific user
                # example: myStream.filter(track=['python']) #filter to stream all tweets containing the word python.
            except requests.exceptions.ConnectionError as ex:
                print('[+] Stream stopped by ConnectionError. Reconnecting'.format(ex.args))
                logging.error('[TweetStreaming] Stream stopped by ConnectionError with error '
                              'args: {}. Reconnecting...'.format(ex.args))
            except requests.exceptions.ReadTimeout as ex:
                print('[+] Stream stopped by ReadTimeout. Reconnecting'.format(ex.args))
                logging.error('[TweetStreaming] Stream stopped by ReadTimeout with error '
                              'args: {}. Reconnecting...'.format(ex.args))
            except Exception as ex:
                print('[+] Stream stopped. Reconnecting...')
                logging.error('[TweetStreaming] Stream stopped with error args: {}. Reconnecting...'.format(ex.args))


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, es, dataset_db, dataset_db_connection, dataset_directory):
        super(MyStreamListener, self).__init__()
        self.es = es
        self.dataset_db = dataset_db
        self.dataset_db_connection = dataset_db_connection
        self.dataset_directory = dataset_directory
        self.ntweets = 0

    def on_status(self, status):
        """"
        To retrieve, process and organize tweets to get structured data and inject data into database or elasticsearch.
        :param status: a tweepy's objects representation of Twitter tweet.
        :return: True in success and False in exception.
        """
        try:
            t = Tweet()
            t.set_tweet_information(status)
            # self.db.create_tweet(self.connection, t.get_tuple_output_without_raw())

            self.es.store_information_to_elasticsearch(index_name=self.es.twitter_streaming_tweet_index_name,
                                                       info=t.tweet, debug=False)
            self.ntweets = self.ntweets + 1

            print('[+] {} new tweet added. Total tweets: {}.'.format(datetime.datetime.now(), self.ntweets))
            logging.info("[MyStreamListener.on_status] Add new tweet: " + str(self.ntweets))
        except Exception as ex:
            logging.error('[MyStreamListener.on_satus] Exception: {}'.format(ex.args))
            return False

        return True

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False
