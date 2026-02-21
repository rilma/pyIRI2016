import wget
import tarfile
import os


def retrieve(url: str, filename: str, directory: str) -> None:
    retrieved_fullpath = wget.download(f"{url}/{filename}", out=directory, bar=wget.bar_thermometer)
    if tarfile.is_tarfile(retrieved_fullpath):
        with tarfile.open(retrieved_fullpath) as tar:

            def is_within_directory(base_dir, target):

                abs_directory = os.path.abspath(base_dir)
                abs_target = os.path.abspath(target)

                try:
                    return os.path.commonpath([abs_directory, abs_target]) == abs_directory
                except ValueError:
                    return False

            def safe_extract(tar, path=".", *, numeric_owner=False):

                # Use the built-in extraction filter when available (Python >=3.11.4 / >=3.12)
                if hasattr(tarfile, "data_filter"):
                    # Check for unsafe members before extraction
                    for member in tar.getmembers():
                        # Reject absolute paths
                        if os.path.isabs(member.name):
                            raise ValueError(f"Unsafe tar member with absolute path: {member.name}")
                        # Reject symlinks, hardlinks and special files
                        if member.issym() or member.islnk() or member.isdev():
                            raise ValueError(f"Unsafe tar member type: {member.name}")

                    try:
                        tar.extractall(
                            path, numeric_owner=numeric_owner, filter=tarfile.data_filter
                        )
                    except tarfile.TarError as e:
                        raise ValueError(f"Unsafe tar member: {e}") from e
                    return

                safe_members = []
                for member in tar.getmembers():
                    # Reject symlinks, hardlinks and special files to prevent
                    # escape-via-link attacks even when the path looks safe.
                    if member.issym() or member.islnk() or member.isdev():
                        raise ValueError(f"Unsafe tar member type: {member.name}")
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise ValueError("Attempted Path Traversal in Tar File")
                    safe_members.append(member)

                tar.extractall(path, safe_members, numeric_owner=numeric_owner)

            safe_extract(tar, path=directory)
        os.remove(retrieved_fullpath)
