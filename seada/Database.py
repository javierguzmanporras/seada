#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error


class Database:
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
                   "description test, url text, protected text, followers_count text, friends_count text," \
                   "listed_count text, created_at text, favourites_count text, geo_enabled text, verified text," \
                   "statuses_count text, profile_image_url_https text, profile_banner_url text, default_profile text," \
                   "default_profile_image)"

        tweet_sql_query = "CREATE TABLE tweet(id integer PRIMARY KEY, created_at text, text text, truncated text," \
                          "source text, in_reply_to_status_id_str text, in_reply_to_user_id_str text," \
                          "in_reply_to_screen_name text, coordinates text, place text, contributors text, " \
                          "is_quote_status text, retweet_count text, favorite_count text, favorited text, " \
                          "retweetd text, possibly_sensitive text, lang text)"

        # self.tuit = {}
        # self.entities_hashtags = []
        # self.entities_user_mentions = []
        # self.entities_urls = []

        try:
            cursor = connection.cursor()
            cursor.execute(user_sql_query)
            cursor.execute(tweet_sql_query)
            connection.commit()
        except Error:
            print(Error)

    def create_user(self, connection, user):
        """
        Create a new user into the users table
        :param connection: Connection to database
        :param user: Tuple object of User
        :return: ID of the last update row
        """

        sql_query = '''INSERT INTO user(id, name, screen_name, location, description, url, protected,
        followers_count, friends_count, listed_count, created_at, favourites_count, geo_enabled, verified,
        statuses_count, profile_image_url_https, profile_banner_url, default_profile, default_profile_image) 
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

        cursor = connection.cursor()
        cursor.execute(sql_query, user)
        connection.commit()
        return cursor.lastrowid

    def create_tweet(self, connection, tweet):
        """
        Create a new tweet into the tweets table
        :param connection: Connection object to database
        :param tweet: Tuple objetct of Tweet
        :return: ¿¿??
        """
        sql_query = '''INSERT INTO tweet(id, created_at, text, truncated, source, in_reply_to_status_id_str,
         in_reply_to_user_id_str, in_reply_to_screen_name, coordinates, place, contributors, is_quote_status, 
         retweet_count, favorite_count, favorited, retweetd, possibly_sensitive, lang)
         VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''



