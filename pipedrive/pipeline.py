# encoding:utf-8
from schematics.exceptions import ValidationError
from base import BaseResource, PipedriveAPI, CollectionResponse, dict_to_model
from schematics.models import Model
from schematics.types import StringType, IntType
from types import PipedriveDateTime


class Pipeline(Model):
    """Represents one of the pipelines in the Pipedrive ecosystem"""
    id = IntType(required=False)
    name = StringType(required=False)
    order_nr = IntType(required=False, min_value=0)
    active = IntType(required=False, choices=(0,1))


class PipelineResource(BaseResource):
    MODEL_CLASS = Pipeline
    API_ACESSOR_NAME = 'pipeline'
    LIST_REQ_PATH = '/pipelines'
    DETAIL_REQ_PATH = '/pipelines/{id}'

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return self.MODEL_CLASS(raw_input(response.json))

    def create(self, pipeline):
        response = self._create(data=pipeline.to_primitive())
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def list(self, **params):
        return CollectionResponse(self._list(params=params), self.MODEL_CLASS)



PipedriveAPI.register_resource(PipelineResource)
