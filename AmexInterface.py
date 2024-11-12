import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class AmexInterface:
    def __init__(self, driver):
        self.driver = driver
        self._set_xpaths()

    def _set_xpaths(self):
        self._row_xpath = (
            "//div[contains(@class, 'offer-row-item')]"
            "[./descendant::span[contains(text(), 'Add to Card')]]"
        )

    def authenticate(self, username, password):
        self.driver.get("https://global.americanexpress.com/offers/eligible")
        username_xpath = "//input[@id='eliloUserID']"
        self.driver.send_keys(username_xpath, username)
        password_xpath = "//input[@id='eliloPassword']"
        self.driver.send_keys(password_xpath, password)
        login_xpath = "//button[@id='loginSubmit']"
        self.driver.click(login_xpath)
        self._handle_login()

    def _handle_login(self):
        for func in [self._login_success, self._need_verify]:
            if self._try_wait(func):
                break

    def _try_wait(self, func):
        try:
            func()
        except TimeoutException:
            return False
        return True

    def _login_success(self):
        self.driver.wait(self._row_xpath)
        logging.info("Logged in...")

    def _need_verify(self):
        verify_xpath = "//h1[contains(text(), 'Verify your identity')]"
        self.driver.wait(verify_xpath)
        logging.info("2-factor authentication required...")
        self._verify()

    def add_offers(self):
        rows = self.driver.driver.find_elements(By.XPATH, self._row_xpath)
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

    def _verify(self):
        logging.info("Sending code to email...")
        self._send_code_to_email()
        code = self._get_code_from_email()
        logging.info(f"Code: {code}")
        self._enter_code(code)

    def _send_code_to_email(self):
        xpath = (
            "//button[@data-testid='option-button' "
            "and .//h3[contains(text(), 'email')]]"
        )
        self.driver.click(xpath)

    def _get_code_from_email(self):
        # TODO
        return "123456"

    def _enter_code(self, code):
        self.driver.send_keys("//input[@id='question-value']", code)
        # TODO: Submit
