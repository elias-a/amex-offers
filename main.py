import pathlib
from ChromeDriver import ChromeDriver

configPath = f"{pathlib.Path(__file__).parent.resolve()}/config.ini"

try:
    driver = ChromeDriver(configPath)
finally:
    driver.closeChrome()