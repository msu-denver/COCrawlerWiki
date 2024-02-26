import os
from bs4 import BeautifulSoup
import requests
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import re


words_to_emphasize = [
    # Colorado Specific
    "Colorado", "Denver", "Boulder", "Aspen", "Telluride", "Vail", "Breckenridge", "Rocky Mountains", "Adams", "Alamosa", "Arapahoe", "Archuleta", "Baca", "Bent", "Boulder", "Broomfield", "Chaffee", "Cheyenne", "Clear Creek", "Conejos", "Costilla", "Crowley", "Custer", "Delta", "Denver", "Dolores", "Douglas", "Eagle", "El Paso", "Elbert", "Fremont", "Garfield", "Gilpin", "Grand", "Gunnison", "Hinsdale", "Huerfano", "Jackson", "Jefferson", "Kiowa", "Kit Carson", "La Plata", "Lake", "Larimer", "Las Animas", "Lincoln", "Logan", "Mesa", "Mineral", "Moffat", "Montezuma", "Montrose", "Morgan", "Otero", "Ouray", "Park", "Phillips", "Pitkin", "Prowers", "Pueblo", "Rio Blanco", "Rio Grande", "Routt", "Saguache", "San Juan", "San Miguel", "Sedgwick", "Summit", "Teller", "Washington", "Weld", "Yuma", 

    # Parks
    "Rocky Mountain National Park", "Great Sand Dunes National Park", "Mesa Verde National Park", "Black Canyon of the Gunnison National Park", "Garden of the Gods", "Maroon Bells",

    # Cities and Towns 
    "Colorado Springs", "Fort Collins", "Steamboat Springs", "Durango", "Pueblo", "Grand Junction",  "Frisco", "Glenwood Springs", "Silverton", 

    # Counties
    "El Paso", "Arapahoe", "Jefferson", "Adams", "Larimer", "Weld", "Douglas", "Eagle", "Summit", "Mesa",
    
    #Lakes
    "Acascosa Lake", "Antero Reservoir", "Aurora Reservoir",
    "Barbour Ponds", "Barker Meadow Reservoir", "Barr Lake",
    "Bear Creek Lake", "Big Soda Lake", "Bierstadt Lake",
    "Bison Reservoir", "Blue Mesa Reservoir", "Bonham Reservoir",
    "Boulder Reservoir", "Boyd Lake", "Carter Lake",
    "Chambers Lake", "Chatfield Reservoir", "City Park Lake",
    "Cherry Creek Reservoir", "Clear Creek Reservoir", "Clinton Gulch Dam Reservoir",
    "Crater Lake", "Cheesman Reservoir", "Crawford Reservoir",
    "Crystal Creek Reservoir", "Crystal Reservoir", "Dawson Reservoir",
    "Deep Lake", "Deep Ward Lake", "Delaney Butte Reservoir",
    "DeWeese Reservoir", "Dillon Reservoir", "Dream Lake",
    "East Portal Reservoir", "Echo Lake", "Eleven Mile Reservoir",
    "Elkhead Reservoir", "Emmaline Lake", "Emerald Lake",
    "Lake Estes", "Fern Lake", "Flatiron Reservoir",
    "Fruitgrowers Reservoir", "Grand Lake", "Grass Valley Reservoir",
    "Green Mountain Reservoir", "Gross Reservoir", "Hanging Lake",
    "Harker Park Lake", "Harvey Gap Reservoir", "Haynach Lakes",
    "Horsetooth Reservoir", "Jackson Gulch Reservoir", "Jefferson Lake",
    "Jackson Lake", "John Martin Reservoir", "Kenney Reservoir",
    "La Jara Reservoir", "Lake Avery", "Lake Dillon",
    "Lake George", "Lake Granby", "Lake Isabel",
    "Lake John", "Lake Loveland", "Lake Meredith",
    "Lake Pueblo", "Lake Maloya", "Lake Rhoda",
    "Lake San Cristobal", "Lemon Reservoir", "Lizard Lake",
    "Maroon Lake", "Marston Lake", "Marys Lake",
    "McPhee Reservoir", "Meadow Creek Reservoir", "Miramonte Reservoir",
    "Monarch Lake", "Montgomery Reservoir", "Morrow Point Reservoir",
    "Mount Elbert Forebay", "Mountain Home Reservoir", "Murphy Lake",
    "Navajo Reservoir", "North Michigan Creek Reservoir", "OHaver Lake",
    "Pacific Tarn", "Paonia Reservoir", "Pearl Lake",
    "Pinewood Lake", "Platoro Reservoir", "Poudre Lake",
    "Pueblo Reservoir", "Quincy Reservoir", "Ralph White Lake",
    "Ralston Reservoir", "Rampart Reservoir", "Ridgway Reservoir",
    "Rifle Gap Reservoir", "Ruedi Reservoir", "Rueter–Hess Reservoir",
    "Runyon Lake", "San Luis Lake", "Sanchez Reservoir",
    "Seaman Reservoir", "Shadow Mountain Lake", "Silver Jack Reservoir",
    "Sloans Lake", "Smith Lake", "Smith Reservoir",
    "Snowdrift Lake", "Stagecoach Reservoir", "Standley Lake",
    "Stapp Lakes", "Steamboat Lake", "Strontia Springs Reservoir",
    "Sweitzer Lake", "Summit Lake", "Sylvan Lake",
    "Taylor Park Reservoir", "Terrace Reservoir", "Trappers Lake",
    "Trinidad Lake", "Turquoise Lake", "Twin Lakes",
    "Vallecito Reservoir", "Vega Reservoir", "Williams Creek Reservoir",
    "Williams Fork Reservoir", "Willow Creek Reservoir", "Windy Gap Reservoir",
    "Wolford Mountain Reservoir",
    # Nature 
    "mountains","sustainability","air quality","water","green initiatives", "rivers", "lakes", "forests", "trails", "wildlife", "elk", "bighorn sheep", "pine", "aspen",
]   # Add more words depending on your data.
emphasis_multiplier = 5  # How much you want to boost these words
words_to_exclude = {'and','pixel','SVG','used','Click','scanner','digital', 'file', 'time','or','modified','KB','Original','view','appeared', 'but', 'if', 'in', 'at', 'by', 'for', 'with', 'about', 'the', 'of'}  # Add words to exclude

def extract_text_from_url(url):
    try:
        print(f"Requesting URL: {url}")  # Debug print to check the URL
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = ' '.join(s.get_text() for s in soup.find_all('p')).lower()
            return text
        else:
            print(f"Failed to access {url}, Status Code: {response.status_code}")
            return ""
    except Exception as e:
        print(f"Error extracting data from {url}: {e}")
        return ""

def generate_word_cloud(text, title='Word Cloud'):
    custom_stopwords = STOPWORDS.union(set(words_to_exclude))
    wordcloud = WordCloud(
        width=1600, height=800, collocations=False, background_color='black', stopwords=custom_stopwords, max_words=1000).generate(text)
    plt.figure(figsize=(16, 9), facecolor=None)
    plt.imshow(wordcloud, interpolation="bilinear")  # Use bilinear interpolation for a smoother appearance
    plt.axis("off")
    plt.title(title)
    plt.tight_layout(pad=0)
    plt.show()

folder_path = 'S:\\Web_Crawler\\ColoradoWikiPages'  # Update this path to your actual folder path
all_text = ""

for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                # Correctly extract the URL, removing any "URL: " prefix if present
                url = lines[1].strip()
                if url.startswith("URL: "):
                    url = url.replace("URL: ", "").strip()  # Remove "URL: " if present
                print(f"Extracting from: {url}")  # Corrected to debug print
                text = extract_text_from_url(url)
                for word in words_to_emphasize:
                    text += (" " + word) * emphasis_multiplier
                all_text += text + " "

if all_text:
    generate_word_cloud(all_text, title='Colorado Content Word Cloud')
else:
    print("No text was aggregated for word cloud generation.")
