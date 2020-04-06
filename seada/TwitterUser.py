#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import SeadaUtils
import json
from elasticsearch import Elasticsearch


class TwitterUser:
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
        self.elasticsearch = Elasticsearch()

    def set_user_information(self, user):
        """
        Set user information from tweepy object user.
        :param user: tweepy object user
        :return: None
        """
        self.raw_json_user = SeadaUtils.SeadaUtils.json_to_string(user)
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
        self.user['created_at'] = str(user.created_at)
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
        td = datetime.today() - self.created_at
        # print("[user] td: %s" % str(td))
        # print("[user] td: {datatime}".format(datatime=td))

        if td.days > 0:
            self.tweets_average = round(float(self.statuses_count / (td.days * 1.0)), 3)
            self.likes_average = round(float(self.favourites_count / (td.days * 1.0)), 3)
        else:
            self.tweets_average = self.statuses_count
            self.likes_average = self.favourites_count

        # print("[user] tweets average: %s" % str(self.tweets_average))
        # print("[user] likes average: %s" % str(self.likes_average))

    def get_csv_output(self, file_name, dataset_directory):
        """
        Generate a cvs file from user information instance. If the file exists, append info in new row.
        :return: a new csv file or a new row.
        """
        item = list(self.get_tuple_output())
        item.pop(-1)
        SeadaUtils.SeadaUtils.get_csv_output(file_name, dataset_directory, item)

    def get_json_output(self, file_name, dataset_directory):
        """
        Generate a json file from user information. If the file exists, append new item.
        :return: a new json file, or a new item
        """
        SeadaUtils.SeadaUtils.get_json_output(file_name, dataset_directory, self.user)

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

    def ingest_user_information_to_elasticsearch(self):
        index = "twitter-user"
        doc_type = "user"
        # doc_type = "new-tweet"
        self.user['timestamp'] = '1585428004495'

        response = self.elasticsearch.index(index=index, doc_type=doc_type, body=self.user)
        print(response['result'])

    def ingest_user_information_to_elasticsearch_v2(self):
        index_name = "twitter-user"
        #doc_type = "user"
        # doc_type = "new-tweet"
        self.user['@timestamp'] = datetime.now()

        #response = self.elasticsearch.index(index=index, doc_type=doc_type, body=self.user)


        with open('elastic/user_mapping.json', 'r') as myfile:
            data = myfile.read()

        settings_file = json.loads(data)

        print(type(settings_file))
        print(settings_file)

        #response = self.elasticsearch.indices.create(index=index_name, body=settings_file)
        #print(response)
        print()

        response = self.elasticsearch.index(index=index_name, id=9, body=self.user)
        print(response)







