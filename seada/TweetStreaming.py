#!/usr/bin/env python
# -*- coding: utf-8 -*-

from MyStreamListener import *


class TweetStreaming:

    def __init__(self):
        pass

    def start(self, api, track_list, args, db, connection, dataset_directory):
        my_stream_listener = MyStreamListener(args, db, connection, dataset_directory)
        my_stream = tweepy.Stream(auth=api.auth, listener=my_stream_listener)
        my_stream.filter(track=track_list)  # filter to stream all tweets containing the word python
        # myStream.filter(follow=["2211149702"])  #filter to stream tweets by a specific user
