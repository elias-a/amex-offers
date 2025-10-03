import logging
from .chrome_driver import ChromeDriver
from .amex_auth import AmexAuth
from .amex_offers import AmexOffers


class AmexInterface:
    def __init__(
        self,
        chrome_profile_path,
        username,
        password,
        verify_sender,
        error_html_path,
    ):
        logging.info("Starting program to add Amex offers...")

        self.error_html_path = error_html_path

        logging.info("Opening Chrome...")
        self.driver = ChromeDriver(chrome_profile_path, headless=True)
        logging.info("Chrome opened successfully...")

        self.auth = AmexAuth(self.driver, username, password, verify_sender)
        self.offers = AmexOffers(self.driver)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.error_html_path, "wt") as f:
            f.write(self.driver.get_page_source())

        if exc_type:
            logging.exception("An exception has occurred")

        logging.info("Exiting program...")

    def add_offers(self):
        self.auth.authenticate()
        self.offers.add_offers()
