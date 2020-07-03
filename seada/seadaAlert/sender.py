#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging
from logging import Handler, Formatter

import requests


class RequestsHandler(Handler):

    def __init__(self, telegram_token, telegram_chat_id):
        super(RequestsHandler, self).__init__()
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id

    def emit(self, record):
        log_entry = self.format(record)
        payload = {
            'chat_id': self.telegram_chat_id,
            'text': log_entry,
            'parse_mode': 'HTML'
        }
        return requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=self.telegram_token),
                             data=payload).content


class LogstashFormatter(Formatter):
    def __init__(self):
        super(LogstashFormatter, self).__init__()

    def format(self, record):
        t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        return "<i>{datetime}</i><pre>\n{message}</pre>".format(message=record.msg, datetime=t)


class SenderTelegramMessages:

    def __init__(self, alert_config):
        self.telegram_username = alert_config.telegram[0]['username']
        self.telegram_token = alert_config.telegram[1]['token']
        self.telegram_chat_id = alert_config.telegram[2]['chatid']

    def send_message_to_bot(self, message):
        logger = logging.getLogger(self.telegram_username)
        logger.setLevel(logging.INFO)
        handler = RequestsHandler(self.telegram_token, self.telegram_chat_id)
        formatter = LogstashFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        message_body = ""
        for alert in message:
            message_body = message_body + """
            [+] SEADA alert:            
            user_name: {}
            created: {} 
            tweet ID: {} 
            text: {}
            hashtags: {}
            user_mentions: {}
            """.format(alert['user_name'], alert['created_at'], alert['id'], alert['text'], alert['hashtags'],
                       alert['user_mentions'])

        logger.error(message_body)
