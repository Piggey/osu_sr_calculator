from .Objects.osu.HitType import HitType
from .Objects.osu.PathType import PathType
from .Objects.Vector2 import Vector2
from .Objects.osu.Beatmap import Beatmap
from .Objects.osu.HitObjects.HitObject import HitObject
from .Objects.osu.HitObjects.HitCircle import HitCircle
from .Objects.osu.HitObjects.Slider import Slider
from .Objects.osu.HitObjects.Spinner import Spinner
from .SliderPath import SliderPath
from .Precision import Precision
from functools import cmp_to_key
from warnings import warn

class BeatmapParser(object):
    beatmap = Beatmap()

    def parseBeatmap(self, data, mods):
        if(not data):
            raise Exception("No beatmap found")

        self.beatmap = Beatmap()
        section = None
        lines = map(lambda line: line.strip(), data.split("\n"))
        
        for line in lines:
            # print(line)
            if(line.startswith('//') or not line):
                continue
            if(not section and 'osu file format v' in line):
                self.beatmap.Version = int(line.split('osu file format v')[1])
                continue
            
            if(line[0] == '['):
                section = line.split('[')[1].split(']')[0]
                continue
                
            if(section == 'General'):
                key, value = map(lambda v: v.strip(), line.split(':'))
                if(key == 'StackLeniency'):
                    self.beatmap.StackLeniency = float(value)
            
            elif(section == 'Difficulty'):
                key, value = map(lambda v: v.strip(), line.split(':'))
                self.beatmap.Difficulty[key] = float(value)

            elif(section == 'TimingPoints'):
                split = line.split(',')

                time = int(split[0]) + (24 if self.beatmap.Version < 5 else 0)
                beatLength = float(split[1])
                speedMultiplier = 100 / -beatLength if beatLength < 0 else 1
                timeSignature = 4
                if(len(split) >= 3):
                    timeSignature = 4 if split[2][0] == '0' else int(split[2])

                timingChange = True
                if(len(split) >= 7):
                    timingChange = split[6][0] == '1'

                if(timingChange):
                    self.beatmap.TimingPoints.append({
                        "Time": time,
                        "BeatLength": beatLength,
                        "TimeSignature": timeSignature
                    })

                self.beatmap.DifficultyTimingPoints.append({
                    "Time": time,
                    "SpeedMultiplier": speedMultiplier
                })

            elif(section == 'HitObjects'):
                split = line.split(',')
                pos = Vector2(int(split[0]), int(split[1]))
                startTime = int(split[2])
                hitType = int(split[3])

                result = None

                scale = (1 - 0.7 * (self.getCircleSize(mods) - 5) / 5) / 2
                radius = 64 * scale

                if(hitType & HitType.Normal.value[0]):
                    result = self.createCircle(pos, startTime, radius)
                
                if(hitType & HitType.Slider.value[0]):
                    pathType = None
                    length = 0
                    pointSplit = split[5].split('|')

                    points = [Vector2(0, 0)]
                    for point in pointSplit:
                        if(len(point) == 1):
                            if(point == 'C'):
                                pathType = PathType.Catmull
                            elif(point == 'B'):
                                pathType = PathType.Bezier
                            elif(point == 'L'):
                                pathType = PathType.Linear
                            elif(point == 'P'):
                                pathType = PathType.PerfectCurve
                            else:
                                pathType = PathType.Catmull
                        
                            break

                        temp = point.split(':')
                        points.append(Vector2(int(temp[0]), int(temp[1])).subtract(pos))
                    
                    def isLinear(p):
                        return Precision.almostEqualsNumber(0, (p[1].y - p[0].y) * (p[2].x - p[0].x) - (p[1].x - p[0].x) * (p[2].y - p[0].y))
                    
                    if(len(points) == 3 and pathType == PathType.PerfectCurve and isLinear(points)):
                        pathType = PathType.Linear
                    
                    repeatCount = int(split[6])
                    repeatCount = max(0, repeatCount - 1)

                    if(len(split) > 7):
                        length = float(split[7])
                    
                    result = self.createSlider(pos, points, length, pathType, repeatCount, startTime, radius)
                
                if(hitType & HitType.Spinner.value[0]):
                    endTime = int(split[5])
                    result = self.createSpinner(pos, startTime, endTime)

                self.beatmap.HitObjects.append(result)

        for h in self.beatmap.HitObjects:
            h.StackHeight = 0

        self.applyStacking(0, len(self.beatmap.HitObjects) - 1)

        scale = (1 - 0.7 * (self.getCircleSize(mods) - 5) / 5) / 2

        for hitObject in self.beatmap.HitObjects:
            hitObject.calculateStackedPosition(scale)
        
        return self.beatmap

    def createCircle(self, pos, startTime, radius):
        return HitCircle(pos, startTime, radius=radius)

    def createSlider(self, pos, points, length, pathType, repeatCount, startTime, radius):
        path = SliderPath(pathType, points, max(0, length))

        speedMultiplier = self.getSpeedMultiplier(startTime)
        beatLength = self.getBeatLength(startTime)

        return Slider(pos, startTime, path, repeatCount, speedMultiplier, beatLength, self.beatmap.Difficulty, radius)

    def createSpinner(self, pos, startTime, endTime):
        return Spinner(pos, startTime, endTime)
    
    def getSpeedMultiplier(self, startTime):
        currentTimingPoint = self.getTimingPoints(startTime, self.beatmap.DifficultyTimingPoints)
        return currentTimingPoint['SpeedMultiplier']

    def getBeatLength(self, startTime):
        currentTimingPoint = self.getTimingPoints(startTime, self.beatmap.TimingPoints)
        return currentTimingPoint['BeatLength']
    
    def getTimingPoints(self, startTime, timingPoints):
        timingPoints = sorted(timingPoints, key=cmp_to_key(lambda a, b: a['Time'] - b['Time']))
        currentTimingPoint = None
        for i in range(len(timingPoints)):
            if(timingPoints[i]['Time'] > startTime):
                currentTimingPoint = i - 1
                break
        
        if(currentTimingPoint == None):
            currentTimingPoint = len(timingPoints) - 1

        if(currentTimingPoint < 0):
            currentTimingPoint = 0
            warn(f'Warning: first timing point after current hit object ({startTime}). Defaulting to first timing point of the map.', Warning)

        return timingPoints[currentTimingPoint]
    
    def applyStacking(self, startIndex, endIndex):
        stack_distance = 3
        TimePreempt = 600

        if(self.beatmap.Difficulty['ApproachRate'] > 5):
            TimePreempt = 1200 + (450 - 1200) * (self.beatmap.Difficulty["ApproachRate"] - 5) / 5
        elif(self.beatmap.Difficulty['ApproachRate'] < 5):
            TimePreempt = 1200 - (1200 - 1800) * (5 - self.beatmap.Difficulty["ApproachRate"]) / 5
        else:
            TimePreempt = 1200

        extendedEndIndex = endIndex
        if(endIndex < (len(self.beatmap.HitObjects) - 1)):
            for i in range(endIndex, startIndex - 1, -1):
                stackBaseIndex = i
                for n in range(stackBaseIndex + 1, len(self.beatmap.HitObjects)):
                    stackBaseObject = self.beatmap.HitObjects[stackBaseIndex]
                    if(isinstance(stackBaseObject, Spinner)):
                        break

                    objectN = self.beatmap.HitObjects[n]
                    if(isinstance(objectN, Spinner)):
                        continue

                    if(isinstance(stackBaseObject, HitCircle)):
                        endTime = stackBaseObject.StartTime
                    else:
                        endTime = stackBaseObject.EndTime

                    stackThreshold = TimePreempt * self.beatmap.StackLeniency

                    if(objectN.StartTime - endTime > stackThreshold):
                        break

                    if(isinstance(stackBaseObject, Slider) and stackBaseObject.EndPosition.distance(objectN.Position) < stack_distance):
                        endPositionDistanceCheck = True
                    else:
                        endPositionDistanceCheck = False

                    if(stackBaseObject.Position.distance(objectN.Position) < stack_distance or endPositionDistanceCheck):
                        stackBaseIndex = n
                        objectN.StackHeight = 0
                
                if(stackBaseIndex > extendedEndIndex):
                    extendedEndIndex = stackBaseIndex
                    if(extendedEndIndex == (len(self.beatmap.HitObjects) - 1)):
                        break
                
        extendedStartIndex = startIndex
        for i in range(extendedEndIndex, startIndex, -1):
            n = i

            objectI = self.beatmap.HitObjects[i]
            if(objectI.StackHeight != 0 or isinstance(objectI, Spinner)):
                continue

            stackThreshold = TimePreempt * self.beatmap.StackLeniency
            if(isinstance(objectI, HitCircle)):
                while(n - 1 >= 0):
                    objectN = self.beatmap.HitObjects[n]
                    if(isinstance(objectN, Spinner)):
                        continue

                    if(isinstance(objectN, HitCircle)):
                        endTime = objectN.StartTime
                    else:
                        endTime = objectN.EndTime

                    if(objectI.StartTime - endTime > stackThreshold):
                        break

                    if(n < extendedStartIndex):
                        objectN.StackHeight = 0
                        extendedStartIndex = n

                    if(isinstance(objectN, Slider) and objectN.EndPosition.distance(objectI.Position) < stack_distance):
                        endPositionDistanceCheck = True
                    else:
                        endPositionDistanceCheck = False

                    if(endPositionDistanceCheck):
                        offset = objectI.StackHeight - objectN.StackHeight + 1
                        for j in range(n + 1, i + 1):
                            objectJ = self.beatmap.HitObjects[j]
                            if(objectN.EndPosition.distance(objectJ.Position) < stack_distance):
                                objectJ.StackHeight -= offset
                                
                        break

                    if(objectN.Position.distance(objectI.Position) < stack_distance):
                        objectN.StackHeight = objectI.StackHeight + 1
                        objectI = objectN
                    
                    n -= 1
            
            elif(isinstance(objectI, Slider)):
                while(n - 1 >= startIndex):
                    objectN = self.beatmap.HitObjects[n]
                    if(isinstance(objectN, Spinner)):
                        continue

                    if(objectI.StartTime - objectN.StartTime > stackThreshold):
                        break

                    if(isinstance(objectN, HitCircle)):
                        objectNEndPosition = objectN.Position
                    else:
                        objectNEndPosition = objectN.EndPosition

                    if(objectNEndPosition.distance(objectI.Position) < stack_distance):
                        objectN.StackHeight = objectI.StackHeight + 1
                        objectI = objectN

                    n -= 1
    
    def getCircleSize(self, mods):
        if("HR" in mods):
            return min(self.beatmap.Difficulty["CircleSize"] * 1.3, 10)
        if("EZ" in mods):
            return self.beatmap.Difficulty["CircleSize"] * 0.5
        return self.beatmap.Difficulty["CircleSize"]