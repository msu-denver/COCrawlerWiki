import json
import os
from urllib.parse import urlparse, urljoin
import re
import time
from bs4 import BeautifulSoup
import requests
import copy
from queue import PriorityQueue  # For managing links with priorities

class WikipediaPage:
    def __init__(self, url):
        self.url = url
        self.title = ""
        self.html = ""
        self.table_of_contents = []
        self.graphics = []
        self.paragraphs = []
        self.links = []

    def store_as_text(self, directory):
        sanitized_title = re.sub(r'[\\/*?:"<>|]', "_", self.title)  # Sanitize title for file name
        file_name = sanitized_title.replace(" ", "_") + '.txt'
        file_path = os.path.join(directory, file_name)
        try:
            with open(file_path, 'w+', encoding='utf-8') as file:
                file.write(f"Title: {self.title}\n")
                file.write(f"URL: {self.url}\n\n")
                for paragraph in self.paragraphs:
                    file.write(f"{paragraph['title']}\n{paragraph['text']}\n")
            # After storing the basic info, append the additional details
            self.append_detailed_info(file_path)
        except OSError as e:
            print(f"Error writing file {file_name}: {e}")

    def append_detailed_info(self, file_path):
        coordinates, summary = self.extract_detailed_info()
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"\nCoordinates: {coordinates}\n")
            file.write(f"Summary: {summary}\n")

    def extract_detailed_info(self):
        try:
            response = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
            if not response.ok:
                return 'Failed to fetch', 'N/A'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            geo_dec = soup.find(class_='geo-dec')
            coordinates = geo_dec.text.strip() if geo_dec else 'Coordinates not found'
            
            paragraphs = soup.find_all('p', limit=5)
            summary = ' '.join(p.text for p in paragraphs[:3]) if paragraphs else 'Summary not found'
            
            return coordinates, summary
        except Exception as e:
            return 'Scrape exception', 'Detailed info failed due to exception'

class Crawler:
    def __init__(self, max_depth, store_after_parsing=True, directory="ColoradoWikiPages"):
        self.max_depth = max_depth
        self.store_after_parsing = store_after_parsing
        self.directory = directory
        self.valid_origins = ["https://en.wikipedia.org"]
        self.wiki_page_link_pattern = re.compile(r"^/wiki/")
        self.category_link_pattern = re.compile(r"^/wiki/Category:")
        self.visited_urls = set()
        self.queued_urls = set()  # Add this line to initialize queued_urls
        self.link_queue = PriorityQueue()
        # Keywords with associated weights
        self.keywords_weights = {
            "Colorado": 5,
            "Denver": 3,
            "Rocky Mountains": 3,
            "Colorado history": 5,
            "Adams": 3,
            "El Paso": 3,
            "Jefferson": 3,
            "Arapahoe": 3,
            "Douglas": 3,
            "Larimer": 3,
            "Weld": 3,
            "Boulder": 3,
            "Pueblo": 3,
            "Mesa": 3,
            "Broomefield": 3,
            "Summit": 3,
            "Vail": 3,
            "Aspen": 3,
            "Rocky Mountain National Park": 5,
            "Mesa Verde National Park": 5,
            "Black Canyon of the Gunnison": 4,
            "Great Sand Dunes": 4,
            "Garden of the Gods": 4,
            "Pikes Peak": 4,
            "Mount Elbert": 4,
            "San Juan Mountains": 4,
            "Maroon Bells": 4,
            "Fort Collins": 3,
            "Colorado Springs": 3,
            "Lakewood": 3,
            "Aurora": 3,
            "Westminster": 3,
            "Red Rocks Amphitheatre": 4,
            "Dinosaur National Monument": 4,
            "Breckenridge": 3,
            "Telluride": 3,
            "University of Colorado Boulder": 2,
            "Colorado State University": 2,
            "University of Denver": 4,
            "Denver Broncos": 5,
            "Colorado Rockies": 5,
            "Colorado Avalanche": 5,
            "Denver Nuggets": 5,
            "Colorado River": 3,
            "Arkansas River": 3,
            "Rio Grande": 3,
            "Platte River": 3,
            "Animas River": 3,
            "Blue Mesa Reservoir": 3,
            "Grand Lake": 3,
            "Lake Dillon": 3,
            "Horsetooth Reservoir": 3,
            "Twin Lakes": 3,
            "Yampa River": 3,
            "Gunnison River": 3,
            "Poudre River": 3,
            "San Juan River": 3,
            "Bear Lake": 3,
            "Chatfield Reservoir": 3,
            "Cherry Creek Reservoir": 3,
            "Sloan's Lake": 3,
            "Steamboat Lake": 3,
            "Turquoise Lake": 3,
            "Mesa": 4,
            "Larimer": 4,
            "Weld County": 4,
            "Montezuma": 4,
            "Acascosa Lake Colorado": 4,
            "Antero Reservoir Colorado": 4,
            "Aurora Reservoir Colorado": 4,
            "Barbour Ponds Colorado": 4,
            "Barker Meadow Reservoir Colorado": 4,
            "Barr Lake Colorado": 4,
            "Bear Creek Lake Colorado": 4,
            "sustainability": 5,
            "Twin Lakes Colorado": 4,
            "San Luis Lake Colorado": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
            "": 4,
        }
        if not os.path.exists(directory):
            os.makedirs(directory)
            time.sleep(1)
        self.visited_urls = set()
        self.link_queue = PriorityQueue()  # Initialize the priority queue

    def is_valid_url(self, url):
        if any(url.endswith(ext) for ext in ['.svg', '.jpg', '.png', '.tif']):
            return False
        return True

    def download_page(self, url):
        time.sleep(1)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            print(f"Failed to download {url}: {e}")
        return None
    
    def calculate_link_relevance(self, link_url):
        relevance_score = 0
        for keyword, weight in self.keywords_weights.items():
            if keyword.lower() in link_url.lower():
                relevance_score += weight
        return relevance_score
    def normalize_url(self, url):
        url = url.lower().strip().rstrip('/')
        return url

    # Modify download_page, parse_category, and parse_page methods as necessary
    def parse_category(self, url, depth=0):
        time.sleep(1)
        if depth >= self.max_depth or url in self.visited_urls:
            return
        print(f"Parsing category: {url} at depth {depth}")
        page_content = self.download_page(url)
        if page_content is None:
            return
        soup = BeautifulSoup(page_content, 'lxml')
        links = soup.find_all('a')
        for link in links:
            link_url = link.get('href')
            if link_url and self.wiki_page_link_pattern.match(link_url) and self.is_valid_url(link_url) and link_url not in self.visited_urls:
                full_url = urljoin(url, link_url)
                self.visited_urls.add(full_url)  # Mark this URL as visited
                relevance_score = -self.calculate_link_relevance(full_url)  # Negate score for PriorityQueue
                self.link_queue.put((relevance_score, full_url))  # Add to queue with priority
                if self.category_link_pattern.match(link_url):
                    self.link_queue.put((relevance_score, full_url))  # It's a subcategory
                else:
                    self.link_queue.put((relevance_score, full_url))  # It's a regular page

    def parse_page(self, url, depth=1):
        normalized_url = self.normalize_url(url)
        if normalized_url in self.visited_urls or normalized_url in self.queued_urls or not self.is_valid_url(normalized_url):
            return
        self.queued_urls.add(normalized_url)
        print("Parsing page: ", url)
        page_content = self.download_page(url)
        if page_content is None:
            return

        soup = BeautifulSoup(page_content, 'lxml')
        page = WikipediaPage(url)

    # Initialize the title and paragraphs for storage
        page.title = soup.find(id="firstHeading").text.strip()
        page.html = str(soup)

    # Extract Wikipedia links and prioritize them
        links = soup.find_all('a')
        for link in links:
            link_url = link.get('href')
            if link_url and self.wiki_page_link_pattern.match(link_url):
                full_url = urljoin(url, link_url)
                if full_url not in self.visited_urls:
                    self.visited_urls.add(full_url)  # Mark this URL as visited
                    relevance_score = -self.calculate_link_relevance(full_url)  # Negate score for PriorityQueue
                    self.link_queue.put((relevance_score, full_url))

    # Collect paragraphs
        text_container = soup.find('div', {'class': 'mw-parser-output'})
        if text_container:
            for child in text_container.children:
                if child.name == "p" and child.text.strip():
                # Append paragraphs as a dictionary to include titles if necessary
                    page.paragraphs.append({"title": "", "text": child.text.strip()})
                elif child.name in ["h2", "h3", "h4", "h5", "h6"]:
                # This is simplified; you might want to handle sections more robustly
                    page.paragraphs.append({"title": child.text.strip(), "text": ""})

    # Save the page
        page.store_as_text(self.directory)


    def crawl(self, initial_link, depth=1):
        if depth > self.max_depth:
            return []
        self.link_queue.put((0, initial_link))  # Queue links with priority, lower scores first

        while not self.link_queue.empty():
            _, current_link = self.link_queue.get()
            print(f"Crawling: {current_link} at depth {depth}")
            if "/wiki/Category:" in current_link:
                self.parse_category(current_link, depth)
            else:
                self.parse_page(current_link, depth)

    
if __name__ == "__main__":
    crawler = Crawler(max_depth=1, store_after_parsing=True, directory="ColoradoWikiPages")
    initial_link = "https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Colorado"
    crawler.crawl(initial_link)
