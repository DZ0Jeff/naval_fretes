import unittest
from main import get_location


class TestLocation(unittest.TestCase):
    def test_location(self):
        data = get_location('santos')
        self.assertTrue(data)


if __name__ == "__main__":
    unittest.main()
