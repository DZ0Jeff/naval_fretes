import logging
import unittest
from src.webdriver import get_token
from scrapper_boilerplate.setup import init_log


class TestBearerGet(unittest.TestCase):
    def setUp(self) -> None:
        init_log()

    def test_token(self):
        bearer_token = get_token()
        logging.info(bearer_token)
        logging.info(len(bearer_token))
        self.assertTrue(bearer_token)


if __name__ == "__main__":
    unittest.main()
