import os
import requests
from bs4 import BeautifulSoup

# Set the directory path where your text files are stored
directory_path = 'S:\\Web_Crawler\\ColoradoWikiPages'  # Update this with the actual path to your directory

def extract_detailed_info(url):
    """
    Extracts detailed information from a given URL using web scraping.
    
    :param url: The URL from which to scrape information.
    :return: A tuple containing the coordinates, an infobox dictionary with key-value pairs, and the article summary.
    """
    try:
        # Send a GET request to the URL with a custom User-Agent header
        response = requests.get(url, headers={'User-Agent': 'Thedude3000'})
        
        # Check if the request was successful
        if not response.ok:
            return 'Failed to fetch', {}, 'N/A'
        
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract coordinates
        geo_dec = soup.find(class_='geo-dec')
        coordinates = geo_dec.get_text().strip() if geo_dec else 'Coordinates not found'

        # Extract information from the infobox
        infobox = {i.find_previous_sibling('th').text: i.text for i in soup.select('.infobox-data') if i.find_previous_sibling('th')}

        # Extract the first five paragraphs as the article summary
        article_summary = ' '.join(p.get_text(strip=True) for p in soup.find_all('p', limit=5)) if soup.find_all('p', limit=4) else 'Summary not found.'

        return coordinates, infobox, article_summary
    except Exception as e:
        # Return a default value in case of an exception
        return 'Scrape exception', {}, 'Detailed info failed due to exception'

def process_file(file_path):
    """
    Processes each text file to extract a URL, scrape the web page at that URL, and append the scraped data to the file.
    
    :param file_path: The path to the text file to process.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read lines from the file to find the URL
        for line in file:
            if line.startswith("URL:"):
                url = line.strip().split("URL: ")[1]
                break
        else:
            # If no URL is found, print a message and exit the function
            print(f"No URL found in {file_path}")
            return
    
    # Extract detailed information from the URL
    coordinates, infobox, summary = extract_detailed_info(url)
    
    # Append the scraped information to the file
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f'\n==Coordinates==\n{coordinates}\n')
        for key, value in infobox.items():
            file.write(f'\n{key}: {value}')
        file.write(f'\nSummary: “{summary}”\n')

if __name__ == "__main__":
    # Loop through all text files in the directory and process them
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            print(f'Processing {filename}...')
            file_path = os.path.join(directory_path, filename)
            process_file(file_path)


            file_path = os.path.join(directory_path, filename)
            process_file(file_path)
            print(f'Coordinates extracted and saved to {file_path}')
