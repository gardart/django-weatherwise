#!/usr/bin/env python
import os
import sys
from pathlib import Path


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    sys.path.append(str(project_root))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weatherwise.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
