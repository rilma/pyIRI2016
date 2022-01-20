import tempfile
from pyiri2016.api import update
from unittest import TestCase
from simple_settings import LazySettings
from parameterized import parameterized

SETTINGS = LazySettings('settings.settings')

class TestApiUpdate(TestCase):        

    @classmethod
    def setUpClass(cls):
        cls.temporary_directory = tempfile.TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.temporary_directory.cleanup()

    @parameterized.expand([
        (SETTINGS.FORTRAN_CODE_URL, SETTINGS.FORTRAN_CODE_COMPRESSED_FILE),
        (SETTINGS.COMMON_FILES_URL, SETTINGS.COMMON_FILES_COMPRESSED_FILE),
        (SETTINGS.INDICES_URL, SETTINGS.INDICES_FILES[0]),
        (SETTINGS.INDICES_URL, SETTINGS.INDICES_FILES[1]),
    ])
    def test_retrieve(self, url: str, filename: str):
        result = update.retrieve(url, filename, directory=self.temporary_directory.name)
        self.assertIsNone(result)
