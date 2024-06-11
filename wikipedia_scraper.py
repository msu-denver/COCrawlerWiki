"""
lfarchio@msudenver.edu | @j4eva | 6/10/2024
"""

import os
from seleniumbase import Driver
from time import sleep

def initialize_driver():
    """
    Initialize the WebDriver using SeleniumBase in headless mode.
    Returns:
        driver (Driver): Initialized SeleniumBase WebDriver instance.
    """
    driver = Driver(headless=True)
    return driver

def get_wikipedia_paragraphs(driver, keyword, num_paragraphs=3):
    """
    Retrieve the first few paragraphs from a Wikipedia page.
    Args:
        driver (Driver): The Selenium WebDriver instance.
        keyword (str): The keyword to search for on Wikipedia.
        num_paragraphs (int): The number of paragraphs to retrieve.
    Returns:
        text (str): The concatenated text of the first few paragraphs.
    """
    url = f"https://en.wikipedia.org/wiki/{keyword.replace(' ', '_')}"
    driver.get(url)
    sleep(2)  # Wait for the page to load

    try:
        paragraphs = driver.find_elements("css selector", 'p')[:num_paragraphs]
        text = "\n\n".join([p.text for p in paragraphs if p.text])
        return text
    except Exception as e:
        return None

def save_to_file(keyword, text, folder="Wiki"):
    """
    Save the retrieved text to a file.
    Args:
        keyword (str): The keyword used for naming the file.
        text (str): The text content to save.
        folder (str): The folder to save the file in.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, f"{keyword.replace(' ', '_')}.txt")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

def click_through_links(driver, keyword, num_paragraphs=3):
    """
    Click through links on a Wikipedia page and save details for relevant links.
    Args:
        driver (Driver): The Selenium WebDriver instance.
        keyword (str): The keyword to search for on Wikipedia.
        num_paragraphs (int): The number of paragraphs to retrieve from each link.
    """
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
    """
    Load keywords from a text file.
    Args:
        file_path (str): The path to the file containing the keywords.
    Returns:
        keywords (list): A list of keywords.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def main():
    """
    Main function to process user input, load keywords, and retrieve Wikipedia content.
    """
    folder = "Colorado"
    counties_file = os.path.join(folder, "counties.txt")
    cities_file = os.path.join(folder, "cities.txt")

    if not os.path.exists(counties_file) or not os.path.exists(cities_file):
        print(f"Ensure both 'counties.txt' and 'cities.txt' are present in the '{folder}' folder.")
        return

    choice = input("Do you want to process 'county' or 'city'? ").strip().lower()
    if choice == 'county':
        keywords = load_keywords(counties_file)
    elif choice == 'city':
        keywords = load_keywords(cities_file)
    else:
        print("Invalid choice. Please enter 'county' or 'city'.")
        return

    driver = initialize_driver()
    for keyword in keywords:
        print(f"Processing: {keyword}")
        text = get_wikipedia_paragraphs(driver, keyword)
        if text:
            save_to_file(keyword, text, "Wiki")
            print(f"Saved details for {keyword}")
        else:
            print(f"Could not find details for {keyword}")
        click_through_links(driver, keyword)
    driver.quit()

if __name__ == "__main__":
    main()
