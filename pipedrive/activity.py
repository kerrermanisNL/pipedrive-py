# encoding:utf-8
from base import BaseResource, CollectionResponse, PipedriveAPI, dict_to_model
from schematics.models import Model
from schematics.types import (
    StringType, IntType, DateTimeType
)
from types import PipedriveDate, PipedriveTime, PipedriveModelType
from user import User
from deal import Deal
# from person import Person
from organization import Organization
from stage import Stage


class Activity(Model):
    subject = StringType(required=True)
    done = IntType(required=False)
    type = StringType(required=True)
    id = IntType(required=False)
    duration = PipedriveTime(required=False)
    user_id = PipedriveModelType(User, required=False)
    deal_id = PipedriveModelType(Deal, required=False)
    # person_id = PipedriveModelType(Person, required=False)
    org_id = PipedriveModelType(Organization, required=False)
    note = StringType(required=False)
    due_date = PipedriveDate(required=False)


class ActivityResource(BaseResource):
    MODEL_CLASS = Activity
    API_ACESSOR_NAME = 'activity'
    LIST_REQ_PATH = '/activities'
    DETAIL_REQ_PATH = '/activities/{id}'

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return self.MODEL_CLASS(raw_input(response.json))

    def create(self, activity):
        response = self._create(data=activity.to_primitive())
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def list(self, **params):
        return CollectionResponse(self._list(params=params), self.MODEL_CLASS)
    
PipedriveAPI.register_resource(ActivityResource)
