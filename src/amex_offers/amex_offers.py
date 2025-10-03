import logging
from selenium.webdriver.common.by import By


class AmexOffers:
    def __init__(self, driver):
        self.driver = driver

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
        [self._add_offer(r) for r in rows]

    def _add_offer(self, row):
        info = row.find_elements(
            By.XPATH,
            ".//div[@data-testid='overflowTextContainer']",
        )

        company, offer = [p.text for p in info]
        logging.info(f"Found offer: {offer}")
        logging.info(f"Company: {company}")

        button_xpath = ".//button[@data-testid='merchantOfferListAddButton']"
        button = row.find_element(By.XPATH, button_xpath)
        self.driver.click_element(button)

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
