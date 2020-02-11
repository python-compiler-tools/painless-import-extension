from sys import version_info
try:
    from pip import main
except ImportError:
    from pip._internal import main

requires = []
if (3, 4) <= version_info < (3, 5):
    pass
else:
    requires = ['PyYAML']

if __name__ == '__main__':
    for package in requires:
        main(['install', package])
