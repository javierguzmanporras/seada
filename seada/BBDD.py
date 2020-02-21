#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error


class BBDD:
    """Database for tweets"""

    def __init__(self):
        #self.connection
        pass

    def create_connection(self, database_name):
        """ create a database connection to the SQLite database specified by database_name
        :param db_file: database file
        :return: Connection object or None
        """
        connection = None
        try:
            connection = sqlite3.connect(database_name)
        except Error:
            print (Error)

        return connection

    def create_table(self, connection):
        """
        Create a user table
        :param connection:
        :return:
        """

        user_sql_query = "CREATE TABLE user(id integer PRIMARY KEY, name text, screen_name text, location text," \
                   "description test, url text, protected text, followers_count text, friends_count text, " \
                   "listed_count text, created_at text, favourites_count text, geo_enabled text, verified text, " \
                   "statuses_count text, profile_image_url_https text, profile_banner_url text, default_profile text," \
                   "default_profile_image)"

        tweet_sql_query = "CREATE TABLE tweet(id integer PRIMARY KEY, created_at text, text text, truncated text," \
                          "source text, in_reply_to_status_id text, )"


        self.in_reply_to_status_id = ""
        self.in_reply_to_status_id_str = ""
        self.in_reply_to_user_id = ""
        self.in_reply_to_user_id_str = ""
        self.in_reply_to_screen_name = ""
        # user
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
        # self.user_name = ""
        self.tuit = {}
        self.entities_hashtags = []
        self.entities_user_mentions = []
        self.entities_urls = []


        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
        except Error:
            print(Error)


    def create_user(self, connection, user):
        """
        Create a new project into the projects table
        :param conn:
        :param project:
        :return: project id
        """

        sql_query = '''INSERT INTO user(id, name, screen_name, location, description, url, protected,
        followers_count, friends_count, listed_count, created_at, favourites_count, geo_enabled, verified,
        statuses_count, profile_image_url_https, profile_banner_url, default_profile, default_profile_image) 
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

        cursor = connection.cursor()
        cursor.execute(sql_query, user)
        connection.commit()
        return cursor.lastrowid

