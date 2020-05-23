import unittest
from seada.seadaAlert.alertHandler import AlertHandler


class SeadaAlertTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_config(self):
        """Test for get config from yaml file"""
        pass
        config_expect = {'alerts_folder': 'alerts', 'sleep_interval': 60, 'es_host': 'localhost', 'es_port': 9200}
        ah = AlertHandler(config_dir='test_config.yml', es_connection=None)
        config = ah.get_config()
        self.assertDictEqual(config, config_expect)


if __name__ == '__main__':
    unittest.main()

