import tarfile
import zipfile
from dataclasses import dataclass
from pathlib import Path

import pytest

from revelation import Revelation


@dataclass
class Presentation:

    parent: Path

    @property
    def root(self):
        return self.parent / "presentation"

    @property
    def file(self):
        return self.root / "slides.md"

    @property
    def config(self):
        return self.root / "config.py"

    @property
    def media(self):
        return self.root / "media"


@pytest.fixture
def presentation(tmp_path: Path) -> Presentation:
    presentation = Presentation(tmp_path)

    presentation.root.mkdir()
    presentation.media.mkdir()
    presentation.file.write_text("# Test", "utf8")

    reveal_meta = {
        "title": "Test Title",
        "author": "Test Author",
        "description": "Test description",
    }

    presentation.config.write_text(f"REVEAL_META = {reveal_meta}", "utf8")

    return presentation


@pytest.fixture
def presentation_zip(presentation: Presentation) -> Path:
    presentation_zip = presentation.parent / "presentation.zip"

    with zipfile.ZipFile(presentation_zip, "w") as fp:
        arcname = Path("presentation_zip")
        fp.write(presentation.root, arcname)

        for file in presentation.root.iterdir():
            fp.write(file, arcname / file.name)

    return presentation_zip


@pytest.fixture
def presentation_tar(presentation: Presentation) -> Path:
    presentation_tar = presentation.parent / "presentation.tar.gz"

    with tarfile.open(presentation_tar, "w:gz") as fp:
        arcname = Path("presentation_tar")
        fp.add(presentation.root, arcname)

    return presentation_tar


@pytest.fixture
def revelation(presentation: Presentation) -> Revelation:
    return Revelation(presentation.file, media=presentation.media)
