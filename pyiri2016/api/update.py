import wget
import tarfile
import os


def retrieve(url: str, filename: str, directory: str) -> None:
    retrieved_fullpath = wget.download(f"{url}/{filename}", out=directory, bar=wget.bar_thermometer)
    if tarfile.is_tarfile(retrieved_fullpath):
        with tarfile.open(retrieved_fullpath) as tar:

            def is_within_directory(directory, target):

                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)

                return os.path.commonpath([abs_directory, abs_target]) == abs_directory

            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):

                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise ValueError("Attempted Path Traversal in Tar File")

                tar.extractall(path, members, numeric_owner=numeric_owner)

            safe_extract(tar, path=directory)
        os.remove(retrieved_fullpath)
    return None
