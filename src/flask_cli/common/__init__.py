"""
Imports click or rich_click depending on env settings.
Rich click increases import times, and it might be desirable to disable it (e.g. when
running automated jobs).
"""

import os

_disable_rich_cli = os.environ.get("RICH_CLI", "").lower() in {
    "0",
    "false"
}
if _disable_rich_cli:
    import click
else:
    import rich_click as click

__all__ = ["click"]
