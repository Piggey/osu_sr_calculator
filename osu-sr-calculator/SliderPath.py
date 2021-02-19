from .Objects.osu.PathType import PathType
from .PathApproximator import PathApproximator
from .Objects.Vector2 import Vector2
from .Precision import Precision

class SliderPath:
    pathType = None
    controlPoints = []
    expectedDistance = None
    isInitialised = False

    calculatedPath = []
    cumulativeLength = []
    pathApproximator = PathApproximator()

    def __init__(self, pathType, controlPoints, expectedDistance):
        self.pathType = pathType
        self.controlPoints = controlPoints
        self.expectedDistance = expectedDistance

        self.ensureInitialised()

    def ensureInitialised(self):
        if(self.isInitialised):
            return

        self.isInitialised = True
        self.controlPoints = self.controlPoints if self.controlPoints is not None else []
        self.calculatedPath = []
        self.cumulativeLength = []

        self.calculatePath()
        self.calculateCumulativeLength()

    def calculatePath(self):
        self.calculatedPath = []
        start = 0
        end = 0

        for i in range(len(self.controlPoints)):
            end += 1
            if(i == (len(self.controlPoints) - 1) or (self.controlPoints[i].x == self.controlPoints[i + 1].x and self.controlPoints[i].y == self.controlPoints[i + 1].y)):
                cpSpan = self.controlPoints[start:end]
                for t in self.calculateSubPath(cpSpan):
                    if(len(self.calculatedPath) == 0 or self.calculatedPath[len(self.calculatedPath) - 1].x != t.x or self.calculatedPath[len(self.calculatedPath) - 1].y != t.y):
                        self.calculatedPath.append(Vector2(t.x, t.y))
                
                start = end

    def calculateSubPath(self, subControlPoints):
        if(self.pathType == PathType.Linear.name):
            return self.pathApproximator.approximateLinear(subControlPoints)

        elif(self.pathType == PathType.PerfectCurve.name):
            if(len(self.controlPoints) != 3 or len(subControlPoints) != 3):
                return
            subPath = self.pathApproximator.approximateCircularArc(subControlPoints)
            if(len(subPath) == 0):
                return 
            return subPath

        elif(self.pathType == PathType.Catmull):
            return self.pathApproximator.approximateCatmull(subControlPoints)
        
        else:
            return self.pathApproximator.approximateBezier(subControlPoints)

    def calculateCumulativeLength(self):
        l = 0
        self.cumulativeLength = []
        self.cumulativeLength.append(l)

        for i in range((len(self.calculatedPath) - 1)):
            diff = self.calculatedPath[i + 1].subtract(self.calculatedPath[i])
            d = diff.length()

            if(self.expectedDistance is not None and self.expectedDistance - l < d):
                self.calculatedPath[i + 1] = self.calculatedPath[i].add(diff.scale((self.expectedDistance - l) / d))
                for j in range(i + 2, (len(self.calculatedPath) - 2 - i)):
                    self.calculatedPath.remove(self.calculatedPath[j])
                
                l = self.expectedDistance
                self.cumulativeLength.append(l)
                break

            l += d
            self.cumulativeLength.append(l)

        if(self.expectedDistance is not None and l < self.expectedDistance and len(self.calculatedPath) > 1):
            diff = self.calculatedPath[len(self.calculatedPath) - 1].subtract(self.calculatedPath[len(self.calculatedPath) - 2])
            d = diff.length()

            if(d <= 0):
                return

            self.calculatedPath[len(self.calculatedPath) - 1].add(diff.scale((self.expectedDistance - l) / d))
            self.cumulativeLength[len(self.calculatedPath) - 1] = self.expectedDistance

    def PositionAt(self, progress):
        self.ensureInitialised()
        d = self.__progressToDistance(progress)
        return self.__interpolateVertices(self.__indexOfDistance(d), d)
    
    def __progressToDistance(self, progress):
        return min(max(progress, 0), 1) * self.expectedDistance

    def __interpolateVertices(self, i, d):
        if(len(self.calculatedPath) == 0):
            return Vector2(0, 0)
        
        if(i <= 0):
            return self.calculatedPath[0]
        if(i >= len(self.calculatedPath)):
            return self.calculatedPath[len(self.calculatedPath) - 1]
        
        p0 = self.calculatedPath[i - 1]
        p1 = self.calculatedPath[i]

        d0 = self.cumulativeLength[i - 1]
        d1 = self.cumulativeLength[i]

        if(Precision.almostEqualsNumber(self, d0, d1)): # uhh what
            return p0
        
        w = (d - d0) / (d1 - d0)
        result = p0.add(p1.subtract(p0).scale(w))
        return result
    
    def __indexOfDistance(self, d):
        try:
            index = self.cumulativeLength.index(d)
        except ValueError:
            # print(ValueError)
            for cL in self.cumulativeLength:
                if(cL > d):
                    return self.cumulativeLength.index(cL)

            return len(self.cumulativeLength)

        return index