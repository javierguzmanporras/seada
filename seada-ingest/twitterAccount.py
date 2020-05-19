#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twitterUser import TwitterUser
from twitterFriend import TwitterFriends
from twitterFollower import TwitterFollowers
from tweetMiner import TweetMiner
from twitterFavorites import TwitterFavorites
from timer import Timer

import tweepy
import logging


class TwitterAccount:

    timer_user_info = Timer(name='user_info')
    timer_tweets_info = Timer(name='tweets_info')
    timer_friends_info = Timer(name='friends_info')
    timer_followers_info = Timer(name='followers_info')
    timer_favorites_info = Timer(name='favorites_info')

    def __init__(self, api, args, account_name, db, db_connection, es_connection, dataset_info):
        self.api = api
        self.args = args
        self.account_name = account_name
        self.db = db
        self.db_connection = db_connection
        self.es_connection = es_connection
        self.dataset_info = dataset_info

        self.user = TwitterUser(self.dataset_info['dataset_directory'])
        self.tm = TweetMiner(api=api, username=account_name, num_tweets=args.tweets_number)
        self.user_tweets = []
        self.user_friends = []
        self.user_followers = []
        self.user_favorites = []
        self.tf = TwitterFriends(api=self.api)
        self.tfollower = TwitterFollowers(username=self.account_name, api=self.api)
        self.t_favorites = TwitterFavorites(username=self.account_name, api=self.api)

    def get_user_information(self):
        try:
            self.timer_user_info.start()
            self.user.set_user_information(self.api.get_user(self.account_name))
            self.es_connection.create_index(index_name=self.es_connection.twitter_user_index_name,
                                            mapping_file=self.es_connection.twitter_user_mapping_file,
                                            debug=self.args.debug)
            self.es_connection.store_information_to_elasticsearch(index_name=self.es_connection.twitter_user_index_name,
                                                                  info=self.user.user,
                                                                  debug=self.args.debug)
            self.timer_user_info.stop()
        except tweepy.error.TweepError as e:
            print('[+] Exception: {}'.format(e))
            logging.critical("[main.test_user] Error: {}".format(e))

    def get_user_output(self):
        if self.args.output == 'json' or self.args.output == 'all':
            file_name = self.dataset_info['dataset_users_file_name'] + '.json'
            self.user.get_json_output(file_name=file_name, dataset_directory=self.dataset_info['dataset_directory'])
            print('[+] {} output file created'.format(file_name))
            logging.info('[seada.get_user_information] JSON output file created')

        if self.args.output == 'csv' or self.args.output == 'all':
            file_name = self.dataset_info['dataset_users_file_name'] + '.csv'
            self.user.get_csv_output(file_name=file_name, dataset_directory=self.dataset_info['dataset_directory'])
            print('[+] {} output file created'.format(file_name))
            logging.info('[seada.get_user_information] CSV output file created')

        if self.args.output == 'database' or self.args.output == 'all':
            user_tuple = self.user.get_tuple_output()
            self.db.create_user(self.db_connection, user_tuple)
            print('[+] database update wih user information')
            logging.info('[seada.get_user_information] database output file created')

    def get_tweets_information(self):
        self.timer_tweets_info.start()
        self.user_tweets = self.tm.mine_tweets(self.api, self.account_name, self.args.tweets_number)
        self.es_connection.create_index(index_name=self.es_connection.twitter_tweet_index_name,
                                        mapping_file=self.es_connection.twitter_tweet_mapping_file,
                                        debug=self.args.debug)

        for tweet in self.user_tweets:
            self.es_connection.store_information_to_elasticsearch(
                index_name=self.es_connection.twitter_tweet_index_name, info=tweet.tweet, debug=self.args.debug)

        self.timer_tweets_info.stop()

    def get_tweets_output(self):
        if self.args.output == 'json' or self.args.output == 'all':
            file_name = self.dataset_info['dataset_tweets_file_name'] + '.json'
            for tweet in self.tm.tweets_instances:
                tweet.get_json_output(file_name=file_name, dataset_directory=self.dataset_info['dataset_directory'])

            print('[+] {} output file created'.format(file_name))
            logging.info('[seada.get_user_information] {} output file created'.format(file_name))

        if self.args.output == 'csv' or self.args.output == 'all':
            file_name = self.dataset_info['dataset_tweets_file_name'] + '.csv'
            for tweet in self.tm.tweets_instances:
                tweet.get_csv_output(file_name=file_name, dataset_directory=self.dataset_info['dataset_directory'])

            print('[+] {} output file created'.format(file_name))
            logging.info('[seada.get_user_information] {} output file created'.format(file_name))

        if self.args.output == 'database' or self.args.output == 'all':
            for tweet in self.tm.tweets_instances:
                self.db.create_tweet(self.db_connection, tweet.get_tuple_output_without_raw())

            print('[+] database updated with {} tweets.'.format(self.args.tweets_number))
            logging.info('[seada.get_tweets_output] database updated with {} tweets'.format(self.args.tweets_number))

    def get_friends_information(self):
        self.timer_friends_info.start()
        self.tf.get_user_friends(username=self.account_name)
        self.es_connection.create_index(index_name=self.es_connection.twitter_friend_index_name,
                                        mapping_file=self.es_connection.twitter_friend_mapping_file,
                                        debug=self.args.debug)

        data = {
            "id": self.user.id,
            "name": self.user.name,
            "screen_name": self.user.screen_name,
            "friend_list": self.tf.friends_id_list
        }

        self.es_connection.store_information_to_elasticsearch(index_name=self.es_connection.twitter_friend_index_name,
                                                              info=data, debug=self.args.debug)
        self.timer_friends_info.stop()

    def get_friends_output(self):
        if self.args.output == 'json' or self.args.output == 'all':
            file_name = self.dataset_info['dataset_friends_file_name'] + '.json'
            self.tf.get_json_output(file_name=file_name, dataset_directory=self.dataset_info['dataset_directory'])
            print('[+] {} output file created'.format(file_name))
            logging.info('[seada.get_friends_output] JSON output file created')

    def get_followers_information(self):
        self.timer_followers_info.start()
        self.tfollower.get_user_followers()
        # tfollower.get_output()

        self.es_connection.create_index(index_name=self.es_connection.twitter_follower_index_name,
                                        mapping_file=self.es_connection.twitter_follower_mapping_file,
                                        debug=self.args.debug)

        data = {
            'id': self.user.id,
            'name': self.user.name,
            'screen_name': self.user.screen_name,
            'follower_list': self.tfollower.followers_id_list
        }

        self.es_connection.store_information_to_elasticsearch(index_name=self.es_connection.twitter_follower_index_name,
                                                              info=data, debug=self.args.debug)
        self.timer_followers_info.stop()

    def get_followers_output(self):
        pass

    def get_favorites_information(self):
        self.timer_favorites_info.start()
        self.t_favorites.get_user_favorites()
        user = self.api.get_user(self.account_name)

        self.es_connection.create_index(index_name=self.es_connection.twitter_favorite_index_name,
                                        mapping_file=self.es_connection.twitter_favorite_mapping_file,
                                        debug=self.args.debug)

        for favorite in self.t_favorites.favorites_list:
            data = {
                '@user_id': user.id,
                'user_name': user.name,
                'user_screen_name': user.screen_name,
                'created_at': favorite.created_at,
                'id': favorite.id,
                'text': favorite.text,
                'source': favorite.source,
                'coordinates': favorite.coordinates,
                'place': favorite.place,
                'retweet_count': favorite.retweet_count,
                'favorite_count': favorite.favorite_count,
                'lang': favorite.lang,
                'hashtags': favorite.entities_hashtags,
                'user_mentions': favorite.entities_user_mentions,
                'urls': favorite.entities_urls
            }

            self.es_connection.store_information_to_elasticsearch(
                index_name=self.es_connection.twitter_favorite_index_name, info=data, debug=self.args.debug)

        self.timer_favorites_info.stop()

    def get_favorites_output(self):
        pass
