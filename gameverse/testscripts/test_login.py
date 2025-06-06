import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

CHROME_DRIVER_PATH = r"D:\chromebrowser\chromedriver-win64\chromedriver.exe"

@pytest.fixture
def driver():
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

def test_homepage_title(driver):
    driver.get("http://127.0.0.1:8000/")
    time.sleep(2)
    assert "Login" in driver.title

