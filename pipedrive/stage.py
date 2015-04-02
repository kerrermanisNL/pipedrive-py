# encoding:utf-8
from base import BaseResource, PipedriveAPI, CollectionResponse, dict_to_model
from schematics.models import Model
from schematics.types import StringType, IntType, FloatType
from types import PipedriveModelType
from pipeline import Pipeline


class Stage(Model):
    """Represents a stage in a pipeline"""
    id = IntType(required=False)
    name = StringType(required=True)
    pipeline_id = PipedriveModelType(Pipeline, required=True)
    deal_probability = FloatType(required=False)
    rotten_flag = IntType(required=False, choices=(0,1))
    rotten_days = IntType(required=False)
    order_nr = IntType(required=False, min_value=0)


class StageResource(BaseResource):
    MODEL_CLASS = Stage
    API_ACESSOR_NAME = 'stage'
    LIST_REQ_PATH = '/stages'
    DETAIL_REQ_PATH = '/stages/{id}'

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return self.MODEL_CLASS(raw_input(response.json))

    def create(self, stage):
        response = self._create(data=stage.to_primitive())
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def list(self, **params):
        return CollectionResponse(self._list(params=params), self.MODEL_CLASS)

    def stages_of_pipeline(self, pipeline, **params):
        params['pipeline_id'] = pipeline.id
        return CollectionResponse(self._list(params=params), self.MODEL_CLASS)


PipedriveAPI.register_resource(StageResource)
