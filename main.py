import tomllib
import logging
from pathlib import Path
from amex_offers import AmexInterface


log_file = Path(__file__).parent / "amex-offers.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)


with open(Path(__file__).parent / "config.toml", "rb") as f:
    config = tomllib.load(f)
chrome_profile_path = config["CHROME"]["PROFILE"]
username = config["AMEX"]["USERNAME"]
password = config["AMEX"]["PASSWORD"]
verify_sender = config["GMAIL"]["SENDER"]
error_html_path = config.get("ERROR_HTML_PATH", "error.html")

with AmexInterface(
    chrome_profile_path,
    username,
    password,
    verify_sender,
    error_html_path,
) as amex_interface:
    amex_interface.add_offers()
