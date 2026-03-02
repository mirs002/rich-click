import io

import click
import rich
from click.testing import CliRunner
from rich.console import Console
from rich.prompt import Prompt

from rich_click.testing import RichCliRunner


@click.command()
def cli() -> None:
    name = Prompt.ask("Name")
    click.echo(f"Hello {name}")


def test_rich_cli_runner_captures_prompt_when_global_console_is_customized() -> None:
    # Simulate application startup code that configured a global Rich console.
    rich._console = Console(file=io.StringIO())  # type: ignore[attr-defined]

    runner = RichCliRunner()
    result = runner.invoke(cli, input="Jane\n")

    assert result.exit_code == 0
    assert "Name" in result.output
    assert "Hello Jane" in result.output


def test_click_cli_runner_does_not_capture_prompt_when_global_console_is_customized() -> None:
    rich._console = Console(file=io.StringIO())  # type: ignore[attr-defined]

    runner = CliRunner()
    result = runner.invoke(cli, input="Jane\n")

    assert result.exit_code == 0
    assert "Hello Jane" in result.output
    assert "Name" not in result.output
