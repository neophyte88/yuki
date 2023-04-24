import click
from core.scrapers.enrichment_scrapers import UrlEnricher
from database.urls import UnenrichedUrl

# Command Group
@click.group(name='enrich', help='Url Enrichment commands')
def url_enrich():
    pass

@url_enrich.command(name='run_all', help='Enriches All Unenriched Urls')
def run_all():
    enricher = UrlEnricher()
    urls = UnenrichedUrl.select()
    enricher.run(urls)
