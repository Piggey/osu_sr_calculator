from .Skill import Skill
from math import log10

class OsuStrainSkill(Skill):

    ReducedSectionCount = 10
    ReducedStrainBaseline = 0.75
    DifficultyMultiplier = 1.06

    def __init__(self):
        super().__init__()
        self.ReducedSectionCount = 10
        self.ReducedStrainBaseline = 0.75
        self.DifficultyMultiplier = 1.06

    def difficultyValue(self):
        self.strainPeaks.sort(reverse=True)

        difficulty = 0
        weight = 1

        for i in range(min(self.ReducedSectionCount, len(self.strainPeaks))):
            scale = log10(1.0 + 9.0 * (float(i) / self.ReducedSectionCount))
            self.strainPeaks[i] *= self.ReducedStrainBaseline + scale * (1.0 - self.ReducedStrainBaseline)

        self.strainPeaks.sort(reverse=True)
        for strain in self.strainPeaks:
            difficulty += strain * weight
            weight *= 0.9

        return difficulty * self.DifficultyMultiplier