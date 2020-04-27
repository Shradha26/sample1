from enum import Enum


class Constants(Enum):
    ACTIONS = ["A1", "A2", "A3"]
    ACTION_MAP = {
        "A1": "Action1_Q",
        "A2": "Action2_Q",
        "A3": "Action3_Q"
    }
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    FAILED = "Failed"
