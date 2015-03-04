# encoding:utf-8
from schematics.exceptions import ValidationError
from base import BaseResource, PipedriveAPI, CollectionResponse, dict_to_model
from schematics.models import Model
from schematics.types import (
    StringType, IntType, DecimalType, DateTimeType
)
from schematics.types.compound import ListType, ModelType
from types import PipedriveDateTime
from user import User


class DealStatusType(StringType):
    OPEN = 'open'
    WON = 'won'
    LOST = 'lost'
    DELETED = 'deleted'
    VALID_STATUSES = (
        OPEN, WON, LOST, DELETED
    )

    def validate(self, value):
        if value not in DealStatusType.VALID_STATUSES:
                    raise ValidationError([
                        "%s is not a valid deal status" % value])


class Deal(Model):
    title = StringType(required=True)
    id = IntType(required=False)
    value = DecimalType(required=False)
    currency = StringType(required=False)
    user = ModelType(User)
    person_id = IntType(required=False)
    org_id = IntType(required=False)
    stage_id = IntType(required=False)
    status = DealStatusType(required=False)
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
