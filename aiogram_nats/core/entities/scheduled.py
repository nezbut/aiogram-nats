import datetime
from dataclasses import dataclass


@dataclass
class ScheduledEntity:

    """
    Represents a scheduled entity with a scheduled time.

    Attributes :
        scheduled_time (datetime.datetime): The time at which the entity is scheduled.
    """

    scheduled_time: datetime.datetime

    def time_come(self) -> bool:
        """
        Checks if the current time has passed the scheduled time of the message.

        Returns :
            bool: True if the current time is greater than the scheduled time, False otherwise.
        """
        now = datetime.datetime.now(datetime.UTC)
        return now > self.scheduled_time

    def time_left(self) -> datetime.timedelta:
        """
        Calculate the time left until the scheduled time of the message.

        Returns :
            datetime.timedelta: The time left until the scheduled time. If the current time is greater than the scheduled time, returns a timedelta of 0.
        """
        now = datetime.datetime.now(datetime.UTC)
        diff = self.scheduled_time - now
        return diff if diff.total_seconds() > 0 else datetime.timedelta()
