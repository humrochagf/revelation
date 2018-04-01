# -*- coding: utf-8 -*-

import unittest

from revelation.config import Config


class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.config = Config()

    def test_config_extends_dict(self):
        self.assertIsInstance(self.config, dict)

    def test_config_initialize_variables(self):
        self.assertIn('REVEAL_META', self.config)
        self.assertIn('REVEAL_SLIDE_SEPARATOR', self.config)
        self.assertIn('REVEAL_CONFIG', self.config)
