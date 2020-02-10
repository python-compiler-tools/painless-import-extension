import unittest


class Main(unittest.TestCase):
    def test_positive(self):
        from tests import test_json
        from tests import some_yaml

    def test_negative(self):
        def f():
            from tests import no_yaml

        self.assertRaises(FileNotFoundError, f)


if __name__ == '__main__':
    unittest.main()
