import os
import logging
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from functools import partial
from datetime import datetime, timezone
from gmail_interface import GmailInterface


class AmexInterface:
    def __init__(self, driver):
        self.driver = driver

    def authenticate(self, username, password, verify_sender):
        self.driver.get("https://global.americanexpress.com/offers/eligible")
        username_xpath = "//input[@id='eliloUserID']"
        self.driver.send_keys(username_xpath, username)
        password_xpath = "//input[@id='eliloPassword']"
        self.driver.send_keys(password_xpath, password)
        login_xpath = "//button[@id='loginSubmit']"
        self.driver.click(login_xpath)
        self._handle_login(verify_sender)

    def _handle_login(self, verify_sender):
        funcs = [
            self._login_success,
            partial(self._need_verify, verify_sender),
        ]
        for func in funcs:
            if self._try_wait(func):
                break
        else:
            raise Exception("Unable to authenticate...")

    def _try_wait(self, func):
        try:
            func()
        except TimeoutException:
            return False
        return True

    def _login_success(self):
        offers_xpath = "//span[contains(text(), 'Amex Offers & Benefits')]"
        self.driver.wait(offers_xpath)
        logging.info("Logged in...")

    def _need_verify(self, verify_sender):
        verify_xpath = "//h1[contains(text(), 'Verify your identity')]"
        self.driver.wait(verify_xpath)
        logging.info("2-factor authentication required...")
        self._verify(verify_sender)

    def add_offers(self):
        row_xpath = (
            "//div[contains(@class, 'offer-row-item')]"
            "[./descendant::span[contains(text(), 'Add to Card')]]"
        )
        try:
            self.driver.wait(row_xpath)
        except TimeoutException:
            logging.info("No offers found...")
            return
        rows = self.driver.driver.find_elements(By.XPATH, row_xpath)
        logging.info(f"Found {len(rows)} offers to add...")
        [self._add_offer(r) for r in rows]

    def _add_offer(self, row):
        info_col = row.find_element(
            By.XPATH,
            ".//div[contains(@class, 'offer-info offer-column')]",
        )
        info = info_col.find_elements(By.XPATH, "./child::*")
        offer, company = [p.text for p in info]
        logging.info(f"Found offer: {offer}")
        logging.info(f"Company: {company}")
        button = row.find_element(
            By.XPATH,
            "//span[contains(text(), 'Add to Card')]",
        )
        self.driver.driver.execute_script("arguments[0].click();", button)
        is_added_xpath = (
            "//div[@data-rowtype='offer']["
            "descendant::span[contains(text(), 'Your offer has been added')]"
            f""" and descendant::p[text()="{company}"]"""
            f""" and descendant::p[text()="{offer}"]]"""
        )
        try:
            self.driver.wait(is_added_xpath)
        except TimeoutException:
            logging.info("Could not verify that offer was added!")
            return
        logging.info("Added offer...")

    def _verify(self, verify_sender):
        logging.info("Sending code to email...")
        sent_time = self._send_code_to_email()
        code = self._get_code_from_email(verify_sender, sent_time)
        logging.info(f"Code: {code}")
        self._enter_code(code)

    def _send_code_to_email(self):
        xpath = (
            "//button[@data-testid='option-button' "
            "and .//h3[contains(text(), 'email')]]"
        )
        self.driver.click(xpath)
        return datetime.now(timezone.utc).replace(microseconds=0)

    def _get_code_from_email(self, sender, sent_time):
        gmail_interface = GmailInterface()
        message = gmail_interface.get_message_by_sender(sender, sent_time)
        return self._parse_email(message)

    def _parse_email(self, message):
        soup = BeautifulSoup(message, "html.parser")
        previous_sibling = soup.find("tr", text="Your Re-authentication Key:")
        return previous_sibling.find_next_sibling().text

    def _enter_code(self, code):
        self.driver.send_keys("//input[@id='question-value']", code)
        # TODO: Submit
        path = os.path.join(os.path.dirname(__file__), "enter_code.html")
        with open(path, "wt") as f:
            f.write(self.driver.driver.page_source)
