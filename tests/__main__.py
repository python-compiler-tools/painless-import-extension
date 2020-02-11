import unittest


class Main(unittest.TestCase):
    def test_positive(self):
        from tests import test_json
        try:
            from tests import some_yaml
        except ImportError:
            pass

    def test_negative(self):
        def f():
            from tests import no_json

        self.assertRaises(FileNotFoundError, f)


if __name__ == '__main__':
    unittest.main()
