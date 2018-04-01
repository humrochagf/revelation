# -*- coding: utf-8 -*-

import os
import tempfile
import unittest

from revelation import Revelation


class RevelationTestCase(unittest.TestCase):

    def setUp(self):
        self.media = tempfile.mkdtemp()
        _, self.slide = tempfile.mkstemp('.md')

        with open(self.slide, 'w') as file:
            file = file.write('# Teste')

        self.app = Revelation(self.slide, self.media)

    def test_parse_media_root_empty(self):
        media_config = self.app.parse_media_root(None)

        self.assertDictEqual(media_config, {})

    def test_parse_media_root(self):
        media_config = self.app.parse_media_root(self.media)

        self.assertDictEqual(
            media_config,
            {'/{}'.format(os.path.basename(self.media)): self.media}
        )
