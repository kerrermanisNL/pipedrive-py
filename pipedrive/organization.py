# encoding:utf-8
from base import BaseResource, PipedriveAPI, CollectionResponse, dict_to_model
from schematics.models import Model
from schematics.types import StringType, IntType
from types import PipedriveModelType
from user import User


class Organization(Model):
    id = IntType(required=False)
    name = StringType(required=False)
    owner_id = PipedriveModelType(User, required=False)
    visible_to = IntType(required=False, choices=(0,1,2))
    address = StringType(required=False)


class OrganizationResource(BaseResource):
    MODEL_CLASS = Organization
    API_ACESSOR_NAME = 'organization'
    LIST_REQ_PATH = '/organizations'
    DETAIL_REQ_PATH = '/organizations/{id}'
    FIND_REQ_PATH = '/organizations/find'

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def create(self, organization):
        response = self._create(data=organization.to_primitive())
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def update(self, organization):
        response = self._update(organization.id, data=organization.to_primitive())
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def list(self, **params):
        return CollectionResponse(self._list(params=params), self.MODEL_CLASS)

    def find(self, term, **params):
        return CollectionResponse(self._find(term, params=params), self.MODEL_CLASS)


PipedriveAPI.register_resource(OrganizationResource)
