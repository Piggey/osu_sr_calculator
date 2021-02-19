from .Objects.Vector2 import Vector2
from .Precision import Precision
from math import atan2, pi, ceil, acos, cos, sin

class PathApproximator(object):
    bezier_tolerance = 0.25
    catmull_detail = 50
    circular_arc_tolerance = 0.1

    def approximateBezier(self, controlPoints):
        output = []
        count = len(controlPoints)

        if(count == 0):
            return output
        
        subdivisionBuffer1 = []
        subdivisionBuffer2 = []
        for i in range(count):
            subdivisionBuffer1.append(Vector2(0, 0))

        for i in range(count * 2 - 1):
            subdivisionBuffer2.append(Vector2(0, 0))

        toFlatten = []
        freeBuffers = []

        deepCopy = []

        for c in controlPoints:
            deepCopy.append(Vector2(c.x, c.y))

        toFlatten.append(deepCopy)

        leftChild = subdivisionBuffer2

        while(len(toFlatten) > 0):
            parent = toFlatten.pop()
            if(self.__bezierIsFlatEnough(parent)):
                self.__bezierApproximate(parent, output, subdivisionBuffer1, subdivisionBuffer2, count)
                freeBuffers.append(parent)
                continue
        
            rightChild = []
            if(len(freeBuffers) > 0):
                rightChild = freeBuffers.pop()
            else:
                for i in range(count):
                    rightChild.append(Vector2(0, 0))

            self.__bezierSubdivide(parent, leftChild, rightChild, subdivisionBuffer1, count)

            for i in range(count):
                parent[i] = leftChild[i]

            toFlatten.append(rightChild)
            toFlatten.append(parent)
        
        output.append(controlPoints[count - 1])
        return output

    def approximateCatmull(self, controlPoints):
        result = []

        for i in range(len(controlPoints) - 1):
            v1 = controlPoints[i - 1] if i > 0 else controlPoints[i]
            v2 = controlPoints[i]
            v3 = controlPoints[i + 1] if i < (len(controlPoints) - 1) else v2.add(v2).subtract(v1)
            v4 = controlPoints[i + 2] if i < (len(controlPoints) - 2) else v3.add(v3).subtract(v2)

            for c in range(self.catmull_detail):
                result.append(self.__catmullFindPoint(v1, v2, v3, v4, c / self.catmull_detail))
                result.append(self.__catmullFindPoint(v1, v2, v3, v4, (c + 1) / self.catmull_detail))

        return result

    def approximateCircularArc(self, controlPoints):
        a = controlPoints[0]
        b = controlPoints[1]
        c = controlPoints[2]

        aSq = (b.subtract(c)).lengthSquared()
        bSq = (a.subtract(c)).lengthSquared()
        cSq = (a.subtract(b)).lengthSquared()

        if(Precision.almostEqualsNumber(aSq, 0) or Precision.almostEqualsNumber(bSq, 0) or Precision.almostEqualsNumber(cSq, 0)):
            return []
        
        s = aSq * (bSq + cSq - aSq)
        t = bSq * (aSq + cSq - bSq)
        u = cSq * (aSq + bSq - cSq)

        Sum = s + t + u

        if(Precision.almostEqualsNumber(Sum, 0)):
            return []

        centre = (a.scale(s).add(b.scale(t)).add(c.scale(u))).divide(Sum)
        dA = a.subtract(centre)
        dC = c.subtract(centre)

        r = dA.length()

        thetaStart = atan2(dA.y, dA.x)
        thetaEnd = atan2(dC.y, dC.x)

        while(thetaEnd < thetaStart):
            thetaEnd += 2 * pi

        Dir = 1
        thetaRange = thetaEnd - thetaStart

        orthoAtoC = c.subtract(a)
        orthoAtoC = Vector2(orthoAtoC.y, -1 * orthoAtoC.x)
        if(orthoAtoC.dot(b.subtract(a)) < 0):
            Dir = -1 * Dir
            thetaRange = 2 * pi - thetaRange

        amountPoints = 2 if 2 * r <= self.circular_arc_tolerance else max(2, ceil(thetaRange / (2 * acos(1 - self.circular_arc_tolerance / r))))
        
        output = []

        for i in range(amountPoints):
            fract = 1 / (amountPoints - 1)
            theta = thetaStart + Dir * fract * thetaRange
            o = Vector2(cos(theta), sin(theta)).scale(r)
            output.append(centre.add(o))

        return output

    def approximateLinear(self, controlPoints):
        return controlPoints
    
    def __bezierIsFlatEnough(self, controlPoints):
        for i in range(1, (len(controlPoints) - 1)):
            if((controlPoints[i - 1].subtract(controlPoints[i].scale(2)).add(controlPoints[i + 1])).lengthSquared() > self.bezier_tolerance * self.bezier_tolerance * 4):
                return False

        return True

    def __bezierApproximate(self, controlPoints, output, subdivisionBuffer1, subdivisionBuffer2, count):
        l = subdivisionBuffer2
        r = subdivisionBuffer1

        self.__bezierSubdivide(controlPoints, l, r, subdivisionBuffer1, count)

        for i in range(count - 1):
            l[count + i] = r[i + 1]

        output.append(controlPoints[0])
        for i in range(1, count - 1):
            index = 2 * i 
            p = (l[index - 1].add(l[index].scale(2)).add(l[index + 1])).scale(0.25)
            output.append(p)

    def __bezierSubdivide(self, controlPoints, l, r, subdivisionBuffer, count):
        midpoints = subdivisionBuffer

        for i in range(count):
            midpoints[i] = controlPoints[i]

        for i in range(count):
            l[i] = midpoints[0]
            r[count - i - 1] = midpoints[count - i - 1]

            for j in range(count - i - 1):
                midpoints[j] = (midpoints[j].add(midpoints[j + 1])).divide(2)

    def __catmullFindPoint(self, vec1, vec2, vec3, vec4, t):
        t2 = t * t
        t3 = t * t2
        result = Vector2(
            0.5 * (2 * vec2.x + (-vec1.x + vec3.x) * t + (2 * vec1.x - 5 * vec2.x + 4 * vec3.x - vec4.x) * t2 + (-vec1.x + 3 * vec2.x - 3 * vec3.x + vec4.x) * t3),
            0.5 * (2 * vec2.y + (-vec1.y + vec3.y) * t + (2 * vec1.y - 5 * vec2.y + 4 * vec3.y - vec4.y) * t2 + (-vec1.y + 3 * vec2.y - 3 * vec3.y + vec4.y) * t3)
        )

        return result
