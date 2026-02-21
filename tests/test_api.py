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
