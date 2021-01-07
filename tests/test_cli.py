from pathlib import Path

from pytest_mock import MockerFixture
from typer.testing import CliRunner

from revelation.cli import cli

from .conftest import Presentation


def test_mkpresentation(tmp_path: Path):
    presentation = Presentation(tmp_path)

    runner = CliRunner()
    result = runner.invoke(cli, ["mkpresentation", str(presentation.root)])

    assert result.exit_code == 0
    assert presentation.root.is_dir()
    assert presentation.file.is_file()
    assert presentation.media.is_dir()
    assert presentation.config.is_file()


def test_mkpresentation_already_exists(presentation: Presentation):
    runner = CliRunner()
    result = runner.invoke(cli, ["mkpresentation", str(presentation.root)])

    assert result.exit_code == 1
    assert result.output == (
        f"Error: '{presentation.root}' already exists.\nAborted!\n"
    )


def test_mkstatic(presentation: Presentation):
    output_dir = presentation.parent / "output"
    index_file = output_dir / "index.html"
    static_dir = output_dir / "static"

    runner = CliRunner()
    result = runner.invoke(
        cli, ["mkstatic", str(presentation.file), "-o", str(output_dir)]
    )

    assert result.exit_code == 0
    assert output_dir.is_dir()
    assert index_file.is_file()
    assert static_dir.is_dir()


def test_mkstatic_override_styles(presentation: Presentation):
    style_file = presentation.root / "style.css"
    style_file.write_text("h1 { color: #000 }", "utf8")

    output_dir = presentation.parent / "output"
    output_style_file = output_dir / "style.css"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "mkstatic",
            str(presentation.file),
            "-o",
            str(output_dir),
            "-s",
            str(style_file),
        ],
    )

    assert result.exit_code == 0
    assert output_style_file.is_file()


def test_mkstatic_output_already_exists_file(presentation: Presentation):
    output_file = presentation.parent / "output"
    output_file.write_text("", "utf8")

    runner = CliRunner()
    result = runner.invoke(
        cli, ["mkstatic", str(presentation.file), "-o", str(output_file)]
    )

    assert result.exit_code == 1
    assert result.output == (
        f"Error: '{output_file}' already exists and is a file.\nAborted!\n"
    )


def test_mkstatic_output_already_exists_folder(presentation: Presentation):
    output_dir = presentation.parent / "output"
    output_dir.mkdir()

    runner = CliRunner()
    result = runner.invoke(
        cli, ["mkstatic", str(presentation.file), "-o", str(output_dir)]
    )

    assert result.exit_code == 1
    assert result.output == (
        f"Error: '{output_dir}' already exists, use --force to override it.\n"
        "Aborted!\n"
    )


def test_mkstatic_presentation_not_found(tmp_path: Path):
    presentation = tmp_path / "notfound"

    runner = CliRunner()
    result = runner.invoke(cli, ["mkstatic", str(presentation)])

    assert result.exit_code == 1
    assert result.output == "Error: Presentation file not found.\nAborted!\n"


def test_mkstatic_style_not_file(presentation: Presentation):
    style_dir = presentation.root / "style.css"
    style_dir.mkdir()

    runner = CliRunner()
    result = runner.invoke(
        cli, ["mkstatic", str(presentation.file), "-s", str(style_dir)]
    )

    assert result.exit_code == 1
    assert result.output == (
        "Error: Style is not a css file or does not exists.\nAborted!\n"
    )


def test_mkstatic_style_not_css(presentation: Presentation):
    style_file = presentation.root / "style.notcss"
    style_file.write_text("", "utf8")

    runner = CliRunner()
    result = runner.invoke(
        cli, ["mkstatic", str(presentation.file), "-s", str(style_file)]
    )

    assert result.exit_code == 1
    assert result.output == (
        "Error: Style is not a css file or does not exists.\nAborted!\n"
    )


def test_start(mocker: MockerFixture, presentation: Presentation):
    mocked_run_simple = mocker.patch("revelation.cli.run_simple")

    runner = CliRunner()
    runner.invoke(cli, ["start", str(presentation.file)])

    assert mocked_run_simple.called


def test_start_presentation_not_found(tmp_path: Path):
    presentation = tmp_path / "notfound"

    runner = CliRunner()
    result = runner.invoke(cli, ["start", str(presentation)])

    assert result.exit_code == 1
    assert result.output == "Error: Presentation file not found.\nAborted!\n"


def test_start_style_not_file(presentation: Presentation):
    style_dir = presentation.root / "style.css"
    style_dir.mkdir()

    runner = CliRunner()
    result = runner.invoke(
        cli, ["start", str(presentation.file), "-s", str(style_dir)]
    )

    assert result.exit_code == 1
    assert result.output == (
        "Error: Style is not a css file or does not exists.\nAborted!\n"
    )


def test_start_style_not_css(presentation: Presentation):
    style_file = presentation.root / "style.notcss"
    style_file.write_text("", "utf8")

    runner = CliRunner()
    result = runner.invoke(
        cli, ["start", str(presentation.file), "-s", str(style_file)]
    )

    assert result.exit_code == 1
    assert result.output == (
        "Error: Style is not a css file or does not exists.\nAborted!\n"
    )
