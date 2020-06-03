class Alert:

    def __init__(self, alert_info):
        self.name = alert_info['name']
        self.type = alert_info['type']
        self.index = alert_info['index']
        self.terms_list = alert_info['list']
        self.interval_time = alert_info['sleep_interval']
        self.outputs = alert_info['outputs']
        self.emails = alert_info['emails']
        self.email = alert_info['email']
        self.telegram = alert_info['telegram']

        try:
            self.operator = alert_info['operator']
        except KeyError:
            self.operator = 'or'

        self.alert_info = alert_info

    def __str__(self):
        return str(self.alert_info)
