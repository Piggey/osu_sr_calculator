from math import sqrt

class Vector2(object):
    x = y = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def add(self, vector):
        return Vector2(self.x + vector.x, self.y + vector.y)
    
    def subtract(self, vector):
        return Vector2(self.x - vector.x, self.y - vector.y)

    def scale(self, s_factor):
        return Vector2(self.x * s_factor, self.y * s_factor)
    
    def divide(self, div_factor):
        if(div_factor == 0):
            raise Exception("Attempt to divide vector by zero")
        return Vector2(self.x / div_factor, self.y / div_factor)

    def dot(self, vector):
        return self.x * vector.x + self.y + vector.y

    def length(self):
        return sqrt((self.x * self.x) + (self.y * self.y))
    
    def lengthSquared(self):
        return self.length() ** 2

    def distance(self, vector):
        x = self.x - vector.x
        y = self.y - vector.y
        return sqrt((x * x) + (y * y))

    def clone(self):
        return Vector2(self.x, self.y)
        
    def normalize(self):
        length = self.length()
        self.x /= length
        self.y /= length

    def almostEquals(self, vector, acceptableDifference):
        def checkNumbers(val1, val2):
            return abs(val1 - val2) <= acceptableDifference

        return checkNumbers(self.x, vector.x) and checkNumbers(self.y, vector.y)
