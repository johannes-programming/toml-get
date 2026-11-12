from __future__ import annotations

__all__: list[str] = ["main", "test"]

import sys
import unittest


def main() -> int:
    return int(not test().wasSuccessful())


def test() -> unittest.TextTestResult:
    loader: unittest.TestLoader
    runner: unittest.TextTestRunner
    suite: unittest.TestSuite
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    sys.exit(main())
