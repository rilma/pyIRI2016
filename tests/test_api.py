from pyiri2016.api import update
from unittest import TestCase
from simple_settings import LazySettings

class TestApiUpdate(TestCase):        

    def test_retrieve(self):
        settings = LazySettings('settings.settings')
        result = update.retrieve(settings.FORTRAN_SOURCE_CODE_URL)
        self.assertIsNotNone(result)
    