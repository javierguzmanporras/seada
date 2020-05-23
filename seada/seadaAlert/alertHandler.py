# -*- coding: utf-8 -*-

import logging
import yaml


class AlertHandler:
    """"""

    def __init__(self):
        pass

    def get_config(file_config):

        config = None

        try:
            with open(file_config) as file:
                config = yaml.safe_load(file)
        except Exception as exception:
            print('[+] Error with config file.')
            logging.error('[seadaAlert.get_config] Exception at config file: {}'.format(exception))

        return config


    def start(self):
        config = None
        config = self.get_config(file_config='seada-alert-config.yml')

        if config:
            es = config_elasticsearch(config['es_host'], config['es_port'])
            print('type: {}'.format(type(es)))
