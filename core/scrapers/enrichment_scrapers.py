import requests
from datetime import datetime
from urllib.parse import urlparse
import hashlib
from bs4 import BeautifulSoup
from loguru import logger
from abc import ABC, abstractmethod

from database import database as DB
from database.source import Source
from database.urls import UnenrichedUrl, EnrichedUrl
from database.keywords import Keyword
from tbselenium.tbdriver import TorBrowserDriver
from pyvirtualdisplay import Display
from tbselenium.utils import start_xvfb, stop_xvfb

from support.text_tools import get_keywords

class EnrichedDataIngestor:
    def __init__(self):
        pass
    def run(self, enriched_data):
        #ingests enriched data into the database
        #enriched_data is a list of dictionaries

        with DB.atomic():
            for url_dict in enriched_data:
                try:
                    EnrichedUrl.create(**url_dict)
                except Exception as e:
                    logger.warning(f"Failed to ingest url | {e}")
class EnrichmentScraperBase(ABC):
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
        self.tbb_path = "/support/bin/tor-browser/"
        self.geckodriver_path = "/usr/local/bin/geckodriver"
        self.logfile_path = "/home/neophyte88/1.json"

    

class UrlEnricher(EnrichmentScraperBase):
    def __init__(self):
        super().__init__()
        # self.enrichment_data = []
        self._display = start_xvfb()
        self.base_dir = "/home/neophyte88/finalyearproject/yuki"
        self.tbb_p = "/home/neophyte88/finalyearproject/yuki/support/bin/tor-browser/"
        self.executable_p= "/usr/local/bin/geckodriver" 
        self.logfile = self.base_dir+"/logs/yuki_tbb_log.json"
    
    def _enrich_url(self, url):
        #fetches data for a given url and saves it to the enriched_urls table
        #if url is already in the enriched_urls table, it is skipped

        try:
            with TorBrowserDriver(self.tbb_p, executable_path=self.executable_p, tbb_logfile_path=self.logfile) as driver:
                
                driver.get(url.link)
                response = driver.page_source
            
            # response = self.session.get(url.link)
            soup = BeautifulSoup(response.replace('\n', ""), "html.parser")
            url_data = self._build_url_data(url, soup)

            return url_data

        except Exception as e:
            logger.error(f"Failed to enrich url: {url.link} | {e}")

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

        keywords = get_keywords(soup.get_text(), 10)

        return keywords

    def _get_url_hash(self, url):
        url_hash = hashlib.md5()
        url_hash.update(url.encode('utf-8'))
        return url_hash.hexdigest()

    def _build_url_data(self,url,soup):
        #builds a dictionary of data for a given url
        #this data is then used to create an entry in the enriched_urls table
        
        url_data = {}
        url_data['url'] = url
        url_data['effective_url'] = urlparse(url.link).netloc
        url_data['url_hash'] = self._get_url_hash(url.link) #str(hashlib.md5(url.link.encode('utf-8')))
        url_data['contents'] = soup
        url_data['media_uri'] = "|".join(self._get_media_uri(soup))
        url_data['keywords'] = "|".join(self._get_keywords(soup))
        url_data['added_on'] = datetime.now()
        
        return url_data

    def _url_breakdown(self, urls):
        #takes the list of urls and returns 2 lists, one containing urls that are already in the enriched_urls table
        #and the other containing urls that are not in the enriched_urls table
        #this is used to skip urls that have already been enriched

        enriched_urls = []
        unenriched_urls = []
        for url in urls:
            try:
                EnrichedUrl.get(EnrichedUrl.url == url)
                enriched_urls.append(url)
            except EnrichedUrl.DoesNotExist:
                unenriched_urls.append(url)
        return unenriched_urls, enriched_urls
    
    def run(self, urls, threads=5):
        #runs the enrichment process for a given list of urls
        #if a url is already in the enriched_urls table, it is skipped
        enrichment_data = []
        create, update = self._url_breakdown(urls)
        logger.info(f"Enriching {len(create)} urls")
        for url in create:
            try:
                url_data = self._enrich_url(url)
                enrichment_data.append(url_data)
                logger.debug(f"Enriched url: {url.link}")
            except Exception as e:
                logger.error(f"Failed to enrich url: {url.link} | {e}")
        

        logger.info(f"Enriched {len(enrichment_data)} urls")
        self.Ingestor.run(enrichment_data)
        logger.success(f"Enriched data ingested")
