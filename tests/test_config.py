# -*- coding: utf-8 -*-

import unittest

from revelation.config import Config


class ConfigTestCase(unittest.TestCase):

    def test_config_extends_dict(self):
        config = Config()

        self.assertIsInstance(config, dict)

    def test_config_initialize_variables(self):
        config = Config()

        self.assertIn('REVEAL_META', config)
        self.assertIn('REVEAL_SLIDE_SEPARATOR', config)
        self.assertIn('REVEAL_CONFIG', config)
