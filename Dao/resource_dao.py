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

    def create2(self, resource_id):
        resource_log = self.client["test_db"]["resource_log"]
        cursor = resource_log.find_one({"resource_id": str(resource_id)})
        if not cursor:
            resource_log.insert_one({
                "resource_id": str(resource_id),
                "status": None,
                "time_start": None,
                "time_end": None
            })
            return True, "Created Document"
        else:
            return False, "Document exists"

    def update(self, resource):
        resource_log = self.client["test_db"]["resource_log"]
        resource_log.update({'resource_id': resource.resource_id}, resource.to_bson())

    def update2(self, resource_id, task_status=None, task_start_time=None, task_end_time=None, action_name=None,
                action_object=None):
        resource_log = self.client["test_db"]["resource_log"]
        if task_status and (task_start_time or task_end_time):
            if task_start_time:
                resource_log.update({"resource_id": str(resource_id)},
                                    {"$set": {"status": task_status, "time_start": task_start_time}})
            if task_end_time:
                resource_log.update({"resource_id": str(resource_id)},
                                    {"$set": {"status": task_status, "time_start": task_end_time}})
        if action_name and action_object:
            cursor = resource_log.find_one({"resource_id": str(resource_id)})
            action = cursor.get(action_name, [])
            action.append(action_object)
            resource_log.update({"resource_id": str(resource_id)}, {"$set": {action_name: action}})
