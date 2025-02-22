# -*- coding: utf-8 -*-
# DEASOS - Data Extraction and Analysis System from Open Sources

import argparse
import datetime
import os
import sys
import logging
import tweepy

from seadaIngest.twitterAccount import TwitterAccount
from seadaIngest.timer import Timer
from seadaIngest.databaseHandler import Database
from seadaIngest.tweetStream import TweetStream
from seadaIngest.elasticsearchHandler import ElasticSearchUtils
from seadaAlert.alertHandler import AlertHandler

__version__ = 0.1


def banner(tool):
    """
    Prints a banner when the program starts
    :param tool: type of tool
    """
    try:
        if tool == 'ingest':
            banner_file = open('data/seada-ingest-banner.txt', 'r')
        elif tool == 'streaming':
            banner_file = open('data/seada-streaming-banner.txt', 'r')
        else:
            banner_file = open('data/seada-alert-banner.txt', 'r')

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
    Method for get the arguments input of seada tool.
    :return: A Namespace class of argparse.
    """
    parser = argparse.ArgumentParser(prog='seada.py',
                                     description='Sistema de Extracción y Análisis de Datos de fuentes Abiertas',
                                     epilog='Enjoy! :)')

    parser.add_argument('-f', '--feature', choices=['ingest', 'alert', 'streaming'], default='None', required=True,
                        help='Type of feature, ingest information tool or alert tool')

    parser.add_argument('-c', '--config', type=str, help='Config file in yaml format for alert feature.')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-a', '--account', metavar='ACCOUNT', type=str, help='User twitter account')

    group.add_argument('-al', '--account_list', metavar='ACCOUNT-LIST', type=str, nargs='+',
                       help='User terms_list twitter account')

    group.add_argument('-sl', '--streaming_list', type=str, nargs='+', help='Download twitter messages in real time.')

    parser.add_argument('-n', '--tweets_number', default=100, type=int,
                        help='Number of tweets that will get from user. Default=100.')

    parser.add_argument('-o', '--output', choices=['csv', 'json', 'database', 'all'], default='None',
                        help='Types of output between json, csv or database. Default=None.')

    parser.add_argument('-of', '--output_folder', default='../data/dataset',
                        help='Save the dataset output into specific folder. Default=seada/data/dataset')

    parser.add_argument('-d', '--debug', action='store_true', help='Activate debug for see more print outputs')

    parser.add_argument('-wf', '--without_favorites', action='store_true',
                        help='Get data without favorites')

    parser.add_argument('-v', '--version', action='version', version=f"%(prog)s {__version__}")
    args = parser.parse_args()
    return args


def config_twitter_api():
    """
    Method for get access keys of twitter from environment variables, create the authentication object and
    create the instance of API class.
    :return: Instance of "API" class of Tweepy
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
        path = os.path.join(seada_path, "../data/seada.log")
        logging.basicConfig(filename=path, filemode='a', format='%(asctime)s %(levelname)s-%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        logging.info("SeadaIngest started!")
    except Exception as exception:
        print('[+] Fail to configure logging feature. Reason: {}'.format(exception))
        logging.critical('[seadaIngest.config_logging] Exception: {}'.format(exception))
        sys.exit(-1)


def config_elasticsearch(es_host, es_port):
    """
    Create a elasticsearch connection
    :param es_host: Name or IP address of the elasticsearch server. By default: localhost
    :param es_port: Port of elasticsearch server. By default: 9200
    :return: A instance of ElasticSearchUtils class with a elasticsearch connection.
    """
    _es = None
    _es = ElasticSearchUtils(es_host=es_host, es_port=es_port)
    es_connection = _es.connect_elasticsearch()
    if es_connection:
        _es.es_connection = es_connection

    return _es


def alert_tool(config_dir, es_connection, debug):
    """
    Method for alert tool.
    :param config_dir: location of config yaml file
    :param es_connection: instance with elasticsearch connection
    :param debug: it indicate if seada is in debug mode
    :return:
    """
    alert_handler = AlertHandler(config_dir=config_dir, es_connection=es_connection, debug=debug)
    alert_handler.start()


def ingest_tool(args, es, api):
    """
    Method for ingest tool.
    :param args: A Namespace class of argparse.
    :param es: instance with elasticsearch connection
    :param api: instance of Tweepy class with connection with Twitter API
    :return:
    """
    #TODO dataset_config method for set vars out from ingest_tool

    db = None
    db_connection = None

    dataset_directory = database_directory = args.output_folder
    dataset_suffix = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    database_name = 'dataset_database_{}.db'.format(dataset_suffix)
    database_path = database_directory + '/' + database_name
    config_dataset_output(dataset_directory)

    if args.output == 'database' or args.output == 'all':
        db, db_connection = config_database(database_path)

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

        if not args.without_favorites:
            twitter_account.get_favorites_information()
            twitter_account.get_favorites_output()

        print('[+] Download and storage {user} information in {time} seconds.'.format(user=args.account,
                                                                                      time=Timer.timers['user_info']))

        print('[+] Download and storage {tweets} tweets of {user} in {time} seconds'.format(
            tweets=args.tweets_number,
            user=args.account,
            time=Timer.timers['tweets_info']))

        print('[+] Download {user} friend terms_list in {time} secods'.format(user=args.account,
                                                                        time=Timer.timers['friends_info']))

        print('[+] Download {} follower terms_list in {} seconds'.format(args.account, Timer.timers['followers_info']))

        if not args.without_favorites:
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

            if not args.without_favorites:
                twitter_account.get_favorites_information()
                twitter_account.get_favorites_output()

            twitter_accounts.append(twitter_account)


def streaming_tool(api, track_list, dataset_db, dataset_db_connection, dataset_directory, elasticseach):
    """
    Method for streaming tool
    :param api: instance of Tweepy class with connection with Twitter API
    :param track_list: list of terms for the streaming
    :param dataset_db:
    :param dataset_db_connection:
    :param dataset_directory:
    :param elasticseach: instance with elasticsearch connection
    :return:
    """
    ts = TweetStream(api, track_list, dataset_db, dataset_db_connection, dataset_directory, elasticseach)
    ts.start()


def main():
    args = parse_args()
    config_logging()
    banner(args.feature)

    if args.debug:
        print('[+] ' + str(vars(args)) + '\n')
        logging.info('[main] {}'.format(vars(args)))

    # Elasticsearch connection
    # es = config_elasticsearch('localhost', '9200')
    es = config_elasticsearch('127.0.0.1', '9200')

    if args.feature == 'alert':
        alert_tool(config_dir=args.config, es_connection=es, debug=args.debug)
    elif args.feature == 'ingest':
        api = config_twitter_api()  # Twitter API connection
        ingest_tool(args=args, es=es, api=api)
    elif args.feature == 'streaming':
        api = config_twitter_api()  # Twitter API connection
        streaming_tool(api, args.streaming_list, None, None, None, es)
    else:
        print('[+] Nothing to do...')

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
