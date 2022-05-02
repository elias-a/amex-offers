from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AmexInterface():
    def __init__(self, driver):
        self.driver = driver

    def authenticate(self, username, password):
        self.driver.get("https://global.americanexpress.com/offers/eligible")

        # Enter username.
        usernameInput = self.driver.find_element(By.XPATH, "//input[@id='eliloUserID']")
        usernameInput.send_keys(username)

        # Enter password.
        passwordInput = self.driver.find_element(By.XPATH, "//input[@id='eliloPassword']")
        passwordInput.send_keys(password)

        loginButton = self.driver.find_element(By.XPATH, "//button[@id='loginSubmit']")
        loginButton.click()