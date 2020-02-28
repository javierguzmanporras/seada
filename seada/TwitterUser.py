#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import csv
import datetime


class TwitterUser:
    """Information about a Twitter user"""

    def __init__(self):
        self.id = ""
        self.id_str = ""
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
        self.json_user = {}
        self.tweets_average = ""
        self.likes_average = ""

    def json_to_string(self, json_information):
        """convert json to string"""
        json_str = json.dumps(json_information._json)
        print(type(json_str))
        print(json_str)

    def set_user_information(self, user):
        self.id = user.id
        self.json_user['id'] = user.id
        self.id_str = user.id_str
        self.json_user['id_str'] = user.id_str
        self.name = user.name
        self.json_user['name'] = user.name
        self.screen_name = user.screen_name
        self.json_user['screen_name'] = user.screen_name
        self.location = user.location
        self.json_user['location'] = user.location
        self.description = user.description
        self.json_user['description'] = user.description
        self.url = user.url
        self.json_user['url'] = user.url
        self.protected = user.protected
        self.json_user['protected'] = user.protected
        self.followers_count = user.followers_count
        self.json_user['followers_count'] = user.followers_count
        self.friends_count = user.friends_count
        self.json_user['friends_count'] = user.friends_count
        self.listed_count = user.listed_count
        self.json_user['listed_count'] = user.listed_count
        self.created_at = user.created_at
        self.json_user['created_at'] = str(user.created_at)
        self.favourites_count = user.favourites_count
        self.json_user['favourites_count'] = user.favourites_count
        self.geo_enabled = user.geo_enabled
        self.json_user['geo_enabled'] = user.geo_enabled
        self.verified = user.verified
        self.json_user['verified'] = user.verified
        self.statuses_count = user.statuses_count
        self.json_user['statuses_count'] = user.statuses_count
        self.profile_image_url_https = user.profile_image_url_https
        self.json_user['profile_image_url_https'] = user.profile_image_url_https
        self.profile_banner_url = user.profile_banner_url
        self.json_user['profile_banner_url'] = user.profile_banner_url
        self.default_profile = user.default_profile
        self.json_user['default_profile'] = user.default_profile
        self.default_profile_image = user.default_profile_image
        self.json_user['default_profile_image'] = user.default_profile_image

        td = datetime.datetime.today() - self.created_at
        print("[user] td: %s" % str(td))
        print("[user] td: {}".format(td))

        if td.days > 0:
            self.tweets_average = round(float(self.statuses_count / (td.days * 1.0)), 2)
            self.likes_average = round(float(self.favourites_count / (td.days * 1.0)), 2)
        else:
            self.tweets_average = self.statuses_count
            self.likes_average = self.favourites_count

        print("[user] tweets average: %s" % str(self.tweets_average))
        print("[user] likes average: %s" % str(self.likes_average))
        print("[user] profile image url: %s" % str(self.profile_image_url_https))
        print("[user] profile banner url: %s" % str(self.profile_banner_url))

    def get_csv_output(self):
        with open('user_file.csv', mode='w') as user_file:
            user_writer = csv.writer(user_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # user_writer.writerow(["", "InfoBot Report"])
            # user_writer.writerow(["", ">>> Date:", datetime.datetime.now().strftime('%Y-%m-%d')])
            # user_writer.writerow(["", ">>> Time:", datetime.datetime.now().strftime('%H:%M')])
            # user_writer.writerow(["", ">>> Analyzed user:", self.screen_name])
            user_writer.writerow([self.id,
                                  self.name,
                                  self.screen_name,
                                  self.location,
                                  self.description,
                                  self.url,
                                  self.protected,
                                  self.followers_count,
                                  self.friends_count,
                                  self.listed_count,
                                  self.created_at,
                                  self.favourites_count,
                                  self.geo_enabled,
                                  self.verified,
                                  self.statuses_count,
                                  self.profile_image_url_https,
                                  self.profile_banner_url,
                                  self.default_profile,
                                  self.default_profile_image])

    def get_json_output(self):
        with open('user_file.json', mode='w') as user_file:
            json.dump(self.json_user, user_file)

    def get_tuple_output(self):
        tuple_user = (self.id, self.name, self.screen_name, self.location, self.description, self.url,
                      self.protected, self.followers_count, self.friends_count, self.listed_count, self.created_at,
                      self.favourites_count, self.geo_enabled, self.verified, self.statuses_count,
                      self.profile_image_url_https, self.profile_banner_url, self.default_profile,
                      self.default_profile_image)

        return tuple_user
