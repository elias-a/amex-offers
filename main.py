import os
import logging
from configparser import ConfigParser
from ChromeDriver import ChromeDriver
from amex_offers import AmexInterface


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("amex-offers.log"),
        logging.StreamHandler(),
    ],
)


logging.info("Starting program to add Amex offers...")
config = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.ini"))
username = config["AMEX"]["USERNAME"]
password = config["AMEX"]["PASSWORD"]
profile_path = config["CHROME"]["PROFILE"]
verify_sender = config["GMAIL"]["SENDER"]
logging.info("Opening Chrome...")
driver = ChromeDriver(profile_path)
try:
    amex_interface = AmexInterface(driver)
    logging.info("Authenticating...")
    amex_interface.authenticate(username, password, verify_sender)
    logging.info("Adding offers...")
    amex_interface.add_offers()
except Exception as e:
    logging.error(e)
