from .Objects.Vector2 import Vector2
from abc import ABC

class Precision(ABC):
    FLOAT_EPSILON = 1e-3

    def almostEqualsNumber(self, value1, value2, acceptableDifference = FLOAT_EPSILON):
        return abs(value1 - value2) <= acceptableDifference

    def almostEqualsVector(self, vec1, vec2, acceptableDifference = FLOAT_EPSILON):
        return self.almostEqualsNumber(vec1.x, vec2.x, acceptableDifference) and self.almostEqualsNumber(vec1.y, vec2.y, acceptableDifference)
