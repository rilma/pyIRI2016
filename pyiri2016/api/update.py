import re
from typing import List
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import wget

def _get_links(url: str, pattern: str=r'.') -> List[str]:
    html_page = urlopen(Request(url))
    soup = BeautifulSoup(html_page, "html.parser")
    links = [link.get('href') for link in soup.findAll('a') if re.match(pattern, link.get('href'), re.DOTALL)]
    return links

def retrieve(url: str, pattern: str, directory: str) -> None:
    links = _get_links(url, pattern=pattern)
    # from pprint import pprint
    print(links)
    print(len(links))
    for link in links:
        filename = wget.download(f'{url}{link}', out=directory, bar=wget.bar_thermometer)
        print('\n', filename)
        break
    return None
    # re.match(r'[a-z0-9_]+.[a-z]+'