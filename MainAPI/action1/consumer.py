import threading
import time
from datetime import datetime

from Dao.resource_dao import ResourceDao
from MainAPI.action1.producer import Producer
from MainAPI.models import Action
from abstract_consumer import AbstractConsumer
from constants import Constants

ACTION_NAME = 'A1'
NEXT_ACTION_NAME = 'A2'


class Consumer(AbstractConsumer):
    def __init__(self, queue_id):
        self.queue_id = queue_id
        super().__init__(self.queue_id)

    def consume(self, resource_id):
        print('Resource_id received ' + resource_id + " by " + threading.current_thread().name)
        # mark status as In Progress
        resource_dao = ResourceDao()
        resource = resource_dao.read(resource_id)

        # Check to ignore
        if ACTION_NAME in resource.actions:
            if resource.actions[ACTION_NAME][-1].get('status') == Constants.COMPLETED.value:
                print('Ignoring Completed Action: A1 for resource_id: ' + resource_id)
                producer = Producer()
                producer.publish(resource_id=resource_id, key=Constants["ACTION_MAP"].value.get(NEXT_ACTION_NAME))
                return
            elif resource.actions[ACTION_NAME][-1].get('status') == Constants.IN_PROGRESS.value:
                print('Ignoring InProgress Action: A1 for resource_id: ' + resource_id)
                return

        # prep the resource
        resource.status = Constants.IN_PROGRESS.value
        resource.time_start = str(datetime.now())
        if ACTION_NAME not in resource.actions:
            resource.actions[ACTION_NAME] = []
        new_action = Action(status=Constants.IN_PROGRESS.value, time_start=str(datetime.now()), action_name=ACTION_NAME)
        resource.actions[ACTION_NAME].append(new_action)

        # update
        resource_dao.update(resource)

        # mock call to action1 API
        producer = Producer()
        time.sleep(20)
        new_action.time_end = str(datetime.now())
        if resource_id == '999':
            resource.status = Constants.FAILED.value
            resource.time_end = str(datetime.now())
            new_action.status = Constants.FAILED.value
            new_action.failure_reason = 'Exception in Action 1 API'
        else:
            new_action.status = Constants.COMPLETED.value
            producer.publish(resource_id=resource_id, key=Constants["ACTION_MAP"].value.get(NEXT_ACTION_NAME))

        # mark complete/ failed
        resource_dao.update(resource)