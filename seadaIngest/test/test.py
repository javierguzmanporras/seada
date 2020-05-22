import unittest
import os
import tweepy
import datetime

import seadaIngest
from seadaIngest import config_twitter_api
from twitterAccount import TwitterAccount


class TestConfigTwitter(unittest.TestCase):

    def setUp(self):
        self.consumer_key = os.environ['CONSUMER_KEY']
        self.consumer_secret = os.environ['CONSUMER_SECRET']
        self.access_token = os.environ['ACCESS_TOKEN']
        self.access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

        self.dataset_suffix = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        self.dataset_directory = 'dataset'
        self.dataset_info = {
            'dataset_directory': self.dataset_directory,
            'dataset_users_file_name': 'dataset_users_{}'.format(self.dataset_suffix),
            'dataset_tweets_file_name': 'dataset_tweets_{}'.format(self.dataset_suffix),
            'dataset_friends_file_name': 'dataset_friends_{}'.format(self.dataset_suffix),
            'dataset_followers_file_name': 'dataset_followers_{}'.format(self.dataset_suffix),
            'dataset_favorites_file_name': 'dataset_favorites_{}'.format(self.dataset_suffix)
        }

    def test_config(self):
        """
        Test that it can config twitter api with Tweepy
        """
        api = config_twitter_api()
        self.assertIsInstance(api, type(tweepy.api))

    # def test_twitter_account(self):
    #      api = config_twitter_api()
    #      ta = TwitterAccount(api=api, args='', account_name='jgbarah2', db="", db_connection="", dataset_info=self.dataset_info)


if __name__ == '__main__':
    unittest.main()
