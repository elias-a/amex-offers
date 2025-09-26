import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class ChromeDriver:
    def __init__(
        self,
        chromedriver_path,
        user_data_dir,
        headless=False,
        timeout=10,
    ):
        self.timeout = timeout
        self.driver = self._init_driver(
            chromedriver_path,
            user_data_dir,
            headless,
        )

    def __del__(self):
        self.driver.quit()

    def _init_driver(self, chromedriver_path, user_data_dir, headless):
        return uc.Chrome(
            driver_executable_path=chromedriver_path,
            user_data_dir=user_data_dir,
            headless=headless,
        )

    def _add_options(self, opts):
        options = uc.ChromeOptions()
        [options.add_experimental_option(k, v) for k, v in opts.items()]
        return options

    def get_page_source(self):
        return self.driver.page_source

    def get(self, url):
        self.driver.get(url)

    def send_keys(self, xpath, text):
        is_loaded = EC.presence_of_element_located((By.XPATH, xpath))
        element = WebDriverWait(self.driver, self.timeout).until(is_loaded)
        element.send_keys(text)

    def click(self, xpath):
        is_loaded = EC.element_to_be_clickable((By.XPATH, xpath))
        element = WebDriverWait(self.driver, self.timeout).until(is_loaded)
        self.driver.execute_script("arguments[0].click();", element)

    def wait(self, xpath):
        is_loaded = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(self.driver, self.timeout).until(is_loaded)

    def wait_and_get(self, xpath):
        try:
            self.wait(xpath)
        except TimeoutException:
            return []
        return self.driver.find_elements(By.XPATH, xpath)
