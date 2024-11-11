import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class AmexInterface:
    def __init__(self, driver):
        self.driver = driver
        self._set_xpaths()

    def _set_xpaths(self):
        self._button_xpath = (
            "./descendant::span[contains(text(), "
            "'Add to Card')]"
        )
        self._row_xpath = f"//div[contains(@class, 'offer-row-item')][{self._button_xpath}]"
        offer_column_xpath = (
            "./ancestor::div[contains(@class, "
            "'offer-info offer-column')]"
        )
        self._offer_column_xpath = offer_column_xpath
        self._company_xpath = (
            "./descendant::p[contains(@class, 'body-1')]"
            f"[{offer_column_xpath}]"
        )
        self._offer_xpath = (
            "./descendant::p[contains(@class, 'heading-3')]"
            f"[{offer_column_xpath}]"
        )

    def authenticate(self, username, password):
        self.driver.get("https://global.americanexpress.com/offers/eligible")
        username_xpath = "//input[@id='eliloUserID']"
        self.driver.send_keys(username_xpath, username)
        password_xpath = "//input[@id='eliloPassword']"
        self.driver.send_keys(password_xpath, password)
        login_xpath = "//button[@id='loginSubmit']"
        self.driver.click(login_xpath)
        self._post_login()

    def _post_login(self):
        try:
            self.driver.wait(self._row_xpath)
        except TimeoutException:
            try:
                self.driver.wait("//h1[contains(text(), 'Verify your identity')]")
                self._verify()
            except TimeoutException:
                raise Exception(
                    "Page did not load after logging in: "
                    f"waited {self.driver.timeout} seconds."
                )

    def add_offers(self):
        #test = self.driver.driver.find_elements(By.XPATH, self._row_xpath)
        #print(test[0].get_attribute("outerHTML"))
        rows = self.driver.driver.find_elements(By.XPATH, self._row_xpath)
        logging.info(f"Found {len(rows)} offers to add...")
        for i, r in enumerate(rows):
            if i > 3:
                return
            self._add_offer(r)
        #[self._add_offer(r) for r in rows]

    def _add_offer(self, row):
        offer_info = row.find_element(By.XPATH, "//div[contains(@class, 'offer-info offer-column')]")
        offer, company = [p.text for p in offer_info.find_elements(By.XPATH, "./child::*")]
        logging.info(f"Found offer: {offer}")
        logging.info(f"Company: {company}")
        button = row.find_element(By.XPATH, "//span[contains(text(), 'Add to Card')]")
        self.driver.driver.execute_script("arguments[0].click();", button)
        import time
        time.sleep(3)
        print(self.driver.driver.page_source)
        is_added_xpath = (
            "//div[@data-rowtype='offer']["
            "descendant::span[contains(text(), 'Your offer has been added')]"
            f""" and descendant::p[text()="{company}"]"""
            f""" and descendant::span[text()="{offer}"]]"""
        )
        try:
            self.driver.wait(is_added_xpath)
        except TimeoutException:
            logging.info("Could not verify that offer was added!")
            return
        logging.info("Added offer...")

    def _verify(self):
        self._send_code_to_email()
        code = self._get_code_from_email()
        self._enter_code(code)

    def _send_code_to_email(self):
        self.driver.click("//button[@data-testid='option-button']")

    def _get_code_from_email(self):
        # TODO
        return "123456"

    def _enter_code(self, code):
        self.driver.send_keys("//input[@id='question-value']", code)
