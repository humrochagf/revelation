# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
from unittest import TestCase

from click.testing import CliRunner

from revelation import cli

try:
    # python 3
    from unittest.mock import patch
except ImportError:
    # legacy python
    from mock import patch


class CliTestCase(TestCase):
    def setUp(self):
        self.tests_folder = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tests_folder)

    def test_mkpresentation(self):
        presentation_folder = os.path.join(
            self.tests_folder, "test_mkpresentation"
        )
        presentation_file = os.path.join(presentation_folder, "slides.md")
        media_folder = os.path.join(presentation_folder, "media")
        config_file = os.path.join(presentation_folder, "config.py")

        runner = CliRunner()
        result = runner.invoke(cli.mkpresentation, [presentation_folder])

        self.assertEqual(result.exit_code, 0)
        self.assertTrue(os.path.isdir(presentation_folder))
        self.assertTrue(os.path.isfile(presentation_file))
        self.assertTrue(os.path.isdir(media_folder))
        self.assertTrue(os.path.isfile(config_file))

    def test_mkpresentation_already_exists(self):
        presentation = tempfile.mkdtemp(dir=self.tests_folder)

        runner = CliRunner()
        result = runner.invoke(cli.mkpresentation, [presentation])

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(
            result.output,
            "Error: '{}' already exists.\n".format(
                os.path.abspath(presentation)
            ),
        )

    def test_mkstatic(self):
        base_folder = tempfile.mkdtemp(dir=self.tests_folder)
        _, presentation_file = tempfile.mkstemp(
            ".md", "slides", base_folder, "# Test\n"
        )
        output_folder = os.path.join(base_folder, "output")
        index_file = os.path.join(output_folder, "index.html")
        static_folder = os.path.join(output_folder, "static")

        runner = CliRunner()
        result = runner.invoke(
            cli.mkstatic, [presentation_file, "-o", output_folder]
        )

        self.assertEqual(result.exit_code, 0)
        self.assertTrue(os.path.isdir(output_folder))
        self.assertTrue(os.path.isfile(index_file))
        self.assertTrue(os.path.isdir(static_folder))

    def test_mkstatic_output_already_exists_file(self):
        base_folder = tempfile.mkdtemp(dir=self.tests_folder)
        _, presentation_file = tempfile.mkstemp(
            ".md", "slides", base_folder, "# Test\n"
        )
        _, output = tempfile.mkstemp(dir=base_folder)

        runner = CliRunner()
        result = runner.invoke(cli.mkstatic, [presentation_file, "-o", output])

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(
            result.output,
            "Error: '{}' already exists and is a file.\n".format(
                os.path.abspath(output)
            ),
        )

    def test_mkstatic_output_already_exists_folder(self):
        base_folder = tempfile.mkdtemp(dir=self.tests_folder)
        _, presentation_file = tempfile.mkstemp(
            ".md", "slides", base_folder, "# Test\n"
        )
        output = tempfile.mkdtemp(dir=base_folder)

        runner = CliRunner()
        result = runner.invoke(cli.mkstatic, [presentation_file, "-o", output])

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(
            result.output,
            "Error: '{}' already exists, use --force to override it.\n".format(
                os.path.abspath(output)
            ),
        )

    def test_mkstatic_presentation_not_found(self):
        base_folder = tempfile.mkdtemp(dir=self.tests_folder)
        presentation = os.path.join(base_folder, "notfound")

        runner = CliRunner()
        result = runner.invoke(cli.mkstatic, [presentation])

        self.assertEqual(result.exit_code, 1)
        self.assertEqual(
            result.output, "Error: Presentation file not found.\n"
        )

    @patch("revelation.cli.WebSocketServer")
    def test_start(self, websocketserver_patch):
        base_folder = tempfile.mkdtemp(dir=self.tests_folder)
        _, presentation_file = tempfile.mkstemp(
            ".md", "slides", base_folder, "# Test\n"
        )

        runner = CliRunner()
        runner.invoke(cli.start, [presentation_file])

        self.assertTrue(websocketserver_patch.called)
