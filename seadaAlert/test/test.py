import unittest

from seadaAlert import get_config


class TestSEADA(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_config(self):
        """Test for get config from yaml file"""
        config_expect = {'alerts_folder': 'alerts', 'sleep_interval': 60, 'es_host': 'localhost', 'es_port': 9200}
        config = get_config('test/test_config.yml')
        self.assertDictEqual(config, config_expect)


if __name__ == '__main__':
    unittest.main()
