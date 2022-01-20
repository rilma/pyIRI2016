import re
from typing import List
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import wget
import tarfile
import os

def _get_links(url: str, pattern: str=r'.') -> List[str]:
    html_page = urlopen(Request(url))
    soup = BeautifulSoup(html_page, "html.parser")
    links = [link.get('href') for link in soup.findAll('a') if re.match(pattern, link.get('href'), re.DOTALL)]
    return links

def retrieve(url: str, filename: str, directory: str) -> None:
    retrieved_fullpath = wget.download(f'{url}/{filename}', out=directory, bar=wget.bar_thermometer)
    if tarfile.is_tarfile(retrieved_fullpath):
        with tarfile.open(retrieved_fullpath) as tar:
            tar.extractall(path=directory)
        os.remove(retrieved_fullpath)
    return None
