from ..Objects.osu.HitObjects.DifficultyHitObject import DifficultyHitObject
from ..Objects.osu.HitObjects.Spinner import Spinner
from abc import ABC

class Skill(ABC):
    SINGLE_SPACING_THRESHOLD = 125
    STREAM_SPACING_THRESHOLD = 110

    def __init__(self):
        self.Previous = [] # array of DifficultyHitObject

        self.currentStrain = 1
        self.currentSectionPeak = 1
        self.strainPeaks = []

        self.SkillMultiplier = None
        self.StrainDecayBase = None

    def saveCurrentPeak(self):
        if(len(self.Previous) > 0):
            self.strainPeaks.append(self.currentSectionPeak) 

    def startNewSectionFrom(self, offset):
        if(len(self.Previous) > 0):
            self.currentSectionPeak = self.currentStrain * self.strainDecay(offset - self.Previous[0].CurrentObject.StartTime)

    def process(self, currentObject):
        self.currentStrain *= self.strainDecay(currentObject.DeltaTime)
        if(not isinstance(currentObject.CurrentObject, Spinner)):
            self.currentStrain += self.strainValueOf(currentObject) * self.SkillMultiplier

        self.currentSectionPeak = max(self.currentStrain, self.currentSectionPeak)

        self.addToHistory(currentObject)

    def difficultyValue(self):
        self.strainPeaks.sort(reverse=True)

        difficulty = 0
        weight = 1

        for strain in self.strainPeaks:
            difficulty += strain * weight
            weight *= 0.9

        return difficulty

    def strainValueOf(self, currentObject):
        pass

    def strainDecay(self, ms):
        return pow(self.StrainDecayBase, ms / 1000)

    def addToHistory(self, currentObject):
        self.Previous.insert(0, currentObject)
        if(len(self.Previous) > 2):
            self.Previous.pop()