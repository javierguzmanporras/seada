#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DEASOS - Data Extraction and Analysis System from Open Sources

import argparse
import os
import sys
import tweepy
from TwitterUser import *
from Database import *
from TweetMiner import *


__version__ = 0.1


def banner():
    """
    Function for print a banner
    """
    try:
        banner_file = open("banner2.txt", 'r')
        for line in banner_file.readlines():
            print(line.replace("\n", ""))
        banner_file.close()
    except FileNotFoundError:
        print('[seada.banner] Error: The banner file not found')
    except Exception as exception:
        print(exception)
        raise


def parse_args():
    """
    Method for get the arguments input of seada program.
    :return: A Namespace class of argparse.
    """
    parser = argparse.ArgumentParser(prog='seada.py',
                                     description='Sistema de Extracción y Análisis de Datos de fuentes Abiertas',
                                     epilog='Enjoy the program! :)')
    parser.add_argument('-a', '--account', metavar='ACCOUNT', type=str, help='User twitter account')
    parser.add_argument('-al', '--account_list', metavar='ACCOUNT-LIST', type=str, help='User list twitter account')
    parser.add_argument('-o', '--output', choices=['csv', 'json', 'database', 'all'], default='json',
                        help='Types of output between json, csv or database. You can chose one or all of them.')
    parser.add_argument('-v', '--version', action='version', version=f"%(prog)s {__version__}")
    args = parser.parse_args()
    return args


def config_twitter_api():
    """
    Method for get access keys of twitter from environment variables, create the authentication object and
    create the instance of API class.
    :return: Instance of "API" class of tweepy
    """
    try:
        consumer_key = os.environ['CONSUMER_KEY']
        consumer_secret = os.environ['CONSUMER_SECRET']
        access_token = os.environ['ACCESS_TOKEN']
        access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
    except KeyError:
        print("Error, any access key not found...")
        print("Error: " + str(sys.exc_info()))

    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    except tweepy.TweepError:
        print("Fatal error with authentication process")
        raise

    return api


def test_user(api, username, db, connection, dataset_directory):
    # user
    user = TwitterUser(dataset_directory)
    user.set_user_information(api.get_user(username))
    user.get_csv_output()
    user.get_json_output()
    user_tuple = user.get_tuple_output()
    print(user_tuple)
    row_id = db.create_user(connection, user_tuple)
    print("[test_user] ROW_ID: " + str(row_id))
    print()

    #tweets
    tm = TweetMiner()
    tm.mine_tweets(api, username, 3000)
    #tm.get_json_output('tweets_file.json', dataset_directory)
    tm.add_tweets_to_database(db, connection)




def config_database(db_name):
    """
    Create a database in sqlite3
    :param db_name: The name of the file for the database
    :return: A database objetc and his connections object
    """
    db = Database()
    connection = db.create_connection(db_name)
    db.create_table(connection)
    return db, connection


def config_dataset_output(path):
    """
    Config output folder for dataset
    :param path:
    :return:
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except os.error as e:
            print("[config_dataset_output] Fail to create folder" + path + str(e))


def main():
    dataset_directory = database_directory = 'dataset'
    database_name = 'twitter_database.db'
    database_path = database_directory + '/' + database_name

    args = parse_args()
    banner()
    config_dataset_output(dataset_directory)

    print(vars(args))
    print(len(args.output))




    # db, connection = config_database(database_path)
    # api = config_twitter_api()
    #
    # if args.account:
    #     test_user(api, args.account, db, connection, dataset_directory)
    #     # test_user(api, "jgp_ingTeleco", db, connection)


if __name__ == '__main__':
    main()
