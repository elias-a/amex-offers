import os
from unittest import TestCase
from unittest.mock import Mock
from amex_interface import AmexInterface
from .data import CODE


class Test_parse_email(TestCase):
    def setUp(self):
        driver = Mock()
        self.amex_interface = AmexInterface(driver)

    def test_parse_email(self):
        path = os.path.join(os.path.dirname(__file__), "data/email.html")
        with open(path, "rt") as f:
            message = f.read()
        code = self.amex_interface._parse_email(message)
        assert code == CODE
