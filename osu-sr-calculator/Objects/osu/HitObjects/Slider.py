from .HitObject import HitObject
from ...Vector2 import Vector2
from ....SliderPath import SliderPath
from .HitCircle import HitCircle
from .SliderObjects.HeadCircle import HeadCircle
from .SliderObjects.TailCircle import TailCircle
from .SliderObjects.SliderTick import SliderTick
from .SliderObjects.RepeatPoint import RepeatPoint
from functools import cmp_to_key

class Slider(HitObject):
    EndPosition = None
    EndTime = None
    Duration = None
    Path = None
    RepeatCount = None
    NestedHitObjects = []
    TickDistance = None
    LazyEndPosition = None
    LazyTravelDistance: None
    SpanDuration: None
    LegacyLastTickOffset = 36
    HeadCircle = None
    TailCircle = None
    
    Velocity = None
    SpanCount = None

    def __init__(self, pos, startTime, path, repeatCount, speedMultiplier, beatLength, mapDifficulty, radius):
        super().__init__(pos, startTime, radius=radius)
        self.Path = path
        self.EndPosition = self.Position.add(self.Path.PositionAt(1))

        self.__calculateEndTimeAndTickDistance(speedMultiplier, beatLength, mapDifficulty, repeatCount, startTime, path.expectedDistance)
        self.Duration = self.EndTime - startTime
        self.RepeatCount = repeatCount

        self.__createNestedHitObjects()
    
    def __calculateEndTimeAndTickDistance(self, speedMultiplier, beatLength, mapDifficulty, repeatCount, startTime, expectedDistance):
        scoringDistance = 100 * mapDifficulty['SliderMultiplier'] * speedMultiplier
        self.Velocity = scoringDistance / beatLength
        self.SpanCount = repeatCount + 1
        self.TickDistance = scoringDistance / mapDifficulty['SliderTickRate'] # there was a '* 1' here but honestly i dont know why would it be there
        self.EndTime = startTime + self.SpanCount * expectedDistance / self.Velocity

    def __createNestedHitObjects(self):
        self.NestedHitObjects = []

        self.__createSliderEnds()
        self.__createSliderTicks()
        self.__createRepeatPoints()

        self.NestedHitObjects = sorted(self.NestedHitObjects, key=cmp_to_key(lambda a, b: a.StartTime - b.StartTime))

        self.TailCircle.StartTime = max(self.StartTime + self.Duration / 2, self.TailCircle.StartTime - self.LegacyLastTickOffset)

    def __createSliderEnds(self):
        self.HeadCircle = HeadCircle(self.Position, self.StartTime, radius=self.Radius)
        self.TailCircle = TailCircle(self.EndPosition, self.EndTime, radius=self.Radius)

        self.NestedHitObjects.append(self.HeadCircle)
        self.NestedHitObjects.append(self.TailCircle)

    def __createSliderTicks(self):
        max_length = 100000

        length = min(max_length, self.Path.expectedDistance)
        tickDistance = min(max(self.TickDistance, 0), length)

        if(tickDistance == 0):
            return
        
        minDistanceFromEnd = self.Velocity * 10
        self.SpanDuration = self.Duration / self.SpanCount

        for span in range(self.SpanCount):
            spanStartTime = self.StartTime + span * self.SpanDuration
            Reversed = span % 2 == 1

            # for d in range(tickDistance, (length + 1), tickDistance):
            #     if(d > length - minDistanceFromEnd):
            #         break

            #     distanceProgress = d / length
            #     timeProgress = 1 - distanceProgress if Reversed else distanceProgress
            #     sliderTickPosition = self.Position.add(self.Path.PositionAt(distanceProgress))
            #     sliderTick = SliderTick(sliderTickPosition, spanStartTime + timeProgress * self.SpanDuration, span, spanStartTime, radius=self.Radius)
            #     self.NestedHitObjects.append(sliderTick)

            d = tickDistance
            while(d <= length):
                if(d > length - minDistanceFromEnd):
                    break

                distanceProgress = d / length
                timeProgress = 1 - distanceProgress if Reversed else distanceProgress
                sliderTickPosition = self.Position.add(self.Path.PositionAt(distanceProgress))
                sliderTick = SliderTick(sliderTickPosition, spanStartTime + timeProgress * self.SpanDuration, span, spanStartTime, radius=self.Radius)
                self.NestedHitObjects.append(sliderTick)

                d += tickDistance
    
    def __createRepeatPoints(self):
        for repeatIndex in range(self.RepeatCount):
            repeat = repeatIndex + 1
            repeatPosition = self.Position.add(self.Path.PositionAt(repeat % 2))
            repeatPoint = RepeatPoint(repeatPosition, self.StartTime + repeat * self.SpanDuration, repeatIndex, self.SpanDuration, radius=self.Radius)
            self.NestedHitObjects.append(repeatPoint)