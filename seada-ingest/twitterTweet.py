#!/usr/bin/env python
# -*- coding: utf-8 -*-

from outputUtilities import *
from outputInterface import OutputInterface


class Tweet(OutputInterface):
    """Tweets of Users"""

    def __init__(self):
        self.created_at = ""
        self.id = ""
        self.text = ""
        self.truncated = ""
        self.source = ""
        self.in_reply_to_status_id_str = ""
        self.in_reply_to_user_id_str = ""
        self.in_reply_to_screen_name = ""
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
        self.user_id = ""
        self.user_name = ""
        self.user_screen_name = ""
        self.entities_hashtags = []
        self.entities_user_mentions = []
        self.entities_urls = []
        # Other information
        self.tweet = {}
        self.raw_tweet = ""
        self.user = ""

    def set_tweet_information(self, item):
        """
        Set tweet information from tweepy object tweet.
        :param item:
        :return:
        """
        self.raw_tweet = OutputUtilities.json_to_string(item)
        self.created_at = item.created_at
        self.tweet['created_at'] = item.created_at
        self.id = item.id
        self.tweet['id'] = item.id
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
        # TODO place is an tweepy.api.API object with many items or attributes
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
        self.lang = item.lang
        self.tweet['lang'] = item.lang
        self.user_id = item.user.id
        self.tweet['user_id'] = item.user.id
        self.user_name = item.user.name
        self.tweet['user_name'] = item.user.name
        self.user_screen_name = item.user.screen_name
        self.tweet['user_screen_name'] = item.user.screen_name
        self.user = item.user

        try:
            self.text = item.full_text
            self.tweet['text'] = item.full_text
        except AttributeError:
            self.text = item.text
            self.tweet['text'] = item.text

        try:
            self.possibly_sensitive = item.possibly_sensitive
            self.tweet['possibly_sensitive'] = item.possibly_sensitive
        except:
            self.tweet['possibly_sensitive'] = None

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

    def get_json_output(self, file_name, dataset_directory):
        """
        Generate a json output file for this instance.
        :param file_name: the name of the json file.
        :param dataset_directory: where the file will create.
        :return: a json file in dataset_directory.
        """
        item = dict(self.tweet)
        item['created_at'] = str(item['created_at'])
        OutputUtilities.get_json_output(file_name=file_name, dataset_directory=dataset_directory, item=item,
                                        datatag='tweet_list')

    def get_csv_output(self, file_name, dataset_directory):
        """
        Generate a csv output file for this instance.
        :param file_name: the name of the csv file.
        :param dataset_directoy: where the file will create
        :return: a csv file in dataset_directory.
        """
        item = list(self.get_tuple_output_without_raw())
        OutputUtilities.get_csv_output(file_name=file_name, dataset_directory=dataset_directory, item=item)

    def get_tuple_output_without_raw(self):
        """
        Generate a tuple with tweet information without raw information for input database
        :return: A tuple with tweet information
        """
        # You could pickle/marshal/json your array and store it as binary/varchar/json field in your database.
        hashtags_json = json.dumps(self.entities_hashtags)
        user_mentions_json = json.dumps(self.entities_user_mentions)
        urls_json = json.dumps(self.entities_urls)

        tuple_tweet = (self.id, self.created_at, self.text, self.truncated, self.source,
                       self.in_reply_to_status_id_str, self.in_reply_to_user_id_str, self.in_reply_to_screen_name,
                       self.coordinates, self.place, self.contributors,
                       self.is_quote_status, self.retweet_count, self.favorite_count, self.favorited, self.retweeted,
                       self.possibly_sensitive, self.lang, self.user_id, self.user_name, self.user_screen_name,
                       hashtags_json, user_mentions_json, urls_json)
        return tuple_tweet

    def get_tuple_output(self):
        """
        Generate a tuple with tweet information for input database
        :return: A tuple with tweet information
        """
        tuple_tweet = (self.id, self.created_at, self.text, self.truncated, self.source,
                       self.in_reply_to_status_id_str, self.in_reply_to_user_id_str, self.in_reply_to_screen_name,
                       self.coordinates, self.place, self.contributors,
                       self.is_quote_status, self.retweet_count, self.favorite_count, self.favorited, self.retweeted,
                       self.possibly_sensitive, self.lang, self.user_id, self.user_name, self.user_screen_name,
                       self.raw_tweet)
        return tuple_tweet
