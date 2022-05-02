import pathlib
from configparser import ConfigParser
from ChromeDriver import ChromeDriver
from AmexInterface import AmexInterface

config = ConfigParser()
configPath = f"{pathlib.Path(__file__).parent.resolve()}/config.ini"
config.read(configPath)
username = config["AMEX"]["username"]
password = config["AMEX"]["password"]

try:
    driver = ChromeDriver(configPath)

    amexInterface = AmexInterface(driver.driver)
    amexInterface.authenticate(username, password)
    amexInterface.addOffers()
finally:
    driver.closeChrome()