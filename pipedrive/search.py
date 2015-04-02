# encoding:utf-8
from base import BaseResource, PipedriveAPI, CollectionResponse, dict_to_model
from schematics.models import Model
from schematics.types import IntType, StringType

class SearchResult(Model):
    id = IntType(required=False)
    type = StringType(required=False, choices=(
        'deal', 'person', 'organization', 'product', 'file'
    ))
    result = StringType(required=False)


class SearchResource(BaseResource):
    API_ACESSOR_NAME = 'search'
    SEARCH_PATH = '/searchResults'
    SEARCH_FIELD_PATH = '/searchResults/field'

    def search_all_fields(self, term, **params):
        """Search for 'term' in all fields of all objects"""
        params['term'] = term
        response = self.send_request('GET', self.SEARCH_PATH, params, data=None)
        search_result = response.json()
        for item in search_result.get('data', []):
            item['result'] = item['title']
        return CollectionResponse(search_result, SearchResult)

    def search_single_field(self, term, field, **params):
        """Search for 'term' in a specific field of a specific type of object.
           'field' must be a DealField, OrganizationField, PersonField or 
           ProductField (all from pipedrive.fields)"""
        params.update({
            'term': term,
            'field_type': field.FIELD_PARENT_TYPE,
            'field_key': field.key,
            'return_item_ids': 1,
        })
        response = self.send_request(
            'GET', self.SEARCH_FIELD_PATH, params, data=None
        )
        search_result = response.json()
        for item in search_result.get('data', []):
            item['result'] = item[field.key]
            item['type'] = field.FIELD_PARENT_TYPE.replace('Field', '')
        return CollectionResponse(search_result, SearchResult)


PipedriveAPI.register_resource(SearchResource)
