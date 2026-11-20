#!/usr/bin/python3
"""Program entry point: start with `python .` or `python __main__.py`.

Owner: Ali Canli
"""

from cli import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Ctrl+C: quit quietly, without a traceback.
        raise SystemExit(130)
