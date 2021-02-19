from .Objects.osu.HitObjects.HitObject import HitObject
from .Objects.osu.HitObjects.DifficultyHitObject import DifficultyHitObject
from .Objects.osu.HitObjects.Slider import Slider
from .Objects.osu.HitObjects.Spinner import Spinner
from .Objects.Vector2 import Vector2
from math import atan2

class DifficultyHitObjectCreator(object):
    difficultyHitObjects = []

    lastLastObject = None
    lastObject = None
    currentObject = None
    timeRate = None

    normalized_radius = 52
    TravelDistance = 0
    JumpDistance = 0
    Angle = 0
    DeltaTime = 0
    StrainTime = 0

    def convertToDifficultyHitObjects(self, hitObjects, timeRate):
        self.difficultyHitObjects = []

        for i in range(1, len(hitObjects)):
            lastLast = hitObjects[i - 2] if i > 1 else None
            last = hitObjects[i - 1]
            current = hitObjects[i]

            difficultyHitObject = self.createDifficultyHitObject(lastLast, last, current, timeRate)
            self.difficultyHitObjects.append(difficultyHitObject)

        return self.difficultyHitObjects

    def createDifficultyHitObject(self, lastLast, last, current, timeRate):
        self.lastLastObject = lastLast
        self.lastObject = last
        self.currentObject = current
        self.timeRate = timeRate

        self.setDistances()
        self.setTimingValues()

        return DifficultyHitObject(self.currentObject, self.lastObject, self.lastLastObject, self.TravelDistance, self.JumpDistance, self.Angle, self.DeltaTime, self.StrainTime)

    def setDistances(self):
        self.TravelDistance = 0
        self.JumpDistance = 0
        self.Angle = 0
        self.DeltaTime = 0
        self.StrainTime = 0

        scalingFactor = self.normalized_radius / self.currentObject.Radius  
        if(self.currentObject.Radius < 30):
            smallCircleBonus = min(30 - self.currentObject.Radius, 5) / 50
            scalingFactor *= 1 + smallCircleBonus
        
        if(isinstance(self.lastObject, Slider)):
            lastSlider = self.lastObject
            self.computeSliderCursorPosition(lastSlider)
            self.TravelDistance = lastSlider.LazyTravelDistance * scalingFactor

        lastCursorPosition = self.getEndCursorPosition(self.lastObject)

        if(not isinstance(self.currentObject, Spinner)):
            self.JumpDistance = self.currentObject.StackedPosition.scale(scalingFactor).subtract(lastCursorPosition.scale(scalingFactor)).length()
        
        if(self.lastLastObject is not None):
            lastLastCursorPosition = self.getEndCursorPosition(self.lastLastObject)

            v1 = lastLastCursorPosition.subtract(self.lastObject.StackedPosition)
            v2 = self.currentObject.StackedPosition.subtract(lastCursorPosition)

            dot = v1.dot(v2)
            det = v1.x * v2.y - v1.y * v2.x

            self.Angle = abs(atan2(det, dot))

    def setTimingValues(self):
        self.DeltaTime = (self.currentObject.StartTime - self.lastObject.StartTime) / self.timeRate
        self.StrainTime = max(50, self.DeltaTime)

    def computeSliderCursorPosition(self, slider):
        if(slider.LazyEndPosition is not None):
            return
        slider.LazyEndPosition = slider.StackedPosition
        slider.LazyTravelDistance = 0

        approxFollowCircleRadius = slider.Radius * 3
        def computeVertex(t):
            progress = (t - slider.StartTime) / slider.SpanDuration
            if(progress % 2 >= 1):
                progress = 1 - progress % 1
            else:
                progress = progress % 1
            
            diff = slider.StackedPosition.add(slider.Path.PositionAt(progress)).subtract(slider.LazyEndPosition)
            dist = diff.length()

            if(dist > approxFollowCircleRadius):
                diff.normalize()
                dist -= approxFollowCircleRadius
                slider.LazyEndPosition = slider.LazyEndPosition.add(diff.scale(dist))
                slider.LazyTravelDistance = dist if slider.LazyTravelDistance is None else slider.LazyTravelDistance + dist

        def mapFunc(t):
            return t.StartTime
        scoringTimes = map(mapFunc, slider.NestedHitObjects[1:len(slider.NestedHitObjects)])

        for time in scoringTimes:
            computeVertex(time)

    def getEndCursorPosition(self, obj):
        pos = obj.StackedPosition

        if(isinstance(obj, Slider)):
            self.computeSliderCursorPosition(obj)
            pos = obj.LazyEndPosition if obj.LazyEndPosition is not None else pos

        return pos