import urllib3
from bs4 import BeautifulSoup


def retrieve_raw_site_contents(site: str) -> BeautifulSoup:
    http = urllib3.PoolManager()
    response = http.request('GET', site)
    soup = BeautifulSoup(response.data, features="html.parser")
    return soup