"""运行项目中的 pytest 测试用例。"""

import sys

import pytest


def main() -> int:
    """运行 testcases/ 下的全部用例，并转发额外的 pytest 参数。"""
    return pytest.main(['-v', 'testcases/', *sys.argv[1:]])


if __name__ == '__main__':
    raise SystemExit(main())
