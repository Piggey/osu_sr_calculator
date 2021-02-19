from .HitObjects.HitObject import HitObject

class Beatmap(object):
    Difficulty = {
        "HPDrainRate": None,
        "CircleSize": None,
        "OverallDifficulty": None,
        "ApproachRate": None,
        "SliderMultiplier": None,
        "SliderTickRate": None
    }

    HitObjects = []
    
    # public TimingPoints: Array<{
    #     Time: number,
    #     BeatLength: number,
    #     TimeSignature: number
    # }>;
    TimingPoints = []

    # public DifficultyTimingPoints: Array<{
    #     Time: number,
    #     SpeedMultiplier: number
    # }>;
    DifficultyTimingPoints = []

    Version = 0
    StackLeniency = 0

    def __init__(self):
        self.Difficulty = {
        "HPDrainRate": 0,
        "CircleSize": 0,
        "OverallDifficulty": 0,
        "ApproachRate": 0,
        "SliderMultiplier": 0,
        "SliderTickRate": 0
        }

        self.HitObjects = []
        self.TimingPoints = []
        self.DifficultyTimingPoints = []