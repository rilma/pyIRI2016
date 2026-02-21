import io
import tarfile
import tempfile
from pyiri2016.api import update
from unittest import TestCase
from unittest.mock import patch, ANY
from simple_settings import LazySettings
from parameterized import parameterized
import pathlib

SETTINGS = LazySettings("settings.settings")


class TestApiUpdate(TestCase):
    def _make_tarball(self, directory: str, filename: str) -> str:
        """Create a minimal tarball fixture with one inner file."""
        tarball_path = str(pathlib.Path(directory) / filename)
        inner_content = b"fake fortran source"
        buf = io.BytesIO(inner_content)
        buf.seek(0)
        with tarfile.open(tarball_path, "w") as tar:
            info = tarfile.TarInfo(name="inner_file.f")
            info.size = len(inner_content)
            tar.addfile(info, buf)
        return tarball_path

    @parameterized.expand(
        [
            (SETTINGS.FORTRAN_CODE_URL, SETTINGS.FORTRAN_CODE_COMPRESSED_FILE, True),
            (SETTINGS.COMMON_FILES_URL, SETTINGS.COMMON_FILES_COMPRESSED_FILE, True),
            (SETTINGS.INDICES_URL, SETTINGS.INDICES_FILES[0], False),
            (SETTINGS.INDICES_URL, SETTINGS.INDICES_FILES[1], False),
        ]
    )
    def test_retrieve(self, url: str, filename: str, is_tar: bool):
        with tempfile.TemporaryDirectory() as tmpdir:
            if is_tar:
                fake_path = self._make_tarball(tmpdir, filename)
            else:
                fake_path = str(pathlib.Path(tmpdir) / filename)
                pathlib.Path(fake_path).write_bytes(b"fake index data")

            with patch(
                "pyiri2016.api.update.wget.download", return_value=fake_path
            ) as mock_download:
                update.retrieve(url, filename, directory=tmpdir)
                mock_download.assert_called_once_with(f"{url}/{filename}", out=tmpdir, bar=ANY)

            file_count = len([f for f in pathlib.Path(tmpdir).iterdir() if f.is_file()])
            self.assertGreater(file_count, 0)

    def _make_tarball_with_traversal(self, directory: str, filename: str, member_name: str) -> str:
        """Create a tarball fixture whose sole member uses a path-traversal name."""
        tarball_path = str(pathlib.Path(directory) / filename)
        inner_content = b"malicious content"
        buf = io.BytesIO(inner_content)
        buf.seek(0)
        with tarfile.open(tarball_path, "w") as tar:
            info = tarfile.TarInfo(name=member_name)
            info.size = len(inner_content)
            tar.addfile(info, buf)
        return tarball_path

    def test_retrieve_path_traversal_raises(self):
        """A tar member that escapes the target directory must raise ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_path = self._make_tarball_with_traversal(
                tmpdir, "traversal.tar", "../malicious.txt"
            )
            with patch(
                "pyiri2016.api.update.wget.download", return_value=fake_path
            ):
                with self.assertRaises(ValueError):
                    update.retrieve("http://example.com", "traversal.tar", directory=tmpdir)

    def test_retrieve_absolute_path_in_tar_raises(self):
        """A tar member with an absolute path that escapes the target directory must raise ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_path = self._make_tarball_with_traversal(
                tmpdir, "absolute.tar", "/etc/passwd"
            )
            with patch(
                "pyiri2016.api.update.wget.download", return_value=fake_path
            ):
                with self.assertRaises(ValueError):
                    update.retrieve("http://example.com", "absolute.tar", directory=tmpdir)
