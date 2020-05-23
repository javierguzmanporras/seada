#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DEASOS - Data Extraction and Analysis System from Open Sources

import argparse
import time
import logging
import os
import sys

import yaml
from .Alert import *
from .Sender import *


# currentdir = os.path.abspath("")
# new_dir = os.path.join(currentdir, "../seadaIngest/")
# sys.path.insert(0, new_dir)

from seadaIngest.elasticsearchHandler import ElasticSearchUtils

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
        print('[seadaAlert.banner] Error: The banner file not found')
        logging.warning("[seadaAlert.banner] Error: The banner file not found")
    except Exception as exception:
        print('[+] Problem with banner')
        logging.warning('[seadaAlert.banner] Exception at banner: {}'.format(exception))
    
    
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
    Method for get the arguments input of seadaAlert tool.
    :return: A Namespace class of argparse.
    """
    parser = argparse.ArgumentParser(prog='seadaAlert.py',
                                     description='Sistema de Extracción y Análisis de Datos de fuentes Abiertas',
                                     epilog='Enjoy! :)')
    parser.add_argument('-c', '--config', type=str, help='Config file in yaml format.')
    parser.add_argument('-v', '--version', action='version', version=f"%(prog)s {__version__}")
    args = parser.parse_args()
    return args


def get_config(file_config):

    config = None

    try:
        with open(file_config) as file:
            config = yaml.safe_load(file)
    except Exception as exception:
        print('[+] Error with config file.')
        logging.error('[seadaAlert.get_config] Exception at config file: {}'.format(exception))

    return config


def config_logging():
    """Config output logging file."""
    try:
        program_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(program_path, "../data/seadaAlert.log")
        logging.basicConfig(filename=path, filemode='a', format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
        logging.info("seadaAlert started!")
    except Exception as exception:
        print('[+] Error at create logging file.')
        logging.critical('[seadaAlert.config_logging] Exception with logging: {}'.format(exception))
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
    es = None
    es = ElasticSearchUtils(es_host=es_host, es_port=es_port)
    es_connection = es.connect_elasticsearch()
    if es_connection:
        es.es_connection = es_connection

    return es


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
    #args = parse_args()
    #config_logging()
    #banner()

    config = None
    config = get_config(file_config='seada-alert-config.yml')

    # print('dirname: {}'.format(os.path.dirname(__file__)))
    # print(os.path.dirname(__file__))
    # print(os.path.abspath(""))
    # print('abspath: {}'.format(os.path.abspath(os.path.dirname(__file__))))
    #
    # print()
    # print()

    # currentdir = os.path.abspath("")
    # #print('seada_alert_path: {}'.format(seada_alert_path))
    # #print('os.path: {}'.format(os.path))
    # new_dir = os.path.join(currentdir, "../seadaIngest/")
    # #print('new_path: {}'.format(new_path))
    # #print('os.path: {}'.format(os.path))
    #
    # # print(sys.path)
    # #sys.path.insert(0, new_path)
    # sys.path.append(new_path)
    # print(sys.path)


    if config:
        es = config_elasticsearch(config['es_host'], config['es_port'])
        print('type: {}'.format(type(es)))



        # n_alerts_loaded, alerts = load_alerts(config['alerts_folder'])
    #     print("[seadaAlert] " + str(n_alerts_loaded) + " alerts loaded...")
    #
    # for alert in alerts:
    #     print ("[seadaAlert] Alert: " + str(alert))
    #
    # while True:
    #     for alert in alerts:
    #         response = search(es, alert)
    #         if response:
    #             send_alert(alert, response)
    #
    #     time.sleep(config['sleep_interval'])


if __name__ == '__main__':
    main()
