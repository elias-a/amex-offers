import os
from unittest import TestCase
from bs4 import BeautifulSoup
from .data import CODE


class Test_parse_email(TestCase):
    def test_parse_email(self):
        path = os.path.join(os.path.dirname(__file__), "data/email.html")
        with open(path, "rt") as f:
            message = f.read()
        soup = BeautifulSoup(message, "html.parser")
        previous_sibling = soup.find("tr", text="Your Re-authentication Key:")
        code = previous_sibling.find_next_sibling().text
        assert code == CODE
