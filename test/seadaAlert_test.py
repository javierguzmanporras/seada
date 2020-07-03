import unittest
from seada.seadaAlert.alertHandler import AlertHandler
from seada.seadaAlert.alert import Alert


class SeadaAlertTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_config(self):
        """Test for get config from yaml file"""
        config_expect = {'alerts_folder': 'alerts', 'sleep_interval': 60, 'es_host': 'localhost', 'es_port': 9200}
        ah = AlertHandler(config_dir='test_config.yml', es_connection=None)
        config = ah.get_config()
        self.assertDictEqual(config, config_expect)

    def test_load_alerts(self):
        """Test for load alerts from yaml file"""

        info = {
            'name': 'Example term alert',
            'type': 'term',
            'index': 'twitter_tweets',
            'terms_list':  ['CiberCOVID19'],
            'outputs': ['email', 'telegram'],
            'emails': ['seadaAlert@example.com'],
            'telegram': [
                {'username': 'username'},
                {'token': 'token'},
                {'chatid': 'chatid'}
            ]
        }

        alert_expect = Alert(info)
        ah = AlertHandler("", "")
        alerts = ah.load_alerts("alerts")
        self.assertEqual(str(alerts[0]), str(alert_expect))


if __name__ == '__main__':
    unittest.main()

