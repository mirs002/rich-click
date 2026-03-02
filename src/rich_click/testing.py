from __future__ import annotations

from contextlib import contextmanager
from typing import IO, Any, Iterator, Mapping

from click.testing import CliRunner


class RichCliRunner(CliRunner):
    """
    CliRunner that rebinds Rich's global console during isolation.

    Rich caches a process-global console instance. If that console is created
    before Click's ``CliRunner`` swaps ``sys.stdin`` / ``sys.stdout`` / ``sys.stderr``,
    Rich prompts and prints will keep writing to the original streams.

    This subclass temporarily points Rich's global console at Click's isolated
    streams so tests can assert on Rich output (including prompt rendering).
    """

    @contextmanager
    def isolation(
        self,
        input: str | bytes | IO[Any] | None = None,
        env: Mapping[str, str | None] | None = None,
        color: bool = False,
    ) -> Iterator[Any]:
        import sys

        import rich
        from rich.console import Console

        old_console = getattr(rich, "_console", None)

        with super().isolation(input=input, env=env, color=color) as streams:
            setattr(rich, "_console", Console(file=sys.stdout, force_terminal=color))
            try:
                yield streams
            finally:
                setattr(rich, "_console", old_console)
