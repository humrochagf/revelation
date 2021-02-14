"""Utility tools used by revelation"""

import os
import shutil
import tarfile
import zipfile
from http.client import HTTPMessage
from pathlib import Path
from typing import Tuple
from urllib.request import urlretrieve

from . import default_config


def make_presentation(presentation_path: Path):
    """
    Make a new presentation boilerplate code given a presentation_path
    """
    name = presentation_path.name

    (presentation_path / "media").mkdir(parents=True)

    shutil.copy(default_config.__file__, presentation_path / "config.py")

    with (presentation_path / "slides.md").open("w") as fp:
        title = name.replace("_", " ").replace("-", " ").title()

        fp.write(f"# {title}\n\nStart from here!")


def download_file(url: str) -> Tuple[Path, HTTPMessage]:
    """
    Download a file from a given url
    """
    downloaded_file, result = urlretrieve(url)

    return Path(downloaded_file), result


def move_and_replace(src: Path, dst: Path):
    """
    Helper function used to move files from one place to another,
    creating os replacing them if needed

    :param src: source directory
    :param dst: destination directory
    """

    src = src.resolve()
    dst = dst.resolve()

    for src_dir, _, files in os.walk(src):
        # using os walk to navigate through the directory tree
        # keep te dir structure by replacing the source root to
        # the destination on walked path
        dst_dir = src_dir.replace(str(src), str(dst))

        if not os.path.exists(dst_dir):
            # to prevent copy from failing, create the not existing dirs
            os.makedirs(dst_dir)

        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)

            if os.path.exists(dst_file):
                os.remove(dst_file)  # to copy not fail, create existing files

            shutil.move(src_file, dst_dir)  # move the files

    shutil.rmtree(src)  # remove the dir structure from the source


def extract_file(compressed_file, path="."):
    """Extract function to extract from zip or tar file"""
    if os.path.isfile(compressed_file):
        if tarfile.is_tarfile(compressed_file):
            with tarfile.open(compressed_file, "r:gz") as tfile:
                basename = tfile.members[0].name
                tfile.extractall(path + "/")
        elif zipfile.is_zipfile(compressed_file):
            with zipfile.ZipFile(compressed_file, "r") as zfile:
                basename = zfile.namelist()[0]
                zfile.extractall(path)
        else:
            raise NotImplementedError("File type not supported")
    else:
        raise FileNotFoundError(f"{compressed_file} is not a valid file")

    return os.path.abspath(os.path.join(path, basename))


def normalize_newlines(text):
    """Normalize text to follow Unix newline pattern"""
    return text.replace("\r\n", "\n").replace("\r", "\n")
