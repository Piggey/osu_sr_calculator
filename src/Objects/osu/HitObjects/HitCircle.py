from Objects_osu_HitObjects_HitObject import HitObject
from Objects_Vector2 import Vector2

class HitCircle(HitObject):
    def __init__(self, pos, startTime, **kwargs):
        radius = kwargs.get('radius', None)
        super().__init__(pos, startTime, radius=radius)