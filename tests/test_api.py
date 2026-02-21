import tempfile
from pyiri2016.api import update
from unittest import TestCase
from simple_settings import LazySettings
from parameterized import parameterized
import pathlib

SETTINGS = LazySettings("settings.settings")


class TestApiUpdate(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary_directory = tempfile.TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.temporary_directory.cleanup()

    def _count_files(self, directory: str) -> int:
        return len([fname for fname in pathlib.Path(directory).iterdir() if fname.is_file()])

    @parameterized.expand(
        [
            (SETTINGS.FORTRAN_CODE_URL, SETTINGS.FORTRAN_CODE_COMPRESSED_FILE),
            (SETTINGS.COMMON_FILES_URL, SETTINGS.COMMON_FILES_COMPRESSED_FILE),
            (SETTINGS.INDICES_URL, SETTINGS.INDICES_FILES[0]),
            (SETTINGS.INDICES_URL, SETTINGS.INDICES_FILES[1]),
        ]
    )
    def test_retrieve(self, url: str, filename: str):
        update.retrieve(url, filename, directory=self.temporary_directory.name)
        self.assertGreater(self._count_files(self.temporary_directory.name), 0)
