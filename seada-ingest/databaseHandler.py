# -*- coding: utf-8 -*-

import sqlite3
import logging


class Database:
    """Database for dataset output"""

    def __init__(self):
        pass

    def create_connection(self, database_name):
        """ create a database connection to the SQLite database specified by database_name
        :param database_name: database file
        :return: Connection object or None
        """
        connection = None
        try:
            connection = sqlite3.connect(database_name)
        except sqlite3.Error as error:
            print('[+] Error with database connection: {}'.format(error))
            logging.critical("[Database.create_connection] Connection Exception: {}".format(error))

        return connection

    def create_table(self, connection):
        """
        Create a user or tweet table
        :param connection:
        :return:
        """

        user_sql_query = "CREATE TABLE IF NOT EXISTS user(id integer PRIMARY KEY, name text, screen_name text, " \
                         "location text, description test, url text, protected text, followers_count text, " \
                         "friends_count text, listed_count text, created_at text, favourites_count text, " \
                         "geo_enabled text, verified text, statuses_count text, profile_image_url_https text, " \
                         "profile_banner_url text, default_profile text, default_profile_image text, raw_user text)"

        tweet_sql_query = "CREATE TABLE IF NOT EXISTS tweet(id integer PRIMARY KEY, created_at text, text text, " \
                          "truncated text," \
                          "source text, in_reply_to_status_id_str text, in_reply_to_user_id_str text," \
                          "in_reply_to_screen_name text, coordinates text, place text, contributors text, " \
                          "is_quote_status text, retweet_count text, favorite_count text, favorited text, " \
                          "retweetd text, possibly_sensitive text, lang text, user_id text, user_name text, " \
                          "user_screen_name text, hashtags text, user_mentions text, urls text)"

        friend_table_sql_query = "CREATE TABLE IF NOT EXISTS friend(friend_id integer PRIMARY KEY, user_id text)"

        follower_table_sql_query = "CREATE TABLE IF NOT EXISTS follower(follower_id integer PRIMARY KEY, user_id text)"

        favorites_table_sql_query = "CREATE TABLE IF NOT EXISTS favorite(favorite_id integer PRIMARY KEY, " \
                                    "user_id text, favorite_created_at text, favorite_text text, " \
                                    "favorite_source text, favorite_place text, " \
                                    "favorite_retweet_count text, favorite_favorite_count text, favorite_lang text, " \
                                    "favorite_hashtags text, favorite_user_mentions text, favorite_urls text)"

        try:
            cursor = connection.cursor()
            cursor.execute(user_sql_query)
            cursor.execute(tweet_sql_query)
            cursor.execute(friend_table_sql_query)
            cursor.execute(follower_table_sql_query)
            cursor.execute(favorites_table_sql_query)
            connection.commit()
        except sqlite3.Error as error:
            print('[+] Error with database table creation: {}'.format(error))
            logging.critical("[Database.create_table] Exception: {}".format(error))
        except Exception as exception:
            print('[+] Error at create table in database: {}'.format(exception))
            logging.error('[Database.create_table] Exception: {}'.format(exception))

    def create_user(self, connection, user):
        """
        Create a new user into the users table
        :param connection: Connection to database
        :param user: Tuple object of User
        :return: ID of the last update row
        """

        sql_query = '''INSERT INTO user(id, name, screen_name, location, description, url, protected,
        followers_count, friends_count, listed_count, created_at, favourites_count, geo_enabled, verified,
        statuses_count, profile_image_url_https, profile_banner_url, default_profile, default_profile_image, raw_user) 
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

        cursor = connection.cursor()
        try:
            cursor.execute(sql_query, user)
        except sqlite3.IntegrityError:
            logging.warning('[Database.create_user] User {} was created before in database'.format(user))

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
                 retweet_count, favorite_count, favorited, retweetd, possibly_sensitive, lang, user_id, user_name, 
                 user_screen_name, hashtags, user_mentions,
                 urls) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

        cursor = connection.cursor()
        try:
            cursor.execute(sql_query, tweet)
        except sqlite3.IntegrityError:
            logging.warning('[Database.create_tweet] Tweet was created before in database')
        except sqlite3.InterfaceError:
            logging.error('[Database.create_tweet] Error with sqlite3.Interface')
        except Exception as exception:
            logging.error('[database.create_tweet] Exception: {}'.format(exception))

        connection.commit()
        return cursor.lastrowid

    def create_friend(self, connection, friend):
        sql_query = '''INSERT INTO friend(friend_id, user_id) VALUES (?,?)'''
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query, friend)
        except sqlite3.IntegrityError:
            logging.error('[database.create_friend] Friend was created before in database')
        except sqlite3.InterfaceError:
            logging.error('[database.create_friend] Interface error')
        except Exception as exception:
            logging.error('[database.create_friend] Exception: {}'.format(exception))

        connection.commit()
        return cursor.lastrowid

    def create_follower(self, connection, follower):
        sql_query = '''INSERT INTO follower(follower_id, user_id) VALUES (?,?)'''
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query, follower)
        except sqlite3.IntegrityError:
            logging.error('[database.create_follower] Follower was created before in database')
        except sqlite3.InterfaceError:
            logging.error('[database.create_follower] Interface error')
        except Exception as exception:
            logging.error('[database.create_follower] Exception: {}'.format(exception))

        connection.commit()
        return cursor.lastrowid

    def create_favorites(self, connection, favorite):
        sql_query = '''INSERT INTO favorite(favorite_id, user_id, favorite_created_at, favorite_text,
        favorite_source, favorite_place, favorite_retweet_count, favorite_favorite_count,
        favorite_lang, favorite_hashtags, favorite_user_mentions, favorite_urls) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'''

        cursor = connection.cursor()
        try:
            cursor.execute(sql_query, favorite)
        except sqlite3.IntegrityError:
            logging.error('[database.create_favorites] Favorite was created before in database')
        except sqlite3.InterfaceError:
            logging.error('[database.create_favorites] Interface error')
        except Exception as exception:
            logging.error('[database.create_favorites] Exception: {}'.format(exception))

        connection.commit()
        return cursor.lastrowid
