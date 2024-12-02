import os
import tomllib
import logging
from ChromeDriver import ChromeDriver
from amex_offers import AmexInterface


log_file = os.path.join(os.path.dirname(__file__), "amex-offers.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)


logging.info("Starting program to add Amex offers...")
with open(os.path.join(os.path.dirname(__file__), "config.toml"), "rb") as f:
    config = tomllib.load(f)
username = config["AMEX"]["USERNAME"]
password = config["AMEX"]["PASSWORD"]
profile_path = config["CHROME"]["PROFILE"]
headless = config["CHROME"]["HEADLESS"]
verify_sender = config["GMAIL"]["SENDER"]
error_html_path = None
if "DEBUGGING" in config and "ERROR_HTML_PATH" in config["DEBUGGING"]:
    error_html_path = config["DEBUGGING"]["ERROR_HTML_PATH"]
logging.info("Opening Chrome...")
driver = ChromeDriver(profile_path, headless=headless)
try:
    amex_interface = AmexInterface(driver)
    logging.info("Authenticating...")
    amex_interface.authenticate(username, password, verify_sender)
    logging.info("Adding offers...")
    amex_interface.add_offers()
except Exception as e:
    if error_html_path is not None:
        with open(error_html_path, "wt") as f:
            f.write(driver.driver.page_source)
    logging.error(e)
    logging.info("Exiting program...")
