import logging
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timezone
from gmail_interface import GmailInterface
from .chrome_driver import ChromeDriver


class AmexInterface:
    def __init__(self, chrome_profile_path):
        chromedriver_path = chromedriver_autoinstaller.install()

        logging.info("Opening Chrome...")
        self.driver = ChromeDriver(
            chromedriver_path,
            chrome_profile_path,
            headless=True,
        )
        logging.info("Chrome opened successfully...")

    def authenticate(self, username, password, verify_sender):
        logging.info("Authenticating...")

        self.driver.get("https://global.americanexpress.com/offers/eligible")

        username_xpath = "//input[@id='eliloUserID']"
        self.driver.send_keys(username_xpath, username)

        password_xpath = "//input[@id='eliloPassword']"
        self.driver.send_keys(password_xpath, password)

        login_xpath = "//button[@id='loginSubmit']"
        self.driver.click(login_xpath)

        self._verify(verify_sender)
        self._add_trusted_device()
        self._check_logged_in()

    def _check_logged_in(self):
        try:
            self.driver.wait("//*[contains(text(), 'Recommended Offers')]")
            logging.info("Logged in...")
        except TimeoutException as e:
            logging.error("Unable to authenticate...")
            raise e

    def _verify(self, verify_sender):
        if self._need_verify():
            logging.info("Sending code to email...")
            sent_time = self._send_code_to_email()
            code = self._get_code_from_email(verify_sender, sent_time)
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

    def add_offers(self):
        rows = self.driver.wait_and_get(
            "//div["
            ".//div[@data-testid='overflowTextContainer'] and "
            ".//button[@data-testid='merchantOfferListAddButton']"
            "][not(.//*[self::div]["
            ".//div[@data-testid='overflowTextContainer'] and "
            ".//button[@data-testid='merchantOfferListAddButton']"
            "])]"
        )
        logging.info(f"Found {len(rows)} offers to add...")

        logging.info("Adding offers...")
        #[self._add_offer(r) for r in rows]
        [self._add_offer(r) for r in [rows[0]]]

    def _add_offer(self, row):
        info = row.find_elements(
            By.XPATH,
            ".//div[@data-testid='overflowTextContainer']",
        )

        company, offer = [p.text for p in info]
        logging.info(f"Found offer: {offer}")
        logging.info(f"Company: {company}")

        button = row.find_element(
            By.XPATH,
            ".//button[@data-testid='merchantOfferListAddButton']",
        )
        self.driver.driver.execute_script("arguments[0].click();", button)

        added_row = self.driver.wait_and_get(
            "//div["
            f'.//span[text()="{company}"] and '
            ".//span[@data-testid='merchantOfferSuccessIcon']"
            "][not(.//*[self::div]["
            f'.//span[text()="{company}"] and '
            ".//span[@data-testid='merchantOfferSuccessIcon']"
            "])]"
        )
        if len(added_row) > 0:
            logging.info("Added offer...")
        else:
            logging.info("Could not verify that offer was added!")

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
