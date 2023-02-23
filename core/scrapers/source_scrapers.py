#Source scrapers to get urls from source websites and upload urls to database
#Sources are tor search engines 
#Scrapers will work using tor proxy, requests and beautifulsoup

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database.source import Source
from database.urls import RawUrl
from database.keywords import Keyword
from database import database as DB
class SourceScraper:
    def __init__(self, url):
        self.url = url
        self.proxy = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
        }
        self.session = requests.Session()
        self.session.proxies = self.proxy
        self.session.headers = self.headers

class RawUrlIngestor:
    def __init__(self):
        pass

    def ingest(self, urls, source):
        #creates raw url entries in the raw_urls table if url does not exist for a given source, using db.atomic() to ensure that all urls are added to the database
        with DB.atomic():
            for link in urls:
                try:
                    RawUrl.get(RawUrl.url == link, RawUrl.source == source)
                except RawUrl.DoesNotExist:
                    data_dict = {
                        "url": link,
                        "source": source,
                        "added_on": datetime.now()
                    }
                    print(data_dict)
                    entry = RawUrl(**data_dict)
                    entry.save()


class AhamiaScraper(SourceScraper):
    def __init__(self):
        self.Source = Source.get(Source.label == "Ahamia")
        self.url = self.Source.url
        self.url_suffix = "/search/?q="
        self.name = self.Source.label
        super().__init__(self.url)
    
    
    #get urls method for ahamia scraper will use the search query to get urls from ahamia using url_suffix, keywords will be appended to the url
    #keywords are taken from the keywords table
    def get_urls(self):
        urls = []
        keywords = Keyword.select()
        for keyword in keywords:
            url = self.url + self.url_suffix + keyword.label
            urls.append(url)
        return urls
    #scrape method will use the get_urls method to get urls and scrape them using beautifulsoup then return the scraped urls
    def sanitize(self, urls):
        #sanitize urls by removing duplicates and non url strings
        #sanitizing urls will be done by removing duplicates and non url strings, non url strings can be identified by the presence of a dot in the url, http or https, .onion
        sanitized_urls = []
        for url in urls:
            if url not in sanitized_urls:
                if url.startswith("http") or ".onion" in url:
                    if "redirect_url=" in url:
                        sanitized_urls.append(url.split("redirect_url=")[1])
                    else:
                        sanitized_urls.append(url)
        return sanitized_urls
    
    def scrape(self):
        urls = self.get_urls()
        scraped_urls = []
        for url in urls:
            response = self.session.get(url)
            soup = BeautifulSoup(response.text.replace('\n', ""), "html.parser")
            for link in soup.find_all("a"):
                scraped_urls.append(link.get("href"))

        return self.sanitize(scraped_urls)
    
    def run(self):
        scraped_urls = self.scrape()
        RawUrlIngestor().ingest(scraped_urls[::-1][:5], self.Source)
        print("Scraped {} urls from {}".format(len(scraped_urls), self.name))