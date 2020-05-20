# -*- coding: utf-8 -*-

from outputUtilities import OutputUtilities
from outputInterface import OutputInterface


class TwitterUser(OutputInterface):
    """Information about a Twitter user"""

    def __init__(self, dataset_directory):
        # Account user information
        self.id = ""
        self.name = ""
        self.screen_name = ""
        self.location = ""
        self.description = ""
        self.url = ""
        self.protected = ""
        self.followers_count = ""
        self.friends_count = ""
        self.listed_count = ""
        self.created_at = ""
        self.favourites_count = ""
        self.geo_enabled = ""
        self.verified = ""
        self.statuses_count = ""
        self.profile_image_url_https = ""
        self.profile_banner_url = ""
        self.default_profile = ""
        self.default_profile_image = ""
        # other information about user
        self.tweets_average = ""
        self.likes_average = ""
        self.raw_json_user = ""
        self.user = {}
        self.dataset_directory = dataset_directory

    def set_user_information(self, user):
        """
        Set user information from tweepy object user.
        :param user: tweepy object user
        :return: None
        """
        self.raw_json_user = OutputUtilities.json_to_string(user)
        self.id = user.id
        self.user['id'] = user.id
        self.name = user.name
        self.user['name'] = user.name
        self.screen_name = user.screen_name
        self.user['screen_name'] = user.screen_name
        self.location = user.location
        self.user['location'] = user.location
        self.description = user.description
        self.user['description'] = user.description
        self.url = user.url
        self.user['url'] = user.url
        self.protected = user.protected
        self.user['protected'] = user.protected
        self.followers_count = user.followers_count
        self.user['followers_count'] = user.followers_count
        self.friends_count = user.friends_count
        self.user['friends_count'] = user.friends_count
        self.listed_count = user.listed_count
        self.user['listed_count'] = user.listed_count
        self.created_at = user.created_at
        # self.user['created_at'] = str(user.created_at)
        self.user['created_at'] = user.created_at
        self.favourites_count = user.favourites_count
        self.user['favourites_count'] = user.favourites_count
        self.geo_enabled = user.geo_enabled
        self.user['geo_enabled'] = user.geo_enabled
        self.verified = user.verified
        self.user['verified'] = user.verified
        self.statuses_count = user.statuses_count
        self.user['statuses_count'] = user.statuses_count
        self.profile_image_url_https = user.profile_image_url_https
        self.user['profile_image_url_https'] = user.profile_image_url_https
        self.default_profile = user.default_profile
        self.user['default_profile'] = user.default_profile
        self.default_profile_image = user.default_profile_image
        self.user['default_profile_image'] = user.default_profile_image

        try:
            self.profile_banner_url = user.profile_banner_url
            self.user['profile_banner_url'] = user.profile_banner_url
        except AttributeError:
            self.user['profile_banner_url'] = ""

    def get_csv_output(self, file_name, dataset_directory):
        """
        Generate a cvs file from user information instance. If the file exists, append info in new row.
        :return: a new csv file or a new row.
        """
        item = list(self.get_tuple_output())
        item.pop(-1)
        OutputUtilities.get_csv_output(file_name, dataset_directory, item)

    def get_json_output(self, file_name, dataset_directory):
        """
        Generate a json file from user information. If the file exists, append new item.
        :return: a new json file, or a new item
        """
        item = dict(self.user)
        item['created_at'] = str(item['created_at'])
        OutputUtilities.get_json_output(file_name=file_name, dataset_directory=dataset_directory,
                                        item=item, datatag='user_list')

    def get_tuple_output(self):
        """
        Generate a tuple with user information for input database
        :return: A tuple with user information
        """
        tuple_user = (self.id, self.name, self.screen_name, self.location, self.description, self.url,
                      self.protected, self.followers_count, self.friends_count, self.listed_count, str(self.created_at),
                      self.favourites_count, self.geo_enabled, self.verified, self.statuses_count,
                      self.profile_image_url_https, self.profile_banner_url, self.default_profile,
                      self.default_profile_image, self.raw_json_user)

        return tuple_user
