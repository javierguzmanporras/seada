# -*- coding: utf-8 -*-

import logging
import yaml
import os
import sys
import time

from datetime import datetime
from datetime import timedelta

#email
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from seadaAlert.alert import Alert
from seadaAlert.sender import SenderTelegramMessages


class AlertHandler:
    """Alerts Handler"""

    def __init__(self, config_dir, es_connection, debug):
        self.config_dir = config_dir
        self.es = es_connection
        self.debug = debug

    def get_config(self):
        config = None

        try:
            with open(self.config_dir) as file:
                config = yaml.safe_load(file)
        except Exception as exception:
            print('[+] Error with config file.')
            logging.error('[AlertHandler.get_config] Exception at config file: {}'.format(exception))

        return config

    def load_alerts(self, alerts_folder):
        alerts = []

        try:
            for f in os.listdir(alerts_folder):
                if f.endswith('yml'):
                    path = alerts_folder + "/" + str(f)

                    try:
                        with open(path) as caf:

                            try:
                                info = yaml.safe_load(caf)
                            except yaml.YAMLError as yerror:
                                print('[+] Exception at load yaml information: {}'.format(yerror))
                                logging.error('[AlertHandler.load_alerts] Exception at load '
                                              'yaml file: {}'.format(yerror))

                            a = Alert(info)
                            alerts.append(a)
                    except Exception as exception:
                        print('[+] Exception at open yaml file: {}'.format(exception))
                        logging.error('[AlertHandler.load_alerts] Exception at load yaml file: {}'.format(exception))

        except Exception as exception:
            print('[+] Exception at load alerts: {}'.format(exception))
            logging.critical('[AlertHandler.load_alerts] Exception: {}'.format(exception))

        return alerts

    def search(self, alert):
        query_one_term = False
        query_n_term = False
        response = None
        search_response = False
        query = ""
        items_search_response = []

        if len(alert.terms_list) > 1:
            query_n_term = True
        else:
            query_one_term = True

        # lte: Less than or equal to
        # gte: Greater than or equal to
        lte = datetime.now().isoformat()
        gte = (datetime.now() - timedelta(seconds=alert.interval_time)).isoformat()

        if self.debug:
            print('[+] gte:{}, lte:{}'.format(gte, lte))

        if query_one_term:
            term = alert.terms_list[0]
            query = {
              "size": 1000,
              "query": {
                "bool": {
                  "should": [
                    {"match": {"text": term}}
                  ],
                  "minimum_should_match": 1,
                  "filter":
                    {"range": {
                        "@timestamp": {
                          "gte": gte,
                          "lte": lte
                        }
                      }
                    }
                }
              },
              "_source": {
                "includes": ["id", "user_name", "text", "created_at", "hashtags", "user_mentions"]
              }
            }

        if query_n_term:
            terms = ""
            for term in alert.terms_list:
                terms = terms + term + " "

            query = {
              "size": 1000,
              "query": {
                "bool": {
                  "should": [
                    {
                      "multi_match": {
                        "query": terms,
                        "fields": "text",
                        "operator": alert.operator
                      }
                    }
                  ],
                  "minimum_should_match": 1,
                  "filter": [
                    {"range": {"@timestamp": {"gte": gte, "lte": lte}}}
                  ]
                }
              },
              "_source": {
                "includes": ["id", "user_name", "text", "created_at", "hashtags", "user_mentions"]
              }
            }

            # query = {
            #   "size": 1000,
            #   "query": {
            #     "match": {
            #       "text": {
            #         "query": terms,
            #         "operator": alert.operator
            #       }
            #     }
            #   },
            #   "_source": {
            #     "includes": ["id", "user_name", "text", "created_at", "hashtags", "user_mentions"]
            #   }
            # }

        try:
            if self.debug:
                print('index: {}'.format(alert.index))
                print('query: {}'.format(query))
                logging.debug('[AlertHandler.search] index: {}'.format(alert.index))
                logging.debug('[AlertHandler.search] query: {}'.format(query))

            response = self.es.es_connection.search(index=alert.index, body=query)
        except Exception as exception:
            print("[+] Error at search: {}".format(exception))
            logging.error('[AlertHandler.search] Error at search: {}'.format(exception))

        if response:
            if response['hits']['total']['value'] > 0:
                search_response = True
                print('[+] {} Got {} hits: RED ALERT!!.'.format(datetime.now(), response['hits']['total']['value']))
                logging.info('[AlertHandler.search] Got {} hits: '
                             'RED ALERT!!.'.format(response['hits']['total']['value']))

                for source in response['hits']['hits']:
                    items_search_response.append(source['_source'])

        return search_response, items_search_response

    def send_email_message(self, alert_config, alert_info):
        """
        Method for send emails messages by gmail
        :param alert_config: needed information for send email
        :param alert_info: Alert's information.
        :return: True if email sended and False if not.
        """
        # we need that receiver_email will be a list of strings and message["To"] will be a string with emails into ""
        # Example:
        # receiver_email = ["seada.alerts@gmail.com", "javier.guzman.porras@gmail.com"]
        # message["To"] = '"javier.guzman.porras@gmail.com", "seada.alerts@gmail.com"'

        send = False

        to = ""
        for e in alert_config.emails:
            to = to + '\"' + e + '\"' + ', '

        port = 465  # For SSL
        sender_email = "seada.alerts@gmail.com"
        receiver_email = alert_config.emails
        password = alert_config.email[0]['password']

        message = MIMEMultipart()
        message["Subject"] = "SEADA Alert"
        message["From"] = sender_email

        message["To"] = to

        message_body = ''

        for alert in alert_info:
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

        table_body = ''
        table = """
        <table>
          <tr>
            <th>User Name</th>
            <th>Created at</th>
            <th>tweet ID</th>
            <th>text</th>
            <th>Hashtags</th>
            <th>User mentions</th>            
          </tr>
        """

        for alert in alert_info:
            table_body = table_body + """
            <tr>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
            </tr>
            """.format(alert['user_name'], alert['created_at'], alert['id'], alert['text'], alert['hashtags'],
                       alert['user_mentions'])

        table = table + table_body + """</table>"""

        style = """
        <style>
            table {font-family: arial, sans-serif; border-collapse: collapse; width: 100%;}
            td, th {border: 1px solid #dddddd; text-align: left; padding: 8px;}                                      
        </style>        
        """

        message_body_html = """
            <html>
              <head>
                {}
              </head>
              <body>
                <h1>Seada Alerts</h1><br>                   
                {}
              </body>
            </html>
            """.format(style, table)

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(message_body_html, "html")
        part2 = MIMEText(message_body, "plain")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create a secure SSL context
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login("seada.alerts@gmail.com", password)
                # print(sender_email)
                # print(receiver_email)
                # print(message)
                mail_response = server.sendmail(sender_email, receiver_email, message.as_string())
                if len(mail_response) == 0:
                    send = True
        except smtplib.SMTPHeloError:
            logging.exception('[AlertHandler.send_email_message] The server didn’t reply properly to the '
                              'HELO greeting.')
        except smtplib.SMTPSenderRefused:
            logging.exception('[AlertHandler.send_email_message] The server didn’t accept the from_addr.')
        except Exception as exception:
            logging.exception('[AlertHandler.send_email_message] Exception at sendmail: {}'.format(exception))

        return send

    def send_alert(self, alert_config, alert_info):

        sended = [False, False, False]

        if "email" in alert_config.outputs:
            if self.send_email_message(alert_config=alert_config, alert_info=alert_info):
                print("[+] {} Email sended...".format(datetime.now()))
                logging.info('[alertHandler.send_alert] email send')
                sended[0] = True
            else:
                print("[+] Fail at send email ")

        if "telegram" in alert_config.outputs:
            s = SenderTelegramMessages(alert_config=alert_config)
            s.send_message_to_bot(alert_info)
            print("[+] {} Telegram message sent...".format(datetime.now()))

        if "alexa" in alert_config.outputs:
            # TODO: add config for send alerts to alexa
            print('[+] Command alexa yeah!')

        return sended

    def insert_database(self, alert_config, response_list):
        """
        Method for insert alert information into elasticsearch index.
        :param alert_config: information of alert.
        :param response_list: alert list
        :return: the result of insert information in elasticsearch
        """
        num_alert_registered = 0
        result = None
        path = 'seadaAlert/elastic/'
        try:
            result = self.es.create_index(index_name=self.es.twitter_alert_index_name,
                                          mapping_file=self.es.twitter_alert_mapping_file, debug=None, path=path)
            if result:
                print('[+] database index created')
                logging.info('[AlertHandler.insert_database] database index created')
            else:
                print('[+] {} database index not created'.format(datetime.now()))
                logging.info('[AlertHandler.insert_database] database index not created')

            for response in response_list:
                info = {
                    "id": response['id'],
                    "alert_name": alert_config.name,
                    "alert_type": alert_config.type,
                    "alert_terms": alert_config.terms_list,
                    "alert_outputs": alert_config.outputs,
                    "alert_content_id": response['id'],
                    "alert_content_username": response['user_name'],
                    "alert_content_text": response['text'],
                    "alert_content_created_at": response['created_at'],
                    "alert_content_hashtags": response['hashtags'],
                    "alert_content_user_mentions": response['user_mentions']
                }
                result = self.es.store_information_to_elasticsearch(index_name=self.es.twitter_alert_index_name,
                                                                    info=info, debug=None)
                if result:
                    num_alert_registered = num_alert_registered + 1
                    logging.info('[AlertHandler.insert_database] alert registered')
                else:
                    logging.info('[AlertHandler.insert_database] alert not registered')

            print('[+] {} Registered {}/{} alerts'.format(datetime.now(), num_alert_registered, len(response_list)))
            logging.info('[AlertHandler.insert_database] Registered {}/{} alerts'.format(num_alert_registered,
                                                                                         len(response_list)))

        except Exception as exception:
            result = None
            print('[+] Exception at insert in elasticsearch: {}'.format(exception))
            logging.error('[AlertHandler.register] Exception at insert in elasticsearch: {}'.format(exception))

        return result

    def start(self):
        """
        Main method of SEADA Alert tool.
        :return:
        """
        print('[+] SEADA Alert starting...')
        logging.info('[AlertHandler.start] SEADA Alert starting...')
        config = {}

        if self.config_dir:
            config = self.get_config()
        else:  # default values
            config['alerts_folder'] = '../data/alerts/'
            config['sleep_interval'] = 900

        if self.debug:
            print('[+] config: {}'.format(config))

        alerts = self.load_alerts(config['alerts_folder'])
        if len(alerts) < 1:
            print('[+] Not alerts loaded. Exit...')
            logging.info('[alertHandler.start] Not alerts loaded. Exit...')
            sys.exit(0)

        print('[+] Number of alerts loaded: {}'.format(len(alerts)))
        title_alerts = []
        for alert in alerts:
            title_alerts.append(alert.name)
        print('[+] {} Alert\'s tittles: {}'.format(datetime.now(), title_alerts))

        if self.debug:
            for alert in alerts:
                print('[+] Alert\'s config: {}'.format(alert))

        while True:
            for alert in alerts:
                try:
                    print('[+] {} Searching following terms in database: {}'.format(datetime.now(), alert.terms_list))
                    logging.info('[AlertHandler.start] Searching following terms in '
                                 'database: {}'.format(alert.terms_list))

                    response, items_response = self.search(alert)

                    if self.debug:
                        print('[+] {} Response: {} and len items: {}'.format(datetime.now(), response,
                                                                             len(items_response)))

                    if response:
                        print('[+] {} Founded one term. Sending alert to: {}'. format(datetime.now(), alert.emails))
                        logging.info('[AlertHandler.start] Founded one term. '
                                     'Sending alert to: {}'. format(alert.emails))

                        if self.send_alert(alert, items_response):
                            print('[+] {} Alerts sent. Inserting alert in database...'.format(datetime.now()))
                            logging.info('[AlertHandler] Alerts sent. Insert alert in database...')

                        if self.insert_database(alert_config=alert, response_list=items_response):
                            print('[+] {} Alert inserted in datebase...'.format(datetime.now()))
                            logging.info('[AlertHandler.start] Alerts sent. Insert alert in database...')

                except Exception as exception:
                    print('[+] {} Exception: {}'.format(datetime.now(), exception))
                    logging.error('[AlertHandler.start] While exception: {}'.format(exception))

            print('[+] {} Waiting for {} secs...'.format(datetime.now(), config['sleep_interval']))
            logging.info('[AlertHandler] Waiting for {0} secs...'.format(config['sleep_interval']))
            time.sleep(config['sleep_interval'])
