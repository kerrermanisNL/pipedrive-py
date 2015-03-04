# encoding:utf-8
from schematics.exceptions import ValidationError
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
    has_pic = BooleanType()

    def __unicode__(self):
        return self.name or str(self.id)
