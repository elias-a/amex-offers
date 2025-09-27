from pathlib import Path
from amex_offers import AmexInterface


def test__parse_email(tmp_path):
    email = (Path(__file__).parent / "data" / "email.html").read_text()
    code = (Path(__file__).parent / "data" / "code.txt").read_text().strip()

    amex_interface = AmexInterface(tmp_path)
    assert amex_interface._parse_email(email) == code
