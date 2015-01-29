import unittest
from unittest import TestCase
from pipedrive.base import BaseResource, PipedriveAPI


class ResourceAccessorAttibute(TestCase):
    def test_registry_does_not_contain(self):
        api = PipedriveAPI('lol')
        try:
            api.lol
            raise ValueError("Should have raised an exception")
        except AttributeError:
            pass

    def test_registry_contains(self):
        BaseResource.API_ACESSOR_NAME = 'sms'
        PipedriveAPI.register_resource(BaseResource)
        api = PipedriveAPI('lol')
        self.assertEqual(BaseResource, api.sms.__class__)


if __name__ == '__main__':
    unittest.main()
