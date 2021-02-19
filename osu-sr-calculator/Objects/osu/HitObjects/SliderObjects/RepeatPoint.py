from ..HitObject import HitObject
from ....Vector2 import Vector2

class RepeatPoint(HitObject):
    RepeatIndex = None
    SpanDuration = None

    def __init__(self, pos, startTime, repeatIndex, spanDuration, **kwargs):
        radius = kwargs.get('radius', None)
        super().__init__(pos, startTime, radius=radius)
        self.RepeatIndex = repeatIndex
        self.SpanDuration = spanDuration