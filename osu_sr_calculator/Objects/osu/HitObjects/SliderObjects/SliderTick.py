from ..HitObject import HitObject
from ....Vector2 import Vector2

class SliderTick(HitObject):
    SpanIndex = None
    SpanStartTime = None

    def __init__(self, pos, startTime, spanIndex, spanStartTime, **kwargs):
        radius = kwargs.get('radius', None)
        super().__init__(pos, startTime, radius=radius)
        self.SpanIndex = spanIndex
        self.SpanStartTime = spanStartTime