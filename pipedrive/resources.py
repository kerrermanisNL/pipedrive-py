# encoding:utf-8
from base import BaseResource, PipedriveAPI, CollectionResponse, dict_to_model
from models import (
    User, Pipeline, Stage, SearchResult, Organization,
    Deal, Activity, ActivityType, Person, Note
)


class UserResource(BaseResource):
    MODEL_CLASS = User
    API_ACESSOR_NAME = 'user'
    LIST_REQ_PATH = '/users'
    DETAIL_REQ_PATH = '/users/{id}'
    FIND_REQ_PATH = '/users/find'

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def create(self, user):
        response = self._create(data=user.to_primitive())
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def list(self, **params):
        return CollectionResponse(self._list(params=params), self.MODEL_CLASS)

    def find(self, term, **params):
        return CollectionResponse(self._find(term, params=params),\
            self.MODEL_CLASS)

    def all(self):
        users = []

        has_more_users = True
        next_start = 0
        while has_more_users:
            result = self.list(start=next_start, limit=500)
            users = users + result.items
            has_more_users = result.more_items_in_collection
            next_start = result.next_start

        return users


class PipelineResource(BaseResource):
    MODEL_CLASS = Pipeline
    API_ACESSOR_NAME = 'pipeline'
    LIST_REQ_PATH = '/pipelines'
    DETAIL_REQ_PATH = '/pipelines/{id}'

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def create(self, pipeline):
        response = self._create(data=pipeline.to_primitive())
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def list(self, **params):
        return CollectionResponse(self._list(params=params), self.MODEL_CLASS)


class StageResource(BaseResource):
    MODEL_CLASS = Stage
    API_ACESSOR_NAME = 'stage'
    LIST_REQ_PATH = '/stages'
    DETAIL_REQ_PATH = '/stages/{id}'

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def create(self, stage):
        response = self._create(data=stage.to_primitive())
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def list(self, **params):
        return CollectionResponse(self._list(params=params), self.MODEL_CLASS)

    def stages_of_pipeline(self, pipeline, **params):
        params['pipeline_id'] = pipeline.id
        return CollectionResponse(self._list(params=params), self.MODEL_CLASS)


class SearchResource(BaseResource):
    API_ACESSOR_NAME = 'search'
    SEARCH_PATH = '/searchResults'
    SEARCH_FIELD_PATH = '/searchResults/field'

    def search_all_fields(self, term, **params):
        """Search for 'term' in all fields of all objects"""
        params['term'] = term
        response = self.send_request('GET', self.SEARCH_PATH, params, data=None)
        search_result = response.json()
        for item in search_result.get('data', []) or []:
            item['result'] = item['title']
        return CollectionResponse(search_result, SearchResult)

    def search_single_field(self, term, field, **params):
        """Search for 'term' in a specific field of a specific type of object.
           'field' must be a DealField, OrganizationField, PersonField or 
           ProductField (all from pipedrive.fields)"""
        params.update({
            'term': term,
            'field_type': field.FIELD_PARENT_TYPE,
            'field_key': field.key,
            'return_item_ids': 1,
        })
        response = self.send_request(
            'GET', self.SEARCH_FIELD_PATH, params, data=None
        )
        search_result = response.json()
        for item in search_result.get('data', []) or []:
            item['result'] = item[field.key]
            item['type'] = field.FIELD_PARENT_TYPE.replace('Field', '')
        return CollectionResponse(search_result, SearchResult)


class OrganizationResource(BaseResource):
    MODEL_CLASS = Organization
    API_ACESSOR_NAME = 'organization'
    LIST_REQ_PATH = '/organizations'
    DETAIL_REQ_PATH = '/organizations/{id}'
    FIND_REQ_PATH = '/organizations/find'
    RELATED_ENTITIES_PATH = '/organizations/{id}/{entity}'

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def create(self, organization):
        response = self._create(data=organization.to_primitive())
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def update(self, organization):
        response = self._update(organization.id,\
            data=organization.to_primitive())
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def list(self, **params):
        return CollectionResponse(self._list(params=params), self.MODEL_CLASS)

    def find(self, term, **params):
        return CollectionResponse(self._find(term, params=params),\
            self.MODEL_CLASS)

    def list_activities(self, resource_ids, **params):
        return self._related_entities(resource_ids, 'activities', Activity,\
            params=params)

    def list_deals(self, resource_ids, **params):
        return self._related_entities(resource_ids, 'deals', Deal,\
            params=params)


class DealResource(BaseResource):
    MODEL_CLASS = Deal
    API_ACESSOR_NAME = 'deal'
    LIST_REQ_PATH = '/deals'
    DETAIL_REQ_PATH = '/deals/{id}'
    FIND_REQ_PATH = '/deals/find'
    RELATED_ENTITIES_PATH = '/deals/{id}/{entity}'

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def create(self, deal):
        response = self._create(data=deal.to_primitive())
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def list(self, **params):
        return CollectionResponse(self._list(params=params), self.MODEL_CLASS)

    def find(self, term, **params):
        return CollectionResponse(self._find(term, params=params),\
            self.MODEL_CLASS)

    def list_activities(self, resource_ids, **params):
        return self._related_entities(resource_ids, 'activities', Activity,\
            params=params)

    def delete(self, deal):
        response = self._delete(deal.id)
        return response.json()


class ActivityResource(BaseResource):
    MODEL_CLASS = Activity
    API_ACESSOR_NAME = 'activity'
    LIST_REQ_PATH = '/activities'
    DETAIL_REQ_PATH = '/activities/{id}'

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def create(self, activity):
        response = self._create(data=activity.to_primitive())
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def list(self, **params):
        return CollectionResponse(self._list(params=params), self.MODEL_CLASS)

    def delete(self, activity):
        response = self._delete(activity.id)
        return response.json()

    def bulk_delete(self, activities):
        activities_ids = [activity.id for activity in activities]

        response = self._bulk_delete(activities_ids)
        return response.json()


class ActivityTypeResource(BaseResource):
    MODEL_CLASS = ActivityType
    API_ACESSOR_NAME = 'activityType'
    LIST_REQ_PATH = '/activityTypes'
    DETAIL_REQ_PATH = '/activityTypes/{id}'

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def create(self, activityType):
        response = self._create(data=activityType.to_primitive())
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def list(self, **params):
        return CollectionResponse(self._list(params=params), self.MODEL_CLASS)

    def delete(self, activityType):
        response = self._delete(activityType.id)
        return response.json()

    def bulk_delete(self, activityTypes):
        activityTypes_ids = [activityType.id for activityType in activityTypes]

        response = self._bulk_delete(activities_ids)
        return response.json()


class PersonResource(BaseResource):
    MODEL_CLASS = Person
    API_ACESSOR_NAME = 'person'
    LIST_REQ_PATH = '/persons'
    DETAIL_REQ_PATH = '/persons/{id}'
    FIND_REQ_PATH = '/persons/find'
    RELATED_ENTITIES_PATH = '/persons/{id}/{entity}'

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def create(self, person):
        response = self._create(data=person.to_primitive())
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def update(self, person):
        response = self._update(person.id, data=person.to_primitive())
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def list(self, **params):
        return CollectionResponse(self._list(params=params), self.MODEL_CLASS)

    def find(self, term, **params):
        return CollectionResponse(self._find(term, params=params), self.MODEL_CLASS)

    def delete(self, person):
        response = self._delete(person.id)
        return response.json()

    def bulk_delete(self, persons):
        person_ids = [person.id for person in persons]

        response = self._bulk_delete(person_ids)
        return response.json()


class NoteResource(BaseResource):
    MODEL_CLASS = Note
    API_ACESSOR_NAME = 'note'
    LIST_REQ_PATH = '/notes'
    DETAIL_REQ_PATH = '/notes/{id}'

    def detail(self, resource_ids):
        response = self._detail(resource_ids)
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def create(self, note):
        response = self._create(data=note.to_primitive())
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def update(self, note):
        response = self._update(note.id, data=note.to_primitive())
        return dict_to_model(response.json()['data'], self.MODEL_CLASS)

    def list(self, **params):
        return CollectionResponse(self._list(params=params), self.MODEL_CLASS)

    def delete(self, note):
        response = self._delete(note.id)
        return response.json()

    def bulk_delete(self, notes):
        note_ids = [note.id for note in notes]

        response = self._bulk_delete(note_ids)
        return response.json()

# Registers the resources
for resource_class in [
    UserResource,
    PipelineResource,
    StageResource,
    SearchResource,
    OrganizationResource,
    DealResource,
    ActivityResource,
    ActivityTypeResource,
    PersonResource,
    NoteResource,
]:
    PipedriveAPI.register_resource(resource_class)
