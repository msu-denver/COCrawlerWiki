import os
import requests
from bs4 import BeautifulSoup

# Define the directory containing the files you want to crawl
directory_path = 'S:\\Web_Crawler\\ColoradoWikiPages'  

# Function to fetch and parse the HTML to extract coordinates
def extract_coordinates(url):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        geo_dec = soup.find(class_='geo-dec') # geo-dec is the class Wiki uses to store these
        if geo_dec:
            return geo_dec.get_text().strip()
        else:
            return 'Coordinates not found'
    else:
        return 'Failed to fetch page'

# Function to process each file
def process_file(file_path):
    url = None
    
    # Use encoding='utf-8' to properly handle a wide range of characters, errors without this
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith("URL:"):
                url = line.strip().split("URL: ")[1]
                break
    
    if url:
        coordinates = extract_coordinates(url)
        
        with open(file_path, 'a', encoding='utf-8') as file: 
            # Also specify encoding here
            file.write('\nCoordinates: ' + coordinates)
    else:
        print(f"No URL found in {file_path}")

# Main script execution
if __name__ == "__main__":
    # Iterate over each file in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):  # Process only text files, you can change this to process others
            file_path = os.path.join(directory_path, filename)
            process_file(file_path)
            print(f'Coordinates extracted and saved to {file_path}')
