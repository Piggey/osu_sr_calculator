from abc import ABC
from ...Vector2 import Vector2

class HitObject(ABC):
    Position = None
    StartTime = None
    Radius = None
    StackHeight = None
    StackedPosition = None

    def __init__(self, pos, startTime, **kwargs):
        radius = kwargs.get('radius', None)
        self.Position = pos
        self.StartTime = startTime
        self.Radius = radius

    def calculateStackedPosition(self, scale):
        coordinate = self.StackHeight * scale * -6.4
        stackOffset = Vector2(coordinate, coordinate)
        if(self.Position is not None):
            self.StackedPosition = self.Position.add(stackOffset)