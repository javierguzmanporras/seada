#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DEASOS - Data Extraction and Analysis System from Open Sources

import argparse
import logging
import os
import sys

import yaml
from Alert import *
from Sender import *
from elasticsearch import Elasticsearch

__version__ = 0.1


def banner():
    """
    Function for print a banner
    """
    try:
        program_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(program_path, "../data/seada-alert-banner.txt")
        banner_file = open(path, 'r')
        for line in banner_file.readlines():
            print(line.replace("\n", ""))
        banner_file.close()
    except FileNotFoundError:
        print('[seada-alert.banner] Error: The banner file not found')
        logging.warning("[seada-alert.banner] Error: The banner file not found")
    except Exception as exception:
        print(exception)
        logging.warning(exception)
    
    
def test_elastic():
    es = Elasticsearch()
    res = es.search(index="twitter-user", body={"query": {"match_all": {}}})
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print(hit["_source"])
        print(type(hit["_source"]))
        if hit["_source"]["screen_name"] == "kinomakino":
            print("RED ALERT!!!  send alarm!!")


def send_telegram_message():
    s = Sender()
    s.sendMessageToBot("test")


def parse_args():
    """
    Method for get the arguments input of seada-ingest program.
    :return: A Namespace class of argparse.
    """
    parser = argparse.ArgumentParser(prog='seada-alert.py',
                                     description='Sistema de Extracción y Análisis de Datos de fuentes Abiertas',
                                     epilog='Enjoy! :)')
    parser.add_argument('-c', '--config', type=str, help='Config file in yaml format.')
    parser.add_argument('-v', '--version', action='version', version=f"%(prog)s {__version__}")
    args = parser.parse_args()
    return args


def get_config(file_config):

    print(file_config)

    with open (file_config) as file:
        config = yaml.safe_load(file)

    print(type(config))
    print(config)

    return config


def config_logging():
    """
    Config output logging file.
    :return:
    """
    try:
        program_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(program_path, "../data/seada-alert.log")
        logging.basicConfig(filename=path, filemode='a', format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        logging.info("seada-alert started!")
    except Exception as exception:
        print(exception)
        sys.exit(-1)


def load_alerts(alerts_folder):
    n_alerts = 0
    alerts = []
    print(alerts_folder)

    for f in os.listdir(alerts_folder):
        if f.endswith('yml'):
            path = alerts_folder + "/" + str(f)
            with open(path) as caf:
                alerts.append(Alert(yaml.safe_load(caf)))
                n_alerts = n_alerts + 1

    return n_alerts, alerts


def main():
    args = parse_args()
    config_logging()
    banner()

    if args.config:
        config = get_config(file_config=args.config)

    n_alerts_loaded, alerts = load_alerts(config['alerts_folder'])

    print("[seada-alert] " + str(n_alerts_loaded) + " alerts loaded...")
    print(alerts[0].name)
    print(alerts[0].type)
    print(alerts[0].list)
    print(alerts[0].outputs)
    print(alerts[0].emails)
    print(alerts[0].telegram)

    #test_elastic()
    #send_telegram_message()

    # while
        # realizar busqeda
        # enviar alerta
        # sleep 5 minutos

if __name__ == '__main__':
    main()
