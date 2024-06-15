"""
lfarchio@msudenver.edu | @j4eva | 6/10/2024
"""

import os
from seleniumbase import Driver
from time import sleep

def initialize_driver():
    """Initialize the WebDriver using SeleniumBase."""
    driver = Driver(headless=True)  # Run in headless mode
    return driver

def get_wikipedia_paragraphs(driver, keyword, num_paragraphs=3):
    """Get the first few paragraphs from a Wikipedia page."""
    url = f"https://en.wikipedia.org/wiki/{keyword.replace(' ', '_')}"
    driver.get(url)
    sleep(2)  # Wait for the page to load

    try:
        paragraphs = driver.find_elements("css selector", 'p')[:num_paragraphs]
        text = "\n\n".join([p.text for p in paragraphs if p.text])
        return text
    except Exception as e:
        return None

def save_to_file(keyword, text, folder="WikiStateParks"):
    """Save the text to a file."""
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, f"{keyword.replace(' ', '_')}.txt")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

def click_through_links(driver, keyword, num_paragraphs=3):
    """Click through links on a Wikipedia page and save details."""
    url = f"https://en.wikipedia.org/wiki/{keyword.replace(' ', '_')}"
    driver.get(url)
    sleep(2)  # Wait for the page to load

    links = driver.find_elements("css selector", 'a')
    for link in links:
        try:
            href = link.get_attribute('href')
            if href and 'Colorado' in href:
                driver.get(href)
                sleep(2)  # Wait for the new page to load
                text = get_wikipedia_paragraphs(driver, href.split('/')[-1], num_paragraphs)
                if text:
                    save_to_file(href.split('/')[-1], text)
                    print(f"Saved details for {href}")
        except Exception as e:
            continue

def load_keywords(file_path):
    """Load keywords from a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def main():
    folder = "Colorado"
    counties_file = os.path.join(folder, "counties.txt")
    cities_file = os.path.join(folder, "cities.txt")
    monuments_file = os.path.join(folder, "monuments.txt")
    state_parks_file = os.path.join(folder, "stateparks.txt")
    national_parks_file = os.path.join(folder, "nationalparks.txt")

    if not os.path.exists(counties_file) or not os.path.exists(cities_file) or not os.path.exists(monuments_file) or not os.path.exists(state_parks_file) or not os.path.exists(national_parks_file):
        print(f"Ensure 'counties.txt', 'cities.txt', 'monuments.txt', 'stateparks.txt', and 'nationalparks.txt' are present in the '{folder}' folder.")
        return

    choice = input("Do you want to process 'county', 'city', 'monuments', 'state parks', or 'national parks'? ").strip().lower()
    if choice == 'county':
        keywords = load_keywords(counties_file)
    elif choice == 'city':
        keywords = load_keywords(cities_file)
    elif choice == 'monuments':
        keywords = load_keywords(monuments_file)
    elif choice == 'state parks':
        keywords = load_keywords(state_parks_file)
    elif choice == 'national parks':
        keywords = load_keywords(national_parks_file)
    else:
        print("Invalid choice. Please enter 'county', 'city', 'monuments', 'state parks', or 'national parks'.")
        return

    driver = initialize_driver()
    for keyword in keywords:
        print(f"Processing: {keyword}")
        text = get_wikipedia_paragraphs(driver, keyword)
        if text:
            save_to_file(keyword, text, "WikiStateParks")
            print(f"Saved details for {keyword}")
        else:
            print(f"Could not find details for {keyword}")
        click_through_links(driver, keyword)
    driver.quit()

if __name__ == "__main__":
    main()
