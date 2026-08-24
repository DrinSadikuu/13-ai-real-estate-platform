from enum import StrEnum

class ViewingStatus(StrEnum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELED = "canceled"