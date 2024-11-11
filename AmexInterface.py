import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class AmexInterface:
    def __init__(self, driver):
        self.driver = driver

    def authenticate(self, username, password):
        self.driver.driver.get("https://global.americanexpress.com/offers/eligible")
        username_xpath = "//input[@id='eliloUserID']"
        self.driver.send_keys(username_xpath, username)
        password_xpath = "//input[@id='eliloPassword']"
        self.driver.send_keys(password_xpath, password)
        login_xpath = "//button[@id='loginSubmit']"
        self.driver.click(login_xpath)
        page_loaded_xpath = "//button[@id='ELIGIBLE']"
        try:
            self.driver.wait(page_loaded_xpath)
        except TimeoutException:
            raise Exception(
                "Page did not load after logging in: "
                f"waited {self.driver.timeout} seconds."
            )

    def add_offers(self):
        button_xpath = "./descendant::button[contains(text(), 'Add to Card')]"
        row_xpath = f"//div[@class='row'][{button_xpath}]"
        rows = self.driver.find_elements(By.XPATH, row_xpath)

        offerColumnXPath = (
            "./ancestor::div[contains(@class, "
            "'offer-info offer-column')]"
        )
        companyXPath = (
            "./descendant::p[contains(@class, 'body-1')]"
            f"[{offerColumnXPath}]"
        )
        offerXPath = (
            "./descendant::p[contains(@class, 'heading-3')]"
            f"[{offerColumnXPath}]"
        )
        for row in rows:
            offerElement = row.find_element(By.XPATH, offerXPath)
            offer = offerElement.get_attribute("innerText")
            logging.info(f"Found offer: {offer}")

            companyElement =  row.find_element(By.XPATH, companyXPath)
            company = companyElement.get_attribute("innerText")
            logging.info(f"Company: {company}")

            button = row.find_element(By.XPATH, f"//{buttonXPath}")
            self.driver.execute_script("arguments[0].click();", button)

            isAddedXPath = (
                "//div[@data-rowtype='offer']["
                "descendant::span[contains(text(), 'Your offer has been added')]"
                f""" and descendant::p[text()="{company}"]"""
                f""" and descendant::span[text()="{offer}"]]"""
            )
            isAdded = EC.presence_of_element_located((By.XPATH, isAddedXPath))
            try:
                WebDriverWait(self.driver, self._timeout).until(isAdded)
            except TimeoutException:
                logging.info("Could not verify that offer was added!")
                continue
            logging.info("Added offer...")

