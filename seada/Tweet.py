#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SeadaUtils import *


class Tweet:
    """Tweets of Users"""
    languages = {}
    sources = {}
    places = {}
    hashtags = {}
    ntweets = 0

    def __init__(self):
        # tweet information (19)
        self.created_at = ""
        self.id = ""
        self.text = ""
        self.truncated = ""
        self.source = ""
        self.in_reply_to_status_id_str = ""
        self.in_reply_to_user_id_str = ""
        self.in_reply_to_screen_name = ""
        #user
        self.coordinates = ""
        self.place = ""
        self.contributors = ""
        self.is_quote_status = ""
        self.retweet_count = ""
        self.favorite_count = ""
        self.favorited = ""
        self.retweeted = ""
        self.possibly_sensitive = ""
        self.lang = ""
        #self.user_name = ""
        self.entities_hashtags = []
        self.entities_user_mentions = []
        self.entities_urls = []
        # Other information
        self.tweet = {}
        self.raw_tweet = ""

    def set_tweet_information(self, item):
        """
        Set tweet information from tweepy object tweet.
        :param item:
        :return:
        """
        self.raw_tweet = SeadaUtils.json_to_string(item)
        self.created_at = item.created_at
        self.tweet['created_at'] = str(item.created_at)
        self.id = item.id
        self.tweet['id'] = item.id
        self.text = item.full_text
        self.tweet['text'] = item.full_text
        self.truncated = item.truncated
        self.tweet['truncated'] = item.truncated
        self.source = item.source
        self.tweet['source'] = item.source
        self.in_reply_to_status_id_str = item.in_reply_to_status_id_str
        self.tweet['in_reply_to_status_id_str'] = item.in_reply_to_status_id_str
        self.in_reply_to_user_id_str = item.in_reply_to_user_id_str
        self.tweet['in_reply_to_user_id_str'] = item.in_reply_to_user_id_str
        self.in_reply_to_screen_name = item.in_reply_to_screen_name
        self.tweet['in_reply_to_screen_name'] = item.in_reply_to_screen_name
        self.coordinates = item.coordinates
        self.tweet['coordinates'] = item.coordinates
        self.place = item.place
        self.tweet['place'] = item.place
        self.contributors = item.contributors
        self.tweet['contributors'] = item.contributors
        self.is_quote_status = item.is_quote_status
        self.tweet['is_quote_status'] = item.is_quote_status
        self.retweet_count = item.retweet_count
        self.tweet['retweet_count'] = item.retweet_count
        self.favorite_count = item.favorite_count
        self.tweet['favorite_count'] = item.favorite_count
        self.favorited = item.favorited
        self.tweet['favorited'] = item.favorited
        self.retweeted = item.retweeted
        self.tweet['retweet'] = item.retweeted
        #self.possibly_sensitive = item.possibly_sensitive
        #self.tuit['possibly_sensitive'] = item.possibly_sensitive
        self.lang = item.lang
        self.tweet['lang'] = item.lang

        e = item.entities
        if len(e['hashtags']) > 0:
            for hastag in e['hashtags']:
                self.entities_hashtags.append(hastag['text'])

        if len(e['user_mentions']) > 0:
            for mention in e['user_mentions']:
                self.entities_user_mentions.append(mention['screen_name'])

        if len(e['urls']) > 0:
            for url in e['urls']:
                self.entities_urls.append(url['expanded_url'])

        self.tweet['hashtags'] = self.entities_hashtags
        self.tweet['user_mentions'] = self.entities_user_mentions
        self.tweet['urls'] = self.entities_urls

        #if self.truncated:
        #    print(item.text_)

        #get lang
        if item.lang in self.languages:
            self.languages[item.lang] += 1
        else:
            self.languages[item.lang] = 1

        #get source
        if item.source in self.sources:
            self.sources[item.source] += 1
        else:
            self.sources[item.source] = 1

        #get places
        if item.place:
            if item.place.name in self.places:
                self.places[item.place.name] += 1
            else:
                self.places[item.place.name] = 1

        for ht in self.entities_hashtags:
            if ht in self.hashtags:
                self.hashtags[ht] += 1
            else:
                self.hashtags[ht] = 1

    @classmethod
    def get_report(self):
        for key, val in self.languages.items():
            print(str(key) + " => " + str(val))

        for key, val in self.sources.items():
            print(str(key) + " => " + str(val))

        for key, val in self.places.items():
            print(str(key) + " => " + str(val))

        for key, val in self.hashtags.items():
            print(str(key) + " => " + str(val))

    def get_json_output(self, file_name, dataset_directory):
        SeadaUtils.get_json_output(file_name, dataset_directory, self.tweet)

    def get_csv_output(self, file_name, dataset_directoy):
        item = list(self.get_tuple_output())
        item.pop(-1)
        SeadaUtils.get_csv_output(file_name, dataset_directoy, item)


    def get_tuple_output(self):
        """
        Generate a tuple with tweet information for input database
        :return: A tuple with tweet information
        """
        tuple_tweet = (self.id, self.created_at, self.text, self.truncated, self.source,
                       self.in_reply_to_status_id_str, self.in_reply_to_user_id_str, self.in_reply_to_screen_name,
                       self.coordinates, self.place, self.contributors,
                       self.is_quote_status, self.retweet_count, self.favorite_count, self.favorited, self.retweeted,
                       self.possibly_sensitive, self.lang, self.raw_tweet)
        return tuple_tweet



    # user
    # self.user_name = ""
    #self.entities_hashtags = []
    #self.entities_user_mentions = []
    #self.entities_urls = []