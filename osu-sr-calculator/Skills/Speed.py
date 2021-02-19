from .Skill import Skill
from ..Objects.osu.HitObjects.DifficultyHitObject import DifficultyHitObject
from math import pi, sin

class Speed(Skill):
    angle_bonus_begin = 5 * pi / 6
    pi_over_4 = pi / 4
    pi_over_2 = pi / 2

    SkillMultiplier = 1400
    StrainDecayBase = 0.3

    min_speed_bonus = 75
    max_speed_bonus = 45
    speed_balancing_factor = 40

    def strainValueOf(self, currentObject):
        distance = min(self.SINGLE_SPACING_THRESHOLD, currentObject.TravelDistance + currentObject.JumpDistance)
        deltaTime = max(self.max_speed_bonus, currentObject.DeltaTime)

        speedBonus = 1.0
        if(deltaTime < self.min_speed_bonus):
            speedBonus = 1 + pow((self.min_speed_bonus - deltaTime) / self.speed_balancing_factor, 2)

        angleBonus = 1.0
        if(currentObject.Angle != None and currentObject.Angle > 0 and currentObject.Angle < self.angle_bonus_begin):
            angleBonus = 1 + pow(sin(1.5 * (self.angle_bonus_begin - currentObject.Angle)), 2) / 3.57
            if(currentObject.Angle < self.pi_over_2):
                angleBonus = 1.28
                if(distance < 90 and currentObject.Angle < self.pi_over_4):
                    angleBonus += (1 - angleBonus) * min((90 - distance) / 10, 1)
                elif(distance < 90):
                    angleBonus += (1 - angleBonus) * min((90 - distance) / 10, 1) * sin(self.pi_over_2 - currentObject.Angle) / self.pi_over_4
        
        returnValue = (1 + (speedBonus - 1) * 0.75) * angleBonus * (0.95 + speedBonus * pow(distance / self.SINGLE_SPACING_THRESHOLD, 3.5)) / currentObject.StrainTime
        return returnValue