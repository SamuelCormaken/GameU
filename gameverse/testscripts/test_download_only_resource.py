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
    # options.add_argument("--headless")  # Uncomment if you want to run without UI
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def test_download_resource(driver):
    driver.get("http://127.0.0.1:8000/")

    wait = WebDriverWait(driver, 10)

    # Login
    wait.until(EC.presence_of_element_located((By.NAME, "email")))
    driver.find_element(By.NAME, "email").send_keys("io@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Wait for organizer dashboard
    wait.until(EC.url_contains("/organizer/"))

    # Go to resources page
    driver.get("http://127.0.0.1:8000/resources/")
    wait.until(EC.presence_of_element_located((By.XPATH, "//h2[text()='Resources']")))

    # Locate download buttons in the "File Downloads" section
    file_section = driver.find_element(By.CLASS_NAME, "file-resource")
    download_links = file_section.find_elements(By.XPATH, ".//a[contains(text(), 'Download')]")

    # Assert at least one download link is present
    assert download_links, "No download links found in file-resource section."

    # Optionally print the download URLs
    for link in download_links:
        print("Download URL:", link.get_attribute("href"))

    # Optionally trigger a download (will open in browser if not headless)
    # download_links[0].click()
