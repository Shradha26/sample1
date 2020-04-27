from datetime import datetime
from json import dumps

from django.http import HttpResponse
from MainAPI.Queue.producer import Producer
from Dao.resource_dao import ResourceDao
from constants import Constants
from MainAPI.models import Resource, Action


def main(request):
    resource_id = str(request.GET["id"])
    resource_dao = ResourceDao()
    resource = resource_dao.read(resource_id)
    action = None
    if not resource:
        #print("No resource object obtained in main; starting at action 1")
        action = "A1"
        resource = Resource(resource_id=resource_id)
        resource_dao.create(resource)
    else:
        for ac in Constants["ACTIONS"].value:
            print("At action: "+ac)
            actions = resource.actions
            print(actions)
            if ac not in actions or actions.get(ac)[-1].get("status") == Constants.FAILED.value:
                action = ac
                break
            if actions.get(ac)[-1].get("status") == Constants.IN_PROGRESS.value:
                return HttpResponse("Duplicate request; action " + ac + " in progress")
    if action:
        producer = Producer()
        producer.publish(resource_id, Constants["ACTION_MAP"].value.get(action))
        producer.shutdown()
        return HttpResponse("Starting at action: " + action)
    return HttpResponse("All actions already completed")