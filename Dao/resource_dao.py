from pymongo import MongoClient

from MainAPI.models import Resource
from constants import Constants


class ResourceDao:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        print("Database Client created")

    def read(self, resource_id):
        resource_log = self.client["test_db"]["resource_log"]
        cursor = resource_log.find_one({"resource_id": str(resource_id)})
        if cursor is None:
            return None
        resource = Resource(resource_id)
        for attr in resource.__dict__:
            resource.__dict__[attr] = cursor.get(attr)
        return resource

    def create(self, resource):
        try:
            resource_log = self.client["test_db"]["resource_log"]
            print(type(resource.to_bson()))
            resource_log.insert_one(resource.to_bson())
        except Exception as e:
            print('ERROR!!: ' + str(e))

    def update(self, resource):
        resource_log = self.client["test_db"]["resource_log"]
        query = {'resource_id': resource.resource_id, 'version': int(resource.version)}
        resource.version += 1
        update = resource.to_bson()
        response = resource_log.find_and_modify(query=query, update=update)
        return response is not None