# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
from unittest import TestCase

from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

from revelation import Revelation


class RevelationTestCase(TestCase):
    def setUp(self):
        self.tests_folder = tempfile.mkdtemp()
        self.media = tempfile.mkdtemp(dir=self.tests_folder)
        _, self.slide = tempfile.mkstemp(".md", dir=self.tests_folder)
        _, self.non_normalized_slide = tempfile.mkstemp(
            ".md", dir=self.tests_folder
        )
        _, self.non_ascii_slide = tempfile.mkstemp(
            ".md", dir=self.tests_folder
        )

        with open(self.slide, "w") as file:
            file = file.write("# Pag1\n---\n# Pag2.1\n---~\n# Page2.2")

        with open(self.non_normalized_slide, "w") as file:
            file = file.write("# Pag1\r---\r\n# Pag2")

        with open(self.non_ascii_slide, "w") as file:
            file = file.write("# こんにちは\n---\n# 乾杯")

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
        slides = self.app.load_slides(self.slide, "---", "---~")

        self.assertListEqual(
            slides, [["# Pag1\n"], ["\n# Pag2.1\n", "\n# Page2.2"]]
        )

    def test_load_slides_non_normalized(self):
        slides = self.app.load_slides(self.non_normalized_slide, "---", "---~")

        self.assertListEqual(slides, [["# Pag1\n"], ["\n# Pag2"]])

    def test_load_slides_non_ascii(self):
        slides = self.app.load_slides(self.non_ascii_slide, "---", "---~")

        self.assertListEqual(slides, [[u"# こんにちは\n"], [u"\n# 乾杯"]])

    def test_client_request_ok(self):
        client = Client(self.app, BaseResponse)
        response = client.get("/")
        self.assertEqual(response.status, "200 OK")
        self.assertEqual(response.headers.get("Content-Type"), "text/html")

    def test_client_with_reload(self):
        app = Revelation(self.slide, media=self.media, reloader=True)
        client = Client(app, BaseResponse)
        response = client.get("/")
        self.assertIn("reloader", response.data.decode("utf8"))

    def test_client_without_reload(self):
        app = Revelation(self.slide, media=self.media, reloader=False)
        client = Client(app, BaseResponse)
        response = client.get("/")
        self.assertNotIn("reloader", response.data.decode("utf8"))
