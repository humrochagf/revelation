# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
from unittest import TestCase

from revelation import Revelation


class RevelationTestCase(TestCase):
    def setUp(self):
        self.tests_folder = tempfile.mkdtemp()
        self.media = tempfile.mkdtemp(dir=self.tests_folder)
        _, self.slide = tempfile.mkstemp(".md", dir=self.tests_folder)

        with open(self.slide, "w") as file:
            file = file.write("# Pag1\n---\n# Pag2")

        self.app = Revelation(self.slide, media=self.media)

    def tearDown(self):
        shutil.rmtree(self.tests_folder)

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
