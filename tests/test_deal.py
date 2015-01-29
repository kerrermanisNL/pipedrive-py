from __future__ import absolute_import
from unittest import TestCase
from schematics.exceptions import ValidationError
from pipedrive.base import dict_to_model
from pipedrive.deal import Deal
from pipedrive.user import User
from utils import get_test_data


class DealModelTest(TestCase):
    def test_required(self):
        deal = Deal()
        self.assertRaises(ValidationError, deal.validate, [])

    def test_title_only(self):
        deal = Deal(raw_data={'title': 'Hello!'})
        self.assertIsNone(deal.validate())

    def test_nested_user(self):
        data = get_test_data('deal-detail.json')
        model = dict_to_model(data, Deal)
        self.assertTrue(isinstance(model.user, User))
