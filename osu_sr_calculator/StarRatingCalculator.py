from .Objects.osu.HitObjects.DifficultyHitObject import DifficultyHitObject
from .Skills.Aim import Aim
from .Skills.Speed import Speed
from math import ceil, sqrt

class StarRatingCalculator(object):
    hitObjects = []
    section_length = 400
    difficlty_multiplier = 0.0675

    def calculate(self, hitObjects, timeRate):
        self.hitObjects = hitObjects
        aimSkill = Aim()
        speedSkill = Speed()

        sectionLength = self.section_length * timeRate

        currentSectionEnd = ceil((self.hitObjects[0].StartTime if hitObjects[0] is not None else 0) / sectionLength) * sectionLength

        for h in hitObjects:
            while(h.CurrentObject.StartTime > currentSectionEnd):
                aimSkill.saveCurrentPeak()
                aimSkill.startNewSectionFrom(currentSectionEnd)

                speedSkill.saveCurrentPeak()
                speedSkill.startNewSectionFrom(currentSectionEnd)

                currentSectionEnd += sectionLength

            aimSkill.process(h)
            speedSkill.process(h)
        
        aimSkill.saveCurrentPeak()
        speedSkill.saveCurrentPeak()

        aimRating = sqrt(aimSkill.difficultyValue()) * self.difficlty_multiplier
        speedRating = sqrt(speedSkill.difficultyValue()) * self.difficlty_multiplier
        starRating = aimRating + speedRating + abs(aimRating - speedRating) / 2
        return {
            "aim": aimRating,
            "speed": speedRating,
            "total": starRating
        }