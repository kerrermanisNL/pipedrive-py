# encoding:utf-8
from schematics.exceptions import ValidationError
from base import BaseResource, PipedriveAPI, CollectionResponse, dict_to_model
from schematics.models import Model
from schematics.types import (
    StringType, IntType, DecimalType, DateTimeType
)
from schematics.types.compound import ListType
from types import PipedriveDateTime, PipedriveModelType
from user import User
# from person import Person
from organization import Organization
from stage import Stage

class Deal(Model):
    title = StringType(required=True)
    id = IntType(required=False)
    value = DecimalType(required=False)
    currency = StringType(required=False)
    user_id = PipedriveModelType(User, required=False)
    # person_id = PipedriveModelType(Person, required=False)
    org_id = PipedriveModelType(Organization, required=False)
    stage_id = PipedriveModelType(Stage, required=False)
    status = StringType(required=False, choices=('open','won','lost','deleted'))
    lost_reson = StringType(required=False)
    add_time = PipedriveDateTime(required=False)
    visible_to = ListType(IntType)


class DealResource(BaseResource):
    API_ACESSOR_NAME = 'deal'
    LIST_REQ_PATH = '/deals'
    DETAIL_REQ_PATH = '/deals/{id}'
    FIND_REQ_PATH = '/deals/find'

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return Deal(raw_input(response.json))

    def create(self, deal):
        response = self._create(data=deal.to_native())
        return dict_to_model(response.json()['data'], Deal)

    def list(self):
        return CollectionResponse(self._list(), Deal)

    def find(self, term):
        return CollectionResponse(self._find(term), Deal)

PipedriveAPI.register_resource(DealResource)
