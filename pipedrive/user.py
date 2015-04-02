# encoding:utf-8
from base import BaseResource, PipedriveAPI, CollectionResponse, dict_to_model
from schematics.models import Model
from schematics.types import (
    StringType, IntType, DecimalType, DateTimeType,
    EmailType, BooleanType)
from schematics.types.compound import ListType
from types import PipedriveDateTime


class User(Model):
    id = IntType(required=True)
    name = StringType()
    email = EmailType()
    active_flag = IntType(choices=(0,1), default=0)
    has_pic = BooleanType()

    def __unicode__(self):
        return self.name or str(self.id)


class UserResource(BaseResource):
    MODEL_CLASS = User
    API_ACESSOR_NAME = 'user'
    LIST_REQ_PATH = '/users'
    DETAIL_REQ_PATH = '/users/{id}'
    FIND_REQ_PATH = '/users/find'

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return self.MODEL_CLASS(raw_input(response.json))

    def create(self, user):
        response = self._create(data=user.to_primitive())
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def list(self, **params):
        return CollectionResponse(self._list(params=params), self.MODEL_CLASS)

    def find(self, term, **params):
        return CollectionResponse(self._find(term, params=params), self.MODEL_CLASS)

PipedriveAPI.register_resource(UserResource)
