# encoding:utf-8
from base import BaseResource, CollectionResponse, PipedriveAPI, dict_to_model
from schematics.models import Model
from schematics.types import (
    StringType, IntType, DateTimeType
)
from types import PipedriveDate, PipedriveTime, PipedriveDateTime


class Activity(Model):
    subject = StringType(required=True)
    type = StringType(required=True)
    id = IntType(required=False)
    duration = PipedriveTime(required=False)
    user_id = IntType(required=False)
    deal_id = IntType(required=False)
    person_id = IntType(required=False)
    org_id = IntType(required=False)
    note = StringType(required=False)
    due_date = PipedriveDate(required=False)


class ActivityResource(BaseResource):
    API_ACESSOR_NAME = 'activity'
    LIST_REQ_PATH = '/activities'
    DETAIL_REQ_PATH = '/activities/{id}'

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return Activity(raw_input(response.json))

    def create(self, deal):
        response = self._create(data=deal.to_native())
        return dict_to_model(response.json()['data'], Activity)

    def list(self):
        return CollectionResponse(self._list(), Activity)
    
PipedriveAPI.register_resource(ActivityResource)
