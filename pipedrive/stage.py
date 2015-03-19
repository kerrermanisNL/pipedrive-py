# encoding:utf-8
from base import BaseResource, PipedriveAPI, CollectionResponse, dict_to_model
from schematics.models import Model
from schematics.types import StringType, IntType, FloatType


class Stage(Model):
    """Represents a stage in a pipeline"""
    id = IntType(required=False)
    name = StringType(required=True)
    pipeline_id = IntType(required=True)
    deal_probability = FloatType(required=False)
    rotten_flag = IntType(required=False, choices=(0,1))
    rotten_days = IntType(required=False)
    order_nr = IntType(required=False, min_value=0)


class StageResource(BaseResource):
    API_ACESSOR_NAME = 'stage'
    LIST_REQ_PATH = '/stages'
    DETAIL_REQ_PATH = '/stages/{id}'

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return Stage(raw_input(response.json))

    def create(self, deal):
        response = self._create(data=deal.to_native())
        return dict_to_model(response.json()['data'], Stage)

    def list(self):
        return CollectionResponse(self._list(), Stage)

    def stages_of_pipeline(self, pipeline):
        params = {'pipeline_id': pipeline.id}
        return CollectionResponse(self._list(params=params), Stage)


PipedriveAPI.register_resource(StageResource)
