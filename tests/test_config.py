from revelation.config import Config

from .conftest import Presentation


def test_config_extends_dict(presentation: Presentation):
    config = Config(presentation.config)

    assert isinstance(config, dict)


def test_config_initialize_variables(presentation: Presentation):
    config = Config(presentation.config)

    assert "REVEAL_META" in config
    assert "REVEAL_SLIDE_SEPARATOR" in config
    assert "REVEAL_THEME" in config
    assert "REVEAL_CONFIG" in config


def test_config_custom_values(presentation: Presentation):
    config = Config(presentation.config)
    meta = {
        "title": "Test Title",
        "author": "Test Author",
        "description": "Test description",
    }

    assert config["REVEAL_META"] == meta
