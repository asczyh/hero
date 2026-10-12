"""Run the project's pytest test cases."""

import sys

import pytest


def main() -> int:
    """Run all test cases under testcases/, forwarding extra pytest options."""
    return pytest.main(['-v', 'testcases/', *sys.argv[1:]])


if __name__ == '__main__':
    raise SystemExit(main())
