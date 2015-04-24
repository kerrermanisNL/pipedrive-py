# encoding:utf-8
from schematics.types import StringType, IntType
from schematics.types.compound import ListType, ModelType
from schematics.models import Model
from base import BaseResource, PipedriveAPI, CollectionResponse, dict_to_model


# Generic classes for fields and their resources
class FieldOption(Model):
    id = StringType(required=False)
    label = StringType(required=True)


class FieldModel(Model):
    id = IntType(required=False)
    key = StringType(required=False)
    name = StringType(required=True)
    field_type = StringType(required=True, choices=(
        'varchar', 'varchar_auto', 'text', 'double', 'monetary', 'date', 'set',
        'enum', 'user', 'org', 'people', 'phone', 'time', 'timerange',
        'daterange'
    ))
    options = ListType(ModelType(FieldOption))


class FieldResource(BaseResource):
    FIELD_CLASS = FieldModel

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return self.FIELD_CLASS(raw_input(response.json()))

    def create(self, field):
        data = field.to_native()
        # When creating a Field in Pipedrive, the 'options' field is not a list
        # of FieldOption dictionaries, but instead a list of strings
        # representing the options' labels - so once again, we need to put a
        # square peg in a round hole
        # https://www.youtube.com/watch?v=C2YZnTL596Q
        if data['options']:
            data['options'] = [op['label'] for op in data['options']]
        response = self._create(data=data)
        return dict_to_model(response.json().get('data', {}) or {}, self.FIELD_CLASS)

    def list(self, **params):
        return CollectionResponse(self._list(params=params), self.FIELD_CLASS)


# Specific classes for fields and their resources
class DealField(FieldModel):
    FIELD_PARENT_TYPE = 'dealField'


class OrganizationField(FieldModel):
    FIELD_PARENT_TYPE = 'organizationField'


class PersonField(FieldModel):
    FIELD_PARENT_TYPE = 'personField'


class ProductField(FieldModel):
    FIELD_PARENT_TYPE = 'productField'


class DealFieldResource(FieldResource):
    FIELD_CLASS = DealField
    API_ACESSOR_NAME = 'dealField'
    LIST_REQ_PATH = '/dealFields'
    DETAIL_REQ_PATH = '/dealFields/{id}'


class OrganizationFieldResource(FieldResource):
    FIELD_CLASS = OrganizationField
    API_ACESSOR_NAME = 'organizationField'
    LIST_REQ_PATH = '/organizationFields'
    DETAIL_REQ_PATH = '/organizationFields/{id}'


class PersonFieldResource(FieldResource):
    FIELD_CLASS = PersonField
    API_ACESSOR_NAME = 'personField'
    LIST_REQ_PATH = '/personFields'
    DETAIL_REQ_PATH = '/personFields/{id}'


class ProductFieldResource(FieldResource):
    FIELD_CLASS = ProductField
    API_ACESSOR_NAME = 'productField'
    LIST_REQ_PATH = '/productFields'
    DETAIL_REQ_PATH = '/productFields/{id}'


PipedriveAPI.register_resource(DealFieldResource)
PipedriveAPI.register_resource(OrganizationFieldResource)
PipedriveAPI.register_resource(PersonFieldResource)
PipedriveAPI.register_resource(ProductFieldResource)
