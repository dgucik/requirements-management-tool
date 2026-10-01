#!/usr/bin/env python
import os
import sys


def main():
    """Run Django's command-line management utility."""

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django is not installed. Run `uv sync` from the backend directory."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
