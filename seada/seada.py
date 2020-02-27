#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DEASOS - Data Extraction and Analysis System from Open Sources

import argparse
import os
import sys
import tweepy

__version__ = 0.1


def banner():
    """
    Function
    :return:
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

    :return:
    """
    parser = argparse.ArgumentParser(prog='seada.py',
                                     description='Sistema de Extracción y Análisis de Datos de fuentes Abiertas',
                                     epilog='Enjoy the program! :)')
    parser.add_argument('-a', '--account', metavar='ACCOUNT', type=str, help='User twitter account')
    parser.add_argument('-al', '--account-list', metavar='ACCOUNT-LIST', type=str, help='User list twitter account')
    parser.add_argument('-o', '--output', choices=['csv', 'json'], help='Type of file output')
    parser.add_argument('-v', '--version', action='version', version=f"%(prog)s {__version__}")
    args = parser.parse_args()
    return args


def config_twitter_api():
    """

    :return:
    """
    try:
        consumer_key = os.environ['CONSUMER_KEY']
        consumer_secret = os.environ['CONSUMER_SECRET']
        access_token = os.environ['ACCESS_TOKEN']
        access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

    except KeyError:
        print("Error, any access key not found...")
        print("Error: " + str(sys.exc_info()))

    return tweepy.API(auth)


def main():
    args = parse_args()
    banner()
    api = config_twitter_api()


if __name__ == '__main__':
    main()
