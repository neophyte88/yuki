import click
from core.scrapers.source_scrapers import AhamiaScraper

# Command Group
@click.group(name='ingest', help='Url Ingest related commands')
def url_ingest():
    pass

@url_ingest.command(name='run_ahamia', help='Ingest Urls from Ahamia')
def run_ahamia():
    sc = AhamiaScraper()
    sc.run()


# @cli_tools.command(name='search', help='test search')
# @click.option('--test1', default='1', help='test option')
# def search_cmd(test1):
#     click.echo('Hello world')