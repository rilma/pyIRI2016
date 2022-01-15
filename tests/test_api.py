import tempfile
from pyiri2016.api import update
from unittest import TestCase
from simple_settings import LazySettings

class TestApiUpdate(TestCase):        

    @classmethod
    def setUpClass(cls):
        cls.temporary_directory = tempfile.TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.temporary_directory.cleanup()

    def test_retrieve(self):
        settings = LazySettings('settings.settings')
        result = update.retrieve(settings.FORTRAN_SOURCE_CODE_URL, settings.FILENAME_REGEX_PATTERN, self.temporary_directory.name)
        self.assertIsNotNone(result)
    