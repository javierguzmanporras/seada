#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DEASOS - Data Extraction and Analysis System from Open Sources

#examples
# python3 seada-ingest.py --account kinomakino

import argparse
import datetime
import logging
import os
import sys

from seada import Seada
from timer import Timer

from databaseHandler import *
from tweetMiner import *
from tweetStreaming import *
from elasticsearchHandler import *
from twitterUser import *
from twitterFavorites import *

__version__ = 0.1


def banner():
    """
    Function for print a banner
    """
    try:
        seada_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(seada_path, "../data/seada-ingest-banner.txt")
        banner_file = open(path, 'r')
        for line in banner_file.readlines():
            print(line.replace("\n", ""))
        banner_file.close()
    except FileNotFoundError:
        print('[main][banner] Error: The banner file not found')
    except Exception as exception:
        print(exception)
        raise


def parse_args():
    """
    Method for get the arguments input of seada-ingest program.
    :return: A Namespace class of argparse.
    """
    parser = argparse.ArgumentParser(prog='seada-ingest.py',
                                     description='Sistema de Extracción y Análisis de Datos de fuentes Abiertas',
                                     epilog='Enjoy! :)')

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-a', '--account', metavar='ACCOUNT', type=str, help='User twitter account')

    group.add_argument('-al', '--account_list', metavar='ACCOUNT-LIST', type=str, nargs='+',
                       help='User list twitter account')

    group.add_argument('-s', '--streaming', type=str, nargs='+', help='Download twitter messages in real time.')

    parser.add_argument('-n', '--tweets_number', default=100, type=int,
                        help='Number of tweets that will get from user. Default=100.')

    parser.add_argument('-o', '--output', choices=['csv', 'json', 'database', 'all'], default='None',
                        help='Types of output between json, csv or database. Default=None.')

    parser.add_argument('-of', '--output_folder', default='dataset',
                        help='Save the dataset output into specific folder. Default=dataset')

    parser.add_argument('-d', '--debug', action='store_true', help='Activate debug for see more print outputs')

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
    except KeyError as e:
        print('[seada-ingest.config_twitter_api] Critical error, ' +
              str(e) + ' environment variable for access key not found.')
        logging.critical('[seada-ingest.config_twitter_api] Critical error: ' +
                         str(e) + ' environment variable for access key not found.')
        sys.exit(-1)

    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    except tweepy.TweepError as e:
        print("[seada-ingest.config_twitter_api] Critical error with authentication process " + str(e))
        logging.critical('[seada-ingest.config_twitter_api] Critical error with authentication process')
        sys.exit(-1)

    return api


def get_user_information(api, args, username, db, connection, dataset_directory, es_connect):
    user = TwitterUser(dataset_directory)
    try:
        user.set_user_information(api.get_user(username))

        # if args.output == 'csv' or args.output == 'all':
        #     user.get_csv_output('users_file.csv', dataset_directory)
        #
        # if args.output == 'json' or args.output == 'all':
        #     user.get_json_output('users_file.json', dataset_directory)
        #
        # if args.output == 'database' or args.output == 'all':
        #     user_tuple = user.get_tuple_output()
        #     row_id = db.create_user(connection, user_tuple)

        user_index_name = "twitter_user"
        user_mapping_file = "elasticsearch_twitter_user_index_mapping.json"
        es_connect.create_index(index_name=user_index_name, mapping_file=user_mapping_file)
        es_connect.store_information_to_elasticsearch(index_name=user_index_name, info=user.user)

    except tweepy.error.TweepError as e:
        print("[main.test_user] Error: " + str(e))


def get_tweets_information(api, args, username, db, connection, dataset_directory, ntweets, es_connect):
    tm = TweetMiner()
    tweets_instances, tweets = tm.mine_tweets(api, username, ntweets)

    # if args.output == 'json' or args.output == 'all':
    #     for tweet in tweets_instances:
    #         tweet.get_json_output('tweets_file.json', dataset_directory)
    #
    # if args.output == 'csv' or args.output == 'all':
    #     for tweet in tweets_instances:
    #         tweet.get_csv_output('tweets_file.csv', dataset_directory)
    #
    # if args.output == 'database' or args.output == 'all':
    #     for tweet in tweets_instances:
    #         db.create_tweet(connection, tweet.get_tuple_output())

    tweet_index_name = "twitter_tweets"
    tweet_mapping_file = "elasticsearch_twitter_tweets_index_mapping.json"
    es_connect.create_index(index_name=tweet_index_name, mapping_file=tweet_mapping_file)
    for tweet in tweets_instances:
        es_connect.store_information_to_elasticsearch(index_name=tweet_index_name, info=tweet.tweet)


def get_streaming(api, args, db, connection, dataset_directory, es_connect):
    ts = TweetStreaming()
    ts.start(api, args.streaming, args, db, connection, dataset_directory)


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
    :param path: Folder's path for dataset files.
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except os.error as e:
            print("[config_dataset_output] Fail to create folder " + path + ". Reason: " + str(e))
            sys.exit(-1)


def config_logging():
    """
    Config output logging file.
    :return:
    """
    try:
        seada_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(seada_path, "../data/seada-ingest.log")
        logging.basicConfig(filename=path, filemode='a', format='%(asctime)s %(levelname)s-%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        logging.info("seada-ingest started!")
    except Exception as exception:
        print(exception)
        sys.exit(-1)


def config_elasticsearch(es_host, es_port):
    _es = None
    _es = ElasticSearchUtils(es_host=es_host, es_port=es_port)
    es_connection = _es.connect_elasticsearch()
    if es_connection:
        _es.es_connection = es_connection

    return _es


def main():
    args = parse_args()
    config_logging()
    banner()

    if args.debug:
        print('[+] ' + str(vars(args)) + '\n')
        logging.info('[main] {}'.format(vars(args)))

    dataset_directory = database_directory = args.output_folder
    dataset_suffix = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    database_name = 'dataset_database_{}.db'.format(dataset_suffix)
    database_path = database_directory + '/' + database_name

    config_dataset_output(dataset_directory)
    db = None
    db_connection = None
    if args.output == 'database' or args.output == 'all':
        db, db_connection = config_database(database_path)

    es = config_elasticsearch('localhost', '9200')
    api = config_twitter_api()

    seada = Seada(api=api,
                  args=args,
                  db=db,
                  db_connection=db_connection,
                  dataset_directory=dataset_directory,
                  es_connect=es)

    if args.account:
        seada.get_user_information(username=args.account)
        seada.get_user_output(file_name='dataset_users_{}'.format(dataset_suffix))
        seada.get_tweets_information(username=args.account, ntweets=args.tweets_number)
        seada.get_tweets_output(file_name='dataset_tweets_{}'.format(dataset_suffix))
        seada.get_friends_information(username=args.account)
        seada.get_friends_output(file_name='dataset_friends_{}'.format(dataset_suffix))
        #seada.get_followers_information(username=args.account)
        #seada.get_favorites_information(username=args.account)

        print('[+] Download and storage {user} information in {time} seconds.'.format(user=args.account,
                                                                                      time=Timer.timers['user_info']))

        print('[+] Download and storage {tweets} tweets of {user} in {time} seconds'.format(
            tweets=args.tweets_number,
            user=args.account,
            time=Timer.timers['tweets_info']))

        print('[+] Download {user} friend list in {time} secods'.format(user=args.account,
                                                                        time=Timer.timers['friends_info']))

        print('[+] Download {} follower list in {} seconds'.format(args.account, Timer.timers['followers_info']))
        print('[+] Download {} favorites in {} seconds'.format(args.account, Timer.timers['favorites_info']))

    if args.account_list:
        for account in args.account_list:
            get_user_information(api, args, account, db, db_connection, dataset_directory, es_connect=es)
            get_tweets_information(api, args, account, db, db_connection, dataset_directory, args.tweets_number,
                                   es_connect=es)

    if args.streaming:
        get_streaming(api, args, db, db_connection, dataset_directory, es_connect=es)

    sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit) as e:
        sys.stdout.flush()
        exit(1)
    except Exception as e:
        print(str(e))
        exit(1)
