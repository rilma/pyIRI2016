import tempfile
from pyiri2016.api import update
from unittest import TestCase
from simple_settings import LazySettings

class TestApiUpdate(TestCase):        

    @classmethod
    def setUpClass(cls):
        cls.settings = LazySettings('settings.settings')
        cls.temporary_directory = tempfile.TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.temporary_directory.cleanup()

    def test_retrieve_code(self):
        result = update.retrieve_code(url=self.settings.FORTRAN_CODE_URL, compressed_filename=self.settings.FORTRAN_CODE_COMPRESSED_FILE, directory=self.temporary_directory.name)
        # import os; os.system(f'ls -lah {self.temporary_directory.name}')
        self.assertIsNone(result)

    # def test_retrieve(self):
    #     settings = LazySettings('settings.settings')
    #     result = update.retrieve(settings.FORTRAN_CODE_URL, settings.FILENAME_REGEX_PATTERN, self.temporary_directory.name)
    #     import os; os.system(f'ls -lah {self.temporary_directory.name}')
    #     self.assertIsNotNone(result)
    