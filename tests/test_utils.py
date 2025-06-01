from pathlib import Path

import pytest

from revelation.utils import extract_file, make_presentation, move_and_replace

from .conftest import Presentation


def test_helper_move_and_replace(presentation: Presentation) -> None:
    dst_dir = presentation.parent / "destination"
    dst_dir.mkdir()

    dst_file = dst_dir / "slides.md"
    dst_file.write_text("replace", "utf8")

    src_files = sorted(f.name for f in presentation.root.iterdir())

    move_and_replace(presentation.root, dst_dir)

    dst_files = sorted(f.name for f in dst_dir.iterdir())

    # The moved directory should not exist because it was moved
    assert not presentation.root.exists()
    # The replaced file should contain the data from the source file
    assert dst_file.read_text("utf8") == "# Test"
    # The moved files from source should be equal to the
    # files on destination directory
    assert src_files == dst_files


def test_extract_file_zipfile(
    presentation: Presentation,
    presentation_zip: Path,
) -> None:
    src_files = sorted(f.name for f in presentation.root.iterdir())

    extracted_dir = Path(extract_file(presentation_zip, presentation.parent))

    extracted_files = sorted(f.name for f in extracted_dir.iterdir())

    assert extracted_files == src_files


def test_extract_file_tarfile(
    presentation: Presentation,
    presentation_tar: Path,
) -> None:
    src_files = sorted(f.name for f in presentation.root.iterdir())

    extracted_dir = Path(extract_file(presentation_tar, presentation.parent))

    extracted_files = sorted(f.name for f in extracted_dir.iterdir())

    assert extracted_files == src_files


def test_extract_file_on_non_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        extract_file(tmp_path / "notfound", tmp_path)


def test_extract_file_on_non_tar_or_zip(tmp_path: Path) -> None:
    wrong_format = tmp_path / "file.wrong"
    wrong_format.write_text("", "utf8")

    with pytest.raises(NotImplementedError):
        extract_file(wrong_format, tmp_path)


def test_make_presentation(tmp_path: Path) -> None:
    presentation = Presentation(tmp_path)

    make_presentation(presentation.root)

    assert presentation.root.is_dir()
    assert presentation.file.is_file()
    assert presentation.media.is_dir()
    assert presentation.config.is_file()
