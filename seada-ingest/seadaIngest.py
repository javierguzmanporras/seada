# -*- coding: utf-8 -*-
# DEASOS - Data Extraction and Analysis System from Open Sources

import argparse
import datetime
import os
import sys
import logging

from twitterAccount import TwitterAccount
from timer import Timer
from databaseHandler import *
from tweetStreaming import *
from elasticsearchHandler import *

__version__ = 0.1


def banner():
    """
    Print a banner when the program starts
    """
    try:
        seada_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(seada_path, "../data/seada-ingest-banner.txt")
        banner_file = open(path, 'r')
        for line in banner_file.readlines():
            print(line.replace("\n", ""))
        banner_file.close()
    except FileNotFoundError:
        print('[+] Error: The banner file not found')
        logging.error('[seadaIngest.banner] Error: The banner file not found')
    except Exception as exception:
        print('[+] Exception: {}'.format(exception))
        logging.critical('[seadaIngest.banner] Exception: {}'.format(exception))
        raise


def parse_args():
    """
    Method for get the arguments input of seadaIngest tool.
    :return: A Namespace class of argparse.
    """
    parser = argparse.ArgumentParser(prog='seadaIngest.py',
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
    except KeyError as error:
        print('[+] Critical error, {} environment variable for access key not found.'.format(error))
        logging.critical('[SeadaIngest.config_twitter_api] Critical error: ' +
                         str(error) + ' environment variable for access key not found.')
        sys.exit(-1)

    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    except tweepy.TweepError as error:
        print("[+] Critical error with authentication process {}".format(error))
        logging.critical('[SeadaIngest.config_twitter_api] Critical error with auth process {}'.format(error))
        sys.exit(-1)

    return api


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
        except os.error as error:
            print("[+] Fail to create dataset folder {}. Reason: {}".format(path, error))
            logging.critical('[SeadaIngest.config_dataset_output] Fail to create dataset folder {}. '
                             'Reason: {}'.format(path, error))
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
        logging.info("SeadaIngest started!")
    except Exception as exception:
        print('[+] Fail to configure logging feature. Reason: {}'.format(exception))
        logging.critical('[seadaIngest.config_logging] Exception: {}'.format(exception))
        sys.exit(-1)


def config_elasticsearch(es_host, es_port):
    es = None
    es = ElasticSearchUtils(es_host=es_host, es_port=es_port)
    es_connection = es.connect_elasticsearch()
    if es_connection:
        es.es_connection = es_connection

    return es


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

    dataset_info = {
        'dataset_directory': dataset_directory,
        'dataset_users_file_name': 'dataset_users_{}'.format(dataset_suffix),
        'dataset_tweets_file_name': 'dataset_tweets_{}'.format(dataset_suffix),
        'dataset_friends_file_name': 'dataset_friends_{}'.format(dataset_suffix),
        'dataset_followers_file_name': 'dataset_followers_{}'.format(dataset_suffix),
        'dataset_favorites_file_name': 'dataset_favorites_{}'.format(dataset_suffix)
    }

    if args.account:
        twitter_account = TwitterAccount(api=api, args=args, account_name=args.account, db=db,
                                         db_connection=db_connection, es_connection=es, dataset_info=dataset_info)
        twitter_account.get_user_information()
        twitter_account.get_user_output()
        twitter_account.get_tweets_information()
        twitter_account.get_tweets_output()
        twitter_account.get_friends_information()
        twitter_account.get_friends_output()
        twitter_account.get_followers_information()
        twitter_account.get_followers_output()
        twitter_account.get_favorites_information()
        twitter_account.get_favorites_output()

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
        twitter_accounts = []
        for account in args.account_list:
            twitter_account = TwitterAccount(api=api, args=args, account_name=account, db=db,
                                             db_connection=db_connection, es_connection=es, dataset_info=dataset_info)
            twitter_account.get_user_information()
            twitter_account.get_user_output()
            twitter_account.get_tweets_information()
            twitter_account.get_tweets_output()
            twitter_account.get_friends_information()
            twitter_account.get_friends_output()
            twitter_account.get_followers_information()
            twitter_account.get_followers_output()
            twitter_account.get_favorites_information()
            twitter_account.get_favorites_output()

            twitter_accounts.append(twitter_account)

    if args.streaming:
        ts = TweetStreaming()
        ts.start(api, args.streaming, args, db, db_connection, dataset_directory)

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
