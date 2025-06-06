import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROME_DRIVER_PATH = r"D:\chromebrowser\chromedriver-win64\chromedriver.exe"
TEST_IMAGE_PATH = r"C:\Users\ASUS\Downloads\ursa.jpg"  # Replace if needed

@pytest.fixture
def driver():
    options = Options()
    # options.add_argument("--headless")  # Optional for headless mode
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def test_edit_profile(driver):
    driver.get("http://127.0.0.1:8000/")

    # Wait for login form
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))

    # Login as existing user (organizer or user)
    driver.find_element(By.NAME, "email").send_keys("pol_updated@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Wait for redirect
    WebDriverWait(driver, 10).until(EC.url_contains("/organizer") or EC.url_contains("/home"))

    # Navigate to profile page
    driver.get("http://127.0.0.1:8000/profile/")

    # Wait for Edit button and click it
    edit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Edit"))
    )
    edit_button.click()

    # Wait for edit form to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )

    # Fill in new data
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "username").send_keys("pol_updated")

    driver.find_element(By.NAME, "email").clear()
    driver.find_element(By.NAME, "email").send_keys("pol_updated@gmail.com")

    # Upload new image
    image_input = driver.find_element(By.NAME, "image")
    image_input.send_keys(TEST_IMAGE_PATH)

    # Submit form
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Wait for redirect back to profile
    WebDriverWait(driver, 10).until(EC.url_contains("/profile"))

    # ✅ Final assertions: Check that updated username/email appear
    assert "pol_updated" in driver.page_source
    assert "pol_updated@gmail.com" in driver.page_source
