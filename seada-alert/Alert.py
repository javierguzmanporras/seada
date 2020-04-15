class Alert:

    def __init__(self, alert_info):

        # print(type(alert_info['name']))
        # print(alert_info['name'])

        self.name = alert_info['name']
        self.type = alert_info['type']
        self.index = alert_info['index']
        self.list = alert_info['list']
        self.outputs = alert_info['outputs']
        self.emails = alert_info['emails']
        self.telegram = alert_info['telegram']
        self.alert_info = alert_info

    def __str__(self):
        return str(self.alert_info)
