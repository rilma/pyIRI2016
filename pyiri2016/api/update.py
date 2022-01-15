from typing import List
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

def _get_links(url: str) -> List[str]:
    request = Request(url)
    html_page = urlopen(request)
    soup = BeautifulSoup(html_page, "html.parser")
    links = [link.get('href') for link in soup.findAll('a')]
    return links

def retrieve(url: str) -> None:
    links = _get_links(url)
    return None