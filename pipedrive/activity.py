# encoding:utf-8
from schematics.exceptions import ValidationError
from base import BaseResource
from schematics.models import Model
from schematics.types import (
    StringType, IntType, DateTimeType
)
from schematics.types.compound import ListType


class DealStatusType(ListType):
    OPEN = 'open'
    WON = 'won'
    LOST = 'lost'
    DELETED = 'deleted'
    VALID_STATUSES = (
        OPEN, WON, LOST, DELETED
    )

    def validate_choices(self, items):
        errors = []
        for item in items:
            try:
                self.field.validate(item)
                if item not in DealStatusType.VALID_STATUSES:
                    errors += ["%s is not a valid deal status" % item]
            except ValidationError as exc:
                errors += exc.messages

        if errors:
            raise ValidationError(errors)


class Activity(Model):
    subject = StringType(required=True)
    type = StringType(required=False)
    duration = IntType(required=False)
    user_id = IntType(required=False)
    deal_id = IntType(required=False)
    person_id = IntType(required=False)
    org_id = IntType(required=False)
    note = StringType(required=False)
    due_date = DateTimeType(required=False)


class DealResource(BaseResource):
    API_ACESSOR_NAME = 'deal'
    LIST_REQ_PATH = '/deals'
    DETAIL_REQ_PATH = '/deals/{id}'

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return Activity(raw_input(response.json))

    def create(self, deal):
        response = self._create(data=deal.to_native())
        return Activity(raw_input(response.json))

    def list(self):
        response = self._list()
        return response.json
