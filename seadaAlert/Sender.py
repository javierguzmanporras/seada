#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging
from logging import Handler, Formatter

import requests

token = '1262332778:AAH5EDRl25ZpHS5NoLKytiI7Bieg-YWrdjg'
chat_id = '366665070'

class RequestsHandler(Handler):
    def emit(self, record):
        log_entry = self.format(record)
        payload = {
            'chat_id': chat_id,
            'text': log_entry,
            'parse_mode': 'HTML'
        }
        return requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=token),
                             data=payload).content


class LogstashFormatter(Formatter):
    def __init__(self):
        super(LogstashFormatter, self).__init__()

    def format(self, record):
        t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        return "<i>{datetime}</i><pre>\n{message}</pre>".format(message=record.msg, datetime=t)



class Sender:

    def __init__(self):
        pass
        # logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        # logger = logging.getLogger('seadaAlert-bot')

    def sendMessageToBot(self, message):
        # updater = Updater(token=self.token)
        # dispatcher = updater.dispatcher

        logger = logging.getLogger('seadaAlert-bot')
        logger.setLevel(logging.INFO)
        handler = RequestsHandler()
        formatter = LogstashFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.error(message)



