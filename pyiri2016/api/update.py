import wget
import tarfile
import os

def retrieve(url: str, filename: str, directory: str) -> None:
    retrieved_fullpath = wget.download(f'{url}/{filename}', out=directory, bar=wget.bar_thermometer)
    if tarfile.is_tarfile(retrieved_fullpath):
        with tarfile.open(retrieved_fullpath) as tar:
            tar.extractall(path=directory)
        os.remove(retrieved_fullpath)
    return None
