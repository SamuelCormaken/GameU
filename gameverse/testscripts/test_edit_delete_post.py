import time
import uuid
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

CHROME_DRIVER_PATH = r"D:\chromebrowser\chromedriver-win64\chromedriver.exe"
IMAGE_PATH = r"C:\Users\ASUS\Downloads\dota2.jpg"

@pytest.fixture
def driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    options = Options()
    # options.add_argument("--headless")  # Uncomment if you want headless mode
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def login(driver):
    driver.get("http://127.0.0.1:8000/")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys("Sarj@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    wait.until(EC.url_contains("/home"))

def test_edit_delete_post_with_image(driver):
    wait = WebDriverWait(driver, 10)
    login(driver)

    unique_id = str(uuid.uuid4())[:8]
    description = f"Post with image {unique_id}"

    # Create new post with image
    wait.until(EC.presence_of_element_located((By.NAME, "description"))).send_keys(description)
    driver.find_element(By.NAME, "image").send_keys(IMAGE_PATH)
    driver.find_element(By.XPATH, "//form//button[text()='Post']").click()

    # Wait for the new post to appear
    wait.until(EC.presence_of_element_located((By.XPATH, f"//p[contains(text(), '{description}')]")))

    # Click the Edit button for the post
    edit_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, f"//p[contains(text(), '{description}')]/ancestor::div[contains(@class,'feed')]//a[contains(text(), 'Edit')]"
    )))
    edit_button.click()

    # Edit post description
    new_description = "Updated description via Selenium"
    edit_field = wait.until(EC.presence_of_element_located((By.NAME, "description")))
    edit_field.clear()
    edit_field.send_keys(new_description)
    driver.find_element(By.XPATH, "//form//button[contains(text(), 'Update')]").click()

    # Wait for the updated post to appear
    wait.until(EC.presence_of_element_located((By.XPATH, f"//p[contains(text(), '{new_description}')]")))

    # Click the Delete button for the updated post
    delete_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, f"//p[contains(text(), '{new_description}')]/ancestor::div[contains(@class,'feed')]//a[contains(text(), 'Delete')]"
    )))
    delete_button.click()

    # On delete confirmation page, click "Yes, Delete"
    confirm_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//form//button[contains(text(), 'Yes, Delete')]"
    )))
    confirm_button.click()

    # Wait to be redirected back to home page
    wait.until(EC.url_contains("/home"))

    # Short pause to allow page update
    time.sleep(1)

    # Define the container that holds all posts — adjust if needed to your actual feed container
    post_feed_xpath = "//div[@id='posts-feed']"  # Change this if your feed container has a different id or class

    try:
        # Wait until the deleted post description text is no longer present in the post feed
        wait.until_not(EC.text_to_be_present_in_element((By.XPATH, post_feed_xpath), new_description))
    except TimeoutException:
        # Debug: check if the post container with the deleted text still exists somewhere
        post_container_xpath = f"//p[contains(text(), '{new_description}')]/ancestor::div[contains(@class,'feed')]"
        elems = driver.find_elements(By.XPATH, post_container_xpath)
        print(f"Still found {len(elems)} elements with post text after deletion")
        for i, el in enumerate(elems):
            print(f"Element {i} text snippet: {el.text[:100]}")
        raise AssertionError("Post was not deleted successfully")
