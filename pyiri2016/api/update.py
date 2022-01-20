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

def retrieve_code(url: str, compressed_filename: str, directory: str) -> None:
    retrieved_fullpath = wget.download(f'{url}/{compressed_filename}', out=directory, bar=wget.bar_thermometer)
    with tarfile.open(retrieved_fullpath) as tar:
        tar.extractall(path=directory)
    os.remove(retrieved_fullpath)
    
# def retrieve(url: str, compressed, pattern: str, directory: str) -> None:
#     links = _get_links(url, pattern=pattern)
#     # from pprint import pprint
#     print(links)
#     print(len(links))
#     for link in links:
#         filename = wget.download(f'{url}{link}', out=directory, bar=wget.bar_thermometer)
#         print('\n', filename)
#         # break
#     return None
#     # re.match(r'[a-z0-9_]+.[a-z]+'