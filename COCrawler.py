import json
import os
from urllib.parse import urlparse, urljoin
import re
from bs4 import BeautifulSoup
import requests
import copy

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
        # Replace invalid file name characters with an underscore or remove them
        sanitized_title = self.title.replace('"', '').replace(':', '_').replace('/', '_').replace('\\', '_').replace('|', '_').replace('?', '').replace('*', '_').replace('<', '_').replace('>', '_')
        file_name = sanitized_title.replace(" ", "_") + '.txt'
        try:
            with open(os.path.join(directory, file_name), 'w+', encoding='utf-8') as file:
                file.write(f"Title: {self.title}\n")
                file.write(f"URL: {self.url}\n\n")
                for paragraph in self.paragraphs:
                    file.write(f"{paragraph['title']}\n{paragraph['text']}\n")
        except OSError as e:
            print(f"Error writing file {file_name}: {e}")


class Crawler:
    def __init__(self, max_depth, store_after_parsing=True, directory="ColoradoWikiPages"):
        self.max_depth = max_depth
        self.store_after_parsing = store_after_parsing
        self.directory = directory
        self.valid_origins = ["https://en.wikipedia.org"]
        self.wiki_page_link_pattern = re.compile(r"^/wiki/")
        self.category_link_pattern = re.compile(r"^/wiki/Category:")
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.visited_urls = set()  # Keep track of visited URLs

    def download_page(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            print(f"Failed to download {url}: {e}")
        return None

    def parse_category(self, url, depth=0):
        """
        Parses a Wikipedia category page and recursively crawls its links.
        """
        print(f"Parsing category: {url} at depth {depth}")
        page_content = self.download_page(url)
        if page_content is None:
            return []
        soup = BeautifulSoup(page_content, 'lxml')
        links = soup.find_all('a')
        pages = []
        for link in links:
            link_url = link.get('href')
            if link_url and self.wiki_page_link_pattern.match(link_url) and not link_url in self.visited_urls:
                full_url = urljoin(url, link_url)
                self.visited_urls.add(full_url)  # Mark this URL as visited
                if self.category_link_pattern.match(link_url):
                    # It's a subcategory, parse it as a category
                    pages.extend(self.parse_category(full_url, depth + 1))
                else:
                    # It's a regular page, parse it as such
                    pages.extend(self.parse_page(full_url, depth + 1))
        return pages
    def is_colorado_related(self, content):
        """
        Checks if the content of the page contains Colorado-related keywords.
        """
        keywords = ['Colorado', 'Denver', 'Rocky Mountains', 'Boulder']
        return any(keyword in content for keyword in keywords)

    def parse_page(self, url, depth=0):
        """
        Downloads and parses a Wikipedia page and stores it if required.
        :param url:
        :return:
        """
        print("Parsing page: ", url)
        page_content = self.download_page(url)
        if page_content is None:
            return []

        soup = BeautifulSoup(page_content, 'lxml')
        pages = []
        page = WikipediaPage(url)

        # Extract Wikipedia links
        links = soup.find_all('a')
        for link in links:
            link_url = link.get('href')
            if link_url is not None and self.wiki_page_link_pattern.match(link_url):
                full_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url)) + link_url
                if full_url not in self.visited_urls:  # Check if the URL has already been visited
                    self.visited_urls.add(full_url)  # Mark this URL as visited
                    page.links.append(full_url)
                    pages.extend(self.crawl(full_url, depth + 1))

        # Extract paragraphs
        text_container = soup.find('div', {'class': 'mw-parser-output'})
        if text_container:  # Check if text_container is not None
            zero_paragraph = {"title": "", "text": ""}
            current_paragraph = copy.deepcopy(zero_paragraph)
            for child in text_container.children:
                if child.name == "p":
                    current_paragraph["text"] += child.text + "\n"
                elif child.name == "h2":
                    if current_paragraph["text"]:  # Ensure paragraph has text before appending
                        page.paragraphs.append(current_paragraph)
                    current_paragraph = copy.deepcopy(zero_paragraph)
                    current_paragraph["title"] = child.text.strip()

            if current_paragraph["text"]:  # Add the last paragraph if it has text
                page.paragraphs.append(current_paragraph)

        # Extract graphics
        image_container = soup.find_all('div', {'class': 'thumbinner'})
        zero_graphic = {"url": "", "caption": ""}
        for image in image_container:
            current_graphic = copy.deepcopy(zero_graphic)
            for child in image.children:
                if child.name == "a":
                    current_graphic["url"] = child.get('href')
                elif child.name == "div":
                    current_graphic["caption"] = child.text
            page.graphics.append(current_graphic)

        toc_element = soup.find(id="toc")
        if toc_element is not None:
            page.table_of_contents = list(filter(lambda x: x != "", toc_element.text.split("\n")[1:]))

        page.title = soup.find(id="firstHeading").text
        page.html = str(soup)

        if self.store_after_parsing:
            page.store_as_text(self.directory)
        pages.append(page)
        return pages

    
    def crawl(self, initial_link, depth=0):
        if depth > self.max_depth:
            return []
        print(f"Crawling: {initial_link} at depth {depth}")
        if "/wiki/Category:" in initial_link:
            return self.parse_category(initial_link, depth)
        else:
            return self.parse_page(initial_link, depth)

if __name__ == "__main__":
    crawler = Crawler(max_depth=2, store_after_parsing=True, directory="ColoradoWikiPages")
    initial_link = "https://en.wikipedia.org/wiki/Category:Colorado"
    crawler.crawl(initial_link)
