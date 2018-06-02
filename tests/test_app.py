# -*- coding: utf-8 -*-

import os
import tempfile
import unittest

from revelation import Revelation


class RevelationTestCase(unittest.TestCase):

    def setUp(self):
        self.media = tempfile.mkdtemp()
        _, self.slide = tempfile.mkstemp(".md")

        with open(self.slide, "w") as file:
            file = file.write("# Pag1\n---\n# Pag2")

        self.app = Revelation(self.slide, media=self.media)

    def test_parse_shared_data_empty(self):
        shared_data_config = self.app.parse_shared_data(None)

        self.assertDictEqual(shared_data_config, {})

    def test_parse_shared_data(self):
        shared_data_config = self.app.parse_shared_data(self.media)

        self.assertDictEqual(
            shared_data_config,
            {"/{}".format(os.path.basename(self.media)): self.media},
        )

    def test_load_slides(self):
        slides = self.app.load_slides(self.slide, "---")

        self.assertListEqual(slides, ["# Pag1\n", "\n# Pag2"])
