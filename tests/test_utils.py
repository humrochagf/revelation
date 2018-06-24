# -*- coding: utf-8 -*-

import os
import shutil
import tarfile
import tempfile
import unittest
import zipfile

from revelation.utils import extract_file, make_presentation, move_and_replace

try:
    # Python 3
    FileNotFoundError
except NameError:
    # Python 2
    FileNotFoundError = IOError


class HelpersTestCase(unittest.TestCase):
    def make_src(self, base):
        source = tempfile.mkdtemp(dir=base)
        file_to_replace_on_source = os.path.join(source, "replace.txt")
        fd, file_to_move = tempfile.mkstemp(".txt", dir=source)

        os.close(fd)

        tempfile.mkdtemp(dir=source)

        with open(file_to_replace_on_source, "w") as f_source:
            f_source.write("source")

        return source

    def make_dst(self, base):
        destination = tempfile.mkdtemp(dir=base)
        file_to_replace_on_dest = os.path.join(destination, "replace.txt")

        with open(file_to_replace_on_dest, "w") as f_dest:
            f_dest.write("dest")

        return destination

    def make_tar(self, content, base):
        fd, tar_file = tempfile.mkstemp(".tar.gz", dir=base)

        os.close(fd)

        with tarfile.open(tar_file, "w:gz") as t:
            t.add(content, arcname="tarfolder")

        return tar_file

    def make_zip(self, content, base):
        fd, zip_file = tempfile.mkstemp(".zip", dir=base)

        os.close(fd)

        with zipfile.ZipFile(zip_file, "w") as z:
            z.write(content, arcname="zipfolder")
            for item in os.listdir(content):
                z.write(
                    os.path.join(content, item),
                    arcname=os.path.join("zipfolder", item),
                )

        return zip_file

    def setUp(self):
        self.base = tempfile.mkdtemp()
        self.source = self.make_src(self.base)
        self.destination = self.make_dst(self.base)
        self.tar = self.make_tar(self.source, self.base)
        self.zip = self.make_zip(self.source, self.base)
        fd, self.somefile = tempfile.mkstemp(dir=self.base)

        os.close(fd)

    def tearDown(self):
        shutil.rmtree(self.base)

    def test_helper_move_and_replace(self):
        src_files = sorted(os.listdir(self.source))

        move_and_replace(self.source, self.destination)

        dst_files = sorted(os.listdir(self.destination))

        with open(os.path.join(self.destination, "replace.txt"), "r") as f:
            file_content = f.read()

        # The moved directory should not exist because it was moved
        self.assertFalse(os.path.exists(self.source))
        # The replaced file should contain the data from the source file
        self.assertEqual(file_content, "source")
        # The moved files from source should be equal to the
        # files on destination directory
        self.assertEqual(src_files, dst_files)

    def test_extract_file_tarfile(self):
        src_files = sorted(os.listdir(self.source))

        extracted = extract_file(self.tar, self.base)

        extracted_files = sorted(os.listdir(extracted))

        self.assertEqual(extracted_files, src_files)

    def test_extract_file_zipfile(self):
        src_files = sorted(os.listdir(self.source))

        extracted = extract_file(self.zip, self.base)

        extracted_files = sorted(os.listdir(extracted))

        self.assertEqual(extracted_files, src_files)

    def test_extract_file_on_non_file(self):
        self.assertRaises(FileNotFoundError, extract_file, self.base)

    def test_extract_file_on_non_tar_or_zip(self):
        self.assertRaises(NotImplementedError, extract_file, self.somefile)

    def test_make_presentation(self):
        path = os.path.join(tempfile.mkdtemp(), "test")
        media_path = os.path.join(path, "media")
        config_path = os.path.join(path, "config.py")
        presentation_path = os.path.join(path, "slides.md")

        make_presentation(path)

        self.assertTrue(os.path.isdir(path))
        self.assertTrue(os.path.isdir(media_path))
        self.assertTrue(os.path.isfile(config_path))
        self.assertTrue(os.path.isfile(presentation_path))
