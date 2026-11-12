from __future__ import annotations

__all__: list[str] = ["main", "run"]

import sys

from toml_get.core import main, run

if __name__ == "__main__":
    sys.exit(main())
