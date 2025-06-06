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

def test_resources_page_elements(driver):
    driver.get("http://127.0.0.1:8000/")

    # Wait for login form to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )

    # Organizer credentials (pol@gmail.com logs to /organizer/)
    driver.find_element(By.NAME, "email").send_keys("io@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Wait for redirect to organizer page after login
    WebDriverWait(driver, 10).until(
        EC.url_contains("/organizer/")
    )

    # Now navigate to resources page
    driver.get("http://127.0.0.1:8000/resources/")

    # Wait for the Resources page header to confirm page load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h2[text()='Resources']"))
    )

    # Assert section headers exist
    assert driver.find_element(By.XPATH, "//h3[contains(text(), 'Text Resources')]")
    assert driver.find_element(By.XPATH, "//h3[contains(text(), 'Photo Resources')]")
    assert driver.find_element(By.XPATH, "//h3[contains(text(), 'File Downloads')]")
    assert driver.find_element(By.XPATH, "//h3[contains(text(), 'Video Tutorials')]")

    # Optional: Check for Download button presence if any
    try:
        download_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Download')]")
        assert download_btn.is_displayed()
    except:
        print("No downloadable files found (skipping check).")

    # Optional: Check Edit/Delete buttons presence
    edit_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'Edit')]")
    delete_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'Delete')]")
    assert len(edit_buttons) > 0 or len(delete_buttons) > 0, "No edit/delete buttons found."
