#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DEASOS - Data Extraction and Analysis System from Open Sources

import argparse
import platform
import os, sys

__version__ = 0.1


def banner():
    f = open("banner2.txt",'r')
    banner = f.readlines()
    for line in banner:
        print(line.replace("\n",""))
    f.close()


def parse_args():
    parser = argparse.ArgumentParser(prog='seada.py',
                                     description='Sistema de Extracción y Análisis de Datos de fuentes Abiertas',
                                     epilog='Enjoy the program! :)')
    parser.add_argument('--account', '-a', metavar='ACCOUNT', type=str, help='User twitter account')
    parser.add_argument('--account-list', '-al', metavar='ACCOUNT-LIST', type=str, help='User list twitter account')
    parser.add_argument('--output', '-o', choices=['csv', 'json'], help='Type of file output')
    parser.add_argument('--version', '-v', action='version', version=f"%(prog)s {__version__}")
    parser.add_argument('--test', '-t', help='test')
    args = parser.parse_args()
    return args


def config():
    try:
        consumer_key = os.environ['CONSUMER_KEY']
        consumer_secret = os.environ['CONSUMER_SECRET']
        access_token = os.environ['ACCESS_TOKEN']
        access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
    except KeyError:
        print("Error, any key not found...")
        print("Error: " + str(sys.exc_info()))


def main():

    #version_string = f"%(prog)s {__version__}\n" + f"{requests.__description__}:  {requests.__version__}\n" + \
    #                 f"Python:  {platform.python_version()}"

    args = parse_args()
    banner()
    config()


if __name__ == '__main__':
    main()