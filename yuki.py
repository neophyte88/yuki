from core.scrapers.source_scrapers import AhamiaScraper
from database import create_tables
from colorama import Fore, Back, Style

from core.scrapers.enrichment_scrapers import UrlEnricher
from database.urls import UnenrichedUrl

import click
from commands.url_ingest import url_ingest
from commands.url_enrich import url_enrich

print(Fore.CYAN+ '/====================================================================\ '+'''
|                               888      d8b                         |
|                               888      Y8P                         |
|                               888                                  |
|             888  888 888  888 888  888 888                         |
|             888  888 888  888 888 .88P 888                         |
|             888  888 888  888 888888K  888                         |
|             Y88b 888 Y88b 888 888 "88b 888                         |
|              "Y88888  "Y88888 888  888 888                         |
|                  888                                               |
|            Y8b d88P"'''+Fore.RED+"""   ユキ- A tor indexing engine by: @neophyte88"""+Fore.CYAN+" |\n"
+ '\====================================================================/'
)

# test = AhamiaScraper()
# test.run()

# test = UrlEnricher()
# urls = UnenrichedUrl.select()
# test.run(urls)



@click.group()
def main():
    """ユキ - Yuki"""

if __name__ == '__main__':
    main.add_command(url_ingest)
    main.add_command(url_enrich)
    main()