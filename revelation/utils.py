"""Utility tools used by revelation"""

import os
import shutil
import tarfile
import zipfile
from http.client import HTTPMessage
from pathlib import Path
from urllib.request import urlretrieve

from revelation import default_config


def make_presentation(presentation_path: Path) -> None:
    """
    Make a new presentation boilerplate code given a presentation_path
    """
    name = presentation_path.name

    (presentation_path / "media").mkdir(parents=True)

    shutil.copy(default_config.__file__, presentation_path / "config.py")

    with (presentation_path / "slides.md").open("w") as fp:
        title = name.replace("_", " ").replace("-", " ").title()

        fp.write(f"# {title}\n\nStart from here!")


def download_file(url: str) -> tuple[Path, HTTPMessage]:
    """
    Download a file from a given url
    """
    downloaded_file, result = urlretrieve(url)

    return Path(downloaded_file), result


def move_and_replace(src: Path, dst: Path) -> None:
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
        # keep the dir structure by replacing the source root to
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


def extract_file(compressed_file: Path, path: Path = Path(".")) -> Path:
    """Extract function to extract from zip or tar file"""
    path = path.resolve()

    if compressed_file.is_file():
        if tarfile.is_tarfile(str(compressed_file)):
            with tarfile.open(compressed_file, "r:gz") as tfile:
                basename = tfile.getnames()[0]

                def is_within_directory(directory, target):
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)

                    prefix = os.path.commonprefix([abs_directory, abs_target])

                    return prefix == abs_directory

                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)

                        if not is_within_directory(path, member_path):
                            msg = "Attempted Path Traversal in Tar File"
                            raise Exception(msg)

                    tar.extractall(path, members, numeric_owner=numeric_owner)

                safe_extract(tfile, str(path.resolve()))
        elif zipfile.is_zipfile(compressed_file):
            with zipfile.ZipFile(compressed_file, "r") as zfile:
                basename = zfile.namelist()[0]
                zfile.extractall(path)
        else:
            msg = "File type not supported"
            raise NotImplementedError(msg)
    else:
        msg = f"{compressed_file} is not a valid file"
        raise FileNotFoundError(msg)

    return path / basename


def normalize_newlines(text: str) -> str:
    """Normalize text to follow Unix newline pattern"""
    return text.replace("\r\n", "\n").replace("\r", "\n")
