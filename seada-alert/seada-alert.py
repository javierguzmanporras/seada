#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DEASOS - Data Extraction and Analysis System from Open Sources

import argparse
import time
import logging
import os
import sys

import yaml
from Alert import *
from Sender import *
from elasticsearch import Elasticsearch
from ElasticsearchUtils import *
from time import sleep

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
    
    
# def test_elastic():
#     es = Elasticsearch()
#     res = es.search(index="twitter-user", body={"query": {"match_all": {}}})
#     print("Got %d Hits:" % res['hits']['total']['value'])
#     for hit in res['hits']['hits']:
#         print(hit["_source"])
#         print(type(hit["_source"]))
#         if hit["_source"]["screen_name"] == "kinomakino":
#             print("RED ALERT!!!  send alarm!!")


def send_telegram_message(message):
    s = Sender()
    s.sendMessageToBot(message)


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

    with open (file_config) as file:
        config = yaml.safe_load(file)

    # print(str(type(config)) + ": " + str(config))
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
    # print(alerts_folder)

    for f in os.listdir(alerts_folder):
        if f.endswith('yml'):
            path = alerts_folder + "/" + str(f)
            with open(path) as caf:
                alerts.append(Alert(yaml.safe_load(caf)))
                n_alerts = n_alerts + 1

    return n_alerts, alerts


def config_elasticsearch(es_host, es_port):
    _es = None
    _es = ElasticSearchUtils(es_host=es_host, es_port=es_port)
    es_connection = _es.connect_elasticsearch()
    if es_connection:
        _es.es_connection = es_connection

    return _es


def search(es, alert):

    query = {
  "query": {
    "bool": {
      "should": [
        { "match": { "text": "#VANESA"}}
      ],
      "minimum_should_match": 1
    }
  },
  "_source": {
    "includes": [ "user_name", "user_screen_name", "@timestamp", "text"]
  }
}
    alarm_info = None
    response = None

    try:
        response = es.es_connection.search(index=alert.index, body=query)
    except:
        print("Error with query!!")

    if response:
        if response['hits']['total']['value'] > 0:
            print("Got %d Hits: RED ALERT!!!  send alarm!!" % response['hits']['total']['value'])
            alarm_info = response['hits']['hits'][0]["_source"]

    return alarm_info


def send_alert(alert_config, alert_info):
    print("sending alert...")
    print()
    print(alert_info)
    print()
    print(alert_config)

    if "email" in alert_config.outputs:
        print("Command email yeah!")

    if "telegram" in alert_config.outputs:
        send_telegram_message(message=alert_info)
        print("Command telegram yeah!")

    print("Alert sended...")


def main():
    args = parse_args()
    config_logging()
    banner()

    if args.config:
        config = get_config(file_config=args.config)

    es = config_elasticsearch(config['es_host'], config['es_port'])
    n_alerts_loaded, alerts = load_alerts(config['alerts_folder'])
    print("[seada-alert] " + str(n_alerts_loaded) + " alerts loaded...")

    for alert in alerts:
        print ("[seada-alert] Alert: " + str(alert))

    while True:
        for alert in alerts:
            response = search(es, alert)
            if response:
                send_alert(alert, response)

        time.sleep(config['sleep_interval'])


if __name__ == '__main__':
    main()
