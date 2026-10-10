import sys

if __name__ == '__main__':
    if '--tests' in sys.argv:
        import pytest

        sys.argv.remove('--tests')
        raise SystemExit(pytest.main(['-v', 'testcases/', *sys.argv[1:]]))

    # 默认读取当前 MuMu 前台打开的《世界启元》战报。
    from run_battle_report import main

    main()
