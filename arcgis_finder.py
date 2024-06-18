"""
lfarchio@msudenver.edu | 6/18/2024 | @j4eva 
"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def initialize_driver(chromedriver_path):
    """Initialize the WebDriver."""
    options = webdriver.ChromeOptions()
    options.headless = False  # Set to True to run in headless mode
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_out_fields(driver, url):
    """Get the out fields from the API page."""
    driver.get(url)
    try:
        # Wait until the elements are present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.simple-input-checkboxes-item.ember-view'))
        )
        
        # Find all checkbox items within the main container div
        checkbox_items = driver.find_elements(By.CSS_SELECTOR, '.simple-input-checkboxes-item.ember-view label input[type="checkbox"]')
        field_names = []
        for item in checkbox_items:
            field_name = item.get_attribute('name')
            if field_name:
                field_names.append(field_name)
        return field_names
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_to_file(filename, field_names, url):
    """Save the field names and the URL to a file."""
    folder = "ArcGIS"
    if not os.path.exists(folder):
        os.makedirs(folder)  # Create the directory if it doesn't exist
    file_path = os.path.join(folder, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"URL: {url}\n\n")  # Write the URL at the top of the file
        for name in field_names:
            file.write(f"{name}\n")

def main():
    url = input("Enter the URL of the API page: ").strip()
    filename = input("Enter the name of the text file to save the out fields (e.g., out_fields.txt): ").strip()
    chromedriver_path = input("Enter the path to your ChromeDriver: Check readME for Mac use \ ").strip()
    if not os.path.exists(chromedriver_path):
        print(f"ChromeDriver not found at {chromedriver_path}")
        return
    driver = initialize_driver(chromedriver_path)
    try:
        field_names = get_out_fields(driver, url)
        if field_names:
            save_to_file(filename, field_names, url)
            print(f"Saved out fields to {filename}")
        else:
            print("Could not find out fields.")
    finally:
        driver.quit()  # Ensure the driver is quit even if an error occurs

if __name__ == "__main__":
    main()
