# -*- coding: utf-8 -*-

import tempfile
import unittest

from revelation.config import Config


class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        _, config_file = tempfile.mkstemp('.py')

        with open(config_file, 'w') as file:
            file.write(
                'REVEAL_META = {\n'
                '"title": "Test Title",\n'
                '"author": "Test Author",\n'
                '"description": "Test description",\n'
                '}'
            )

        self.config = Config(config_file)

    def test_config_extends_dict(self):
        self.assertIsInstance(self.config, dict)

    def test_config_initialize_variables(self):
        self.assertIn('REVEAL_META', self.config)
        self.assertIn('REVEAL_SLIDE_SEPARATOR', self.config)
        self.assertIn('REVEAL_THEME', self.config)
        self.assertIn('REVEAL_CONFIG', self.config)

    def test_config_custom_values(self):
        self.assertDictEqual(
            self.config['REVEAL_META'],
            {
                'title': 'Test Title',
                'author': 'Test Author',
                'description': 'Test description',
            }
        )
