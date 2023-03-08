import requests
from datetime import datetime
from urllib.parse import urlparse
import hashlib
from bs4 import BeautifulSoup
from loguru import logger

from database import database as DB
from database.source import Source
from database.urls import UnenrichedUrl, EnrichedUrl
from database.keywords import Keyword


class EnrichedDataIngestor:
    def __init__(self):
        pass
    def run(self, enriched_data):
        #ingests enriched data into the database
        #enriched_data is a list of dictionaries

        with DB.atomic():
            for url_dict in enriched_data:
                EnrichedUrl.create(**url_dict)

class EnrichmentScraperBase:
    def __init__(self):
        
        self.proxy = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
        }
        self.session = requests.Session()
        self.session.proxies = self.proxy
        self.session.headers = self.headers
        self.Ingestor = EnrichedDataIngestor()

    

class UrlEnricher(EnrichmentScraperBase):
    def __init__(self):
        super().__init__()
    
    def _enrich_url(self, url):
        #fetches data for a given url and saves it to the enriched_urls table
        #if url is already in the enriched_urls table, it is skipped
        
        response = self.session.get(url.link)
        soup = BeautifulSoup(response.text.replace('\n', ""), "html.parser")

        url_data = self._build_url_data(url, soup)

        return url_data

    def _get_media_uri(self, soup):
        #gets the media uri for a given url
        #media url are all the urls that either point to an image or a video or a file

        media_uri = []
        for link in soup.find_all('a'):
            if link.has_attr('href'):
                if link['href'].startswith('http'):
                    media_uri.append(link['href'])
        
        return media_uri
    def _get_keywords(self, soup):
        #gets all the words that might be keywords for a given page
        #these keywords can be used to search for the page in the future

        keywords = []
        
        return keywords



    def _build_url_data(self,url,soup):
        #builds a dictionary of data for a given url
        #this data is then used to create an entry in the enriched_urls table
        
        url_data = {}
        url_data['url'] = url
        url_data['effective_url'] = urlparse(url.link).netloc
        url_data['url_hash'] = hashlib.md5(url.link)
        url_data['contents'] = soup
        url_data['media_uri'] = "|".join(self._get_media_uri(soup))
        url_data['keywords'] = "|".join(self._get_keywords(soup))
        url_data['added_on'] = datetime.now()
        
        return url_data

    def run(self, urls):
        #runs the enrichment process for a given list of urls
        #if a url is already in the enriched_urls table, it is skipped
        enrichment_data = []
        for url in urls:
            try:
                EnrichedUrl.get(EnrichedUrl.url == url)
            except EnrichedUrl.DoesNotExist:
                try:
                    url_data = self._enrich_url(url)
                    enrichment_data.append(url_data)
                    logger.debug(f"Enriched url: {url.link}")
                except Exception as e:
                    logger.error(f"Failed to enrich url: {url.link} | {e}")
        logger.info(f"Enriched {len(enrichment_data)} urls")
        self.Ingestor.run(enrichment_data)
        logger.success(f"Enriched data ingested")
