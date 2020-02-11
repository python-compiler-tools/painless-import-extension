# this file is for CI only.
from sys import version_info

# https://github.com/pypa/pip/issues/7498
try:
    from pip._internal.main import main
    if not callable(main):
        raise ImportError

except ImportError:
    try:
        from pip._internal import main
        if not callable(main):
            raise ImportError

    except ImportError:
        from pip import main

        if not callable(main):
            raise ImportError

requires = []
if (3, 4) <= version_info < (3, 5):
    pass
else:
    requires = ['PyYAML']

if __name__ == '__main__':
    for package in requires:
        main(['install', package])
