import os
import logging
from configparser import ConfigParser
from ChromeDriver import ChromeDriver
from AmexInterface import AmexInterface

logging.basicConfig(
    filename="amex-offers.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.info("Starting program to add Amex offers...")

config = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.ini"))
username = config["AMEX"]["username"]
password = config["AMEX"]["password"]

logging.info("Opening Chrome...")
driver = ChromeDriver()
driver.initDriver()
try:
    amexInterface = AmexInterface(driver.driver)
    amexInterface.authenticate(username, password)
    amexInterface.addOffers()
except Exception as e:
    logging.error(e)
finally:
    logging.info("Closing Chrome...")
    driver.closeChrome()

