import logging
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timezone
from gmail_interface import GmailInterface


class AmexAuth:
    def __init__(self, driver, username, password, verify_sender):
        self.driver = driver
        self.username = username
        self.password = password
        self.verify_sender = verify_sender

    def authenticate(self):
        logging.info("Authenticating...")

        self.driver.get("https://global.americanexpress.com/offers/eligible")

        username_xpath = "//input[@id='eliloUserID']"
        self.driver.send_keys(username_xpath, self.username)

        password_xpath = "//input[@id='eliloPassword']"
        self.driver.send_keys(password_xpath, self.password)

        login_xpath = "//button[@id='loginSubmit']"
        self.driver.click(login_xpath)

        self._verify()
        self._add_trusted_device()
        self._check_logged_in()

    def _check_logged_in(self):
        try:
            self.driver.wait("//*[contains(text(), 'Recommended Offers')]")
            logging.info("Logged in...")
        except TimeoutException as e:
            logging.error("Unable to authenticate...")
            raise e

    def _verify(self):
        if self._need_verify():
            logging.info("Sending code to email...")
            sent_time = self._send_code_to_email()
            code = self._get_code_from_email(self.verify_sender, sent_time)
            logging.info(f"Code: {code}")
            self._enter_code(code)

    def _need_verify(self):
        try:
            self.driver.wait("//h1[contains(text(), 'Verify your identity')]")
            logging.info("2-factor authentication required...")
            return True
        except TimeoutException:
            logging.info("2-factor authentication not required...")
            return False

    def _add_trusted_device(self):
        try:
            self.driver.click(
                "//button[@id='submitBtn' and "
                "contains(., 'Add This Device')]"
            )
            logging.info("Added trusted device...")
        except TimeoutException:
            logging.info("Not prompted to trust device...")

    def _send_code_to_email(self):
        self.driver.click(
            "//button[@data-testid='option-button' "
            "and .//h3[contains(text(), 'email')]]"
        )
        return datetime.now(timezone.utc).replace(microsecond=0)

    def _get_code_from_email(self, sender, sent_time):
        gmail_interface = GmailInterface()
        message = gmail_interface.get_message_by_sender(sender, sent_time)
        return self._parse_email(message)

    def _parse_email(self, message):
        soup = BeautifulSoup(message, "html.parser")
        p_tag = soup.find("p", string="One-Time Verification Code:")
        previous_sibling = p_tag.find_parent("tr")
        return previous_sibling.find_next_sibling().get_text().strip()

    def _enter_code(self, code):
        logging.info("Entering verification code...")
        self.driver.send_keys("//input[@id='question-value']", code)
        self.driver.click("//button[@data-testid='continue-button']")
