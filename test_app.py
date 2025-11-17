import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Get the URL of the deployed app from the environment variable
APP_URL = os.environ.get("APP_URL")

if not APP_URL:
    raise Exception("APP_URL environment variable not set.")

print(f"Testing application at: {APP_URL}")

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
print("WebDriver initialized.")

try:
    driver.get(APP_URL)
    print("Page loaded.")

    # Wait for the form to be present
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "form"))
    )
    print("Form found.")

    # Fill the form with default values
    # We find elements by their 'id' from the HTML
    driver.find_element(By.ID, "pregnant").send_keys("1")
    driver.find_element(By.ID, "glucose").send_keys("120")
    driver.find_element(By.ID, "bp").send_keys("70")
    driver.find_element(By.ID, "skin").send_keys("20")
    driver.find_element(By.ID, "insulin").send_keys("80")
    driver.find_element(By.ID, "bmi").send_keys("32.5")
    driver.find_element(By.ID, "pedigree").send_keys("0.5")
    driver.find_element(By.ID, "age").send_keys("40")
    print("Form filled.")

    # Click the predict button
    driver.find_element(By.TAG_NAME, "button").click()
    print("Predict button clicked.")

    # Wait for the prediction result to appear
    # We check if the 'h2' tag with id 'prediction_result' contains the text 'Prediction:'
    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element((By.ID, "prediction_result"), "Prediction:")
    )
    
    result_text = driver.find_element(By.ID, "prediction_result").text
    print(f"Test successful! Result: {result_text}")

except Exception as e:
    print(f"An error occurred during the test: {e}")
    # Take a screenshot on failure
    driver.save_screenshot("test_failure.png")
    # Print page source
    print("\nPAGE SOURCE:\n", driver.page_source)
    # Re-raise the exception to fail the job
    raise e

finally:
    driver.quit()
    print("WebDriver closed.")