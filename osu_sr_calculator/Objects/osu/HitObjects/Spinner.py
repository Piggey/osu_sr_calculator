from .HitObject import HitObject
from ...Vector2 import Vector2

class Spinner(HitObject):
    EndTime = None

    def __init__(self, pos, startTime, endTime):
        super().__init__(pos, startTime)
        self.EndTime = endTime