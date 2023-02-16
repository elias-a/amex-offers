import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class AmexInterface:
    def __init__(self, driver, timeout = 10):
        self.driver = driver
        self._timeout = timeout

    def authenticate(self, username, password):
        self.driver.get("https://global.americanexpress.com/offers/eligible")

        # Enter username.
        usernameXPath = "//input[@id='eliloUserID']"
        usernameIsLoaded = EC.presence_of_element_located((By.XPATH, usernameXPath))
        usernameInput = WebDriverWait(self.driver, self._timeout).until(usernameIsLoaded)
        usernameInput.send_keys(username)

        # Enter password.
        passwordXPath = "//input[@id='eliloPassword']"
        passwordIsLoaded = EC.presence_of_element_located((By.XPATH, passwordXPath))
        passwordInput = WebDriverWait(self.driver, self._timeout).until(passwordIsLoaded)
        passwordInput.send_keys(password)

        loginXPath = "//button[@id='loginSubmit']"
        loginIsLoaded = EC.presence_of_element_located((By.XPATH, loginXPath))
        loginButton = WebDriverWait(self.driver, self._timeout).until(loginIsLoaded)
        self.driver.execute_script("arguments[0].click();", loginButton)

        isPageLoadedXPath = "//button[@id='ELIGIBLE']"
        isPageLoaded = EC.presence_of_element_located((By.XPATH, isPageLoadedXPath))
        try:
            WebDriverWait(self.driver, self._timeout).until(isPageLoaded)
        except TimeoutException:
            raise Exception(f"Page did not load after logging in: waited {self._timeout} seconds.")

    def addOffers(self):
        buttonXPath = "./descendant::button[contains(text(), 'Add to Card')]"
        rowXPath = f"//div[@class='row'][{buttonXPath}]"
        rows = self.driver.find_elements(By.XPATH, rowXPath)

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

