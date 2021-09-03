from werkzeug.test import Client
from werkzeug.wrappers import Response

from revelation import Revelation

from .conftest import Presentation


def test_parse_shared_data_empty(revelation: Revelation):
    shared_data_config = revelation.parse_shared_data(None)

    assert shared_data_config == {}


def test_parse_shared_data(presentation: Presentation, revelation: Revelation):
    shared_data_config = revelation.parse_shared_data(presentation.media)

    assert shared_data_config == {
        f"/{presentation.media.name}": str(presentation.media)
    }


def test_load_slides(presentation: Presentation, revelation: Revelation):
    presentation.file.write_text(
        "# Pag1\n---\n# Pag2.1\n---~\n# Page2.2", "utf8"
    )

    slides = revelation.load_slides(presentation.file, "---", "---~")

    assert slides == [["# Pag1\n"], ["\n# Pag2.1\n", "\n# Page2.2"]]


def test_load_slides_non_normalized(
    presentation: Presentation, revelation: Revelation
):
    presentation.file.write_text("# Pag1\r---\r\n# Pag2", "utf8")

    slides = revelation.load_slides(presentation.file, "---", "---~")

    assert slides == [["# Pag1\n"], ["\n# Pag2"]]


def test_load_slides_non_ascii(
    presentation: Presentation, revelation: Revelation
):
    presentation.file.write_text("# こんにちは\n---\n# 乾杯", "utf8")

    slides = revelation.load_slides(presentation.file, "---", "---~")

    assert slides == [["# こんにちは\n"], ["\n# 乾杯"]]


def test_client_request_ok(revelation: Revelation):
    client = Client(revelation, Response)

    response = client.get("/")

    assert response.status == "200 OK"
    assert response.headers.get("Content-Type") == "text/html"
