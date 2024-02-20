# Project Title

Colorado Crawler Wikipedia

## Description

This will crawl Wikipedia for pages related to Colorado. This is meant to be an easy way to extract data for an LLM or RAG system tailored to your keywords and weights

## Getting Started

### Dependencies
* Run 
```
pip install -r requirements.txt
```
### Installing

* Pull the REPO
  ```
  git clone https://github.com/LukeFarch/COCrawlerWiki.git
  ```
* Change the paths to match your needs

  
### Executing program

* How to run the program
```
python COCrawlerWiki.py
```
* This will visit each link in the txt file and attach coordinates to the txt file based on the info from the link. This uses the geo-dec class on wiki to scrape coordinates
```
 python GeoLocator.py 
```
* This will clean the URL's to ensure all of them can be accessed and scraped for information 
```
python Cleaner.py
```
## Authors

Contributors names and contact info
- Luke Farchione (J4eva) www.0xFarch.com

## TODO: 
- [ ] Word Cloud Analysis on the extracted pages from the wiki, will allow me to update the weights based on those results.
