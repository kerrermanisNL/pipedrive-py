# encoding:utf-8
from schematics.exceptions import ValidationError
from base import BaseResource, PipedriveAPI, CollectionResponse, dict_to_model
from schematics.models import Model
from schematics.types import (
    StringType, IntType, DecimalType, DateTimeType
)
from schematics.types.compound import ListType, ModelType
from types import PipedriveDateTime
from django.conf import settings

# PIPEDRIVE_CNPJ_FIELD_KEY = getattr(settings, 'PIPEDRIVE_CNPJ_FIELD_KEY', None)

class Organization(Model):
    id = IntType(required=False)
    name = StringType(required=False)