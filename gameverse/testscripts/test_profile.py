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
    # options.add_argument("--headless")  # Uncomment for headless mode
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def test_profile_page_elements(driver):
    driver.get("http://127.0.0.1:8000/")

    # Wait for login form
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )

    # Log in as organizer or user
    driver.find_element(By.NAME, "email").send_keys("pol_updated@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    # Wait for redirect to either organizer or home page
    WebDriverWait(driver, 10).until(
        lambda d: "/organizer/" in d.current_url or "/home/" in d.current_url
    )

    # Navigate to profile page
    driver.get("http://127.0.0.1:8000/profile/")

    # Wait for profile page heading (e.g. "<username>'s Profile")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), \"'s Profile\")]"))
    )

    # Assert profile image is visible (either user image or default)
    profile_img = driver.find_element(By.XPATH, "//div[@class='profile-card']//img")
    assert profile_img.is_displayed()

    # Assert username heading includes 'Profile'
    heading = driver.find_element(By.XPATH, "//h2[contains(text(), \"'s Profile\")]")
    assert heading.is_displayed()

    # Assert email label and email text are present
    email_label = driver.find_element(By.XPATH, "//strong[contains(text(), 'Email:')]")
    email_text = driver.find_element(By.XPATH, "//span[@class='text-muted']")
    assert email_label.is_displayed()
    assert email_text.is_displayed()

    # Assert Edit button exists and visible
    edit_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Edit')]")
    assert edit_button.is_displayed()
