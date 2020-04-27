# Create your models here.
import json

from bson.json_util import loads


class Resource:
    def to_bson(self):
        return loads(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True))

    def __init__(self, resource_id, status=None, restart=False, time_start=None, time_end=None, actions={}):
        self.resource_id = resource_id
        self.status = status
        self.restart = restart
        self.time_start = time_start
        self.time_end = time_end
        self.actions = actions


class Action:
    def __init__(self, action_name, status, time_start, failure_reason=None, time_end=None):
        self.action_name = action_name
        self.status = status
        self.failure_reason = failure_reason
        self.time_start = time_start
        self.time_end = time_end
