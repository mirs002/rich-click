from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator, Mapping, Optional, TextIO, Tuple, Union

from click.testing import CliRunner


class RichCliRunner(CliRunner):
    """CliRunner that rebinds Rich's global console during isolation.

    Rich caches a process-global console instance. If that console is created
    before Click's ``CliRunner`` swaps ``sys.stdin`` / ``sys.stdout`` / ``sys.stderr``,
    Rich prompts and prints will keep writing to the original streams.

    This subclass temporarily points Rich's global console at Click's isolated
    streams so tests can assert on Rich output (including prompt rendering).
    """

    @contextmanager
    def isolation(  # type: ignore[override]
        self,
        input: Union[str, bytes, TextIO, None] = None,
        env: Optional[Mapping[str, Optional[str]]] = None,
        color: bool = False,
    ) -> Iterator[Tuple[object, object, object]]:
        import sys

        import rich
        from rich.console import Console

        old_console = rich._console  # type: ignore[attr-defined]

        with super().isolation(input=input, env=env, color=color) as streams:
            rich._console = Console(file=sys.stdout, force_terminal=color)  # type: ignore[attr-defined]
            try:
                yield streams
            finally:
                rich._console = old_console  # type: ignore[attr-defined]
