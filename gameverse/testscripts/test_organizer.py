import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROME_DRIVER_PATH = r"D:\chromebrowser\chromedriver-win64\chromedriver.exe"

@pytest.fixture
def driver():
    options = Options()
    # options.add_argument("--headless")  # Uncomment to run in headless mode
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def test_organizer_redirect(driver):
    driver.get("http://127.0.0.1:8000/")

    # Wait for login form to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )

    # Organizer credentials
    driver.find_element(By.NAME, "email").send_keys("io@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Wait for redirect to organizer page
    WebDriverWait(driver, 10).until(
        EC.url_contains("/organizer/")
    )

    # Assert organizer page loaded
    assert "/organizer/" in driver.current_url

    # ✅ Check for "Post Tournament Form" button
    post_tournament_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Post Tournament Form']"))
    )
    assert post_tournament_button.is_displayed()
