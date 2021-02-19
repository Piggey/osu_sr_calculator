from .OsuService import OsuService
from .BeatmapParser import BeatmapParser
from .DifficultyHitObjectCreator import DifficultyHitObjectCreator
from .StarRatingCalculator import StarRatingCalculator

osuService = OsuService()
beatmapParser = BeatmapParser()
difficultyHitObjectCreator = DifficultyHitObjectCreator()
starRatingCalculator = StarRatingCalculator()
Beatmap = None

def calculateStarRating(returnAllDifficultyValues = False, allCombinations = False, **kwargs):
    """Parameters:
    returnAllDifficultyValues = False
        returns total star rating value if False
        when set to True, method will also return aim and speed difficulty
        
    filepath: string
        path to .osu file (no need if map_id is set)

    map_id: integer
        BeatmapID number of a beatmap (no need if filepath is set)

    mods (optional): list of string
        Specify which mods to include during star rating calculation
        examples: 
            mods=['DT']
            mods=['EZ', 'HD', 'DT']
            mods=[]

    allCombinations = False
        when set to True, will return star rating of every possible mod combination
    """

    map_filepath = kwargs.get('filepath', None)
    map_id = kwargs.get('map_id', None)
    mods = kwargs.get('mods', None)
    allCombinations = kwargs.get('allCombinations', False)

    if(not map_filepath and not map_id):
        raise Exception('Neither BeatmapID nor beatmap filepath specified.')
    elif(map_id):
        Map = getOsuBeatmap(map_id)
    else:
        Map = getLocalOsuBeatmap(map_filepath)

    if(Map == None):
        raise Exception('No map found for specified map id. / wrong filepath')
    
    mods = parseMods(mods)
    output = {}
    if(not allCombinations):
        label = ''.join(mods) if len(mods) > 0 else "nomod"
        response = calculateNextModCombination(Map, mods, True)
        output[label] = response if returnAllDifficultyValues else response['total']
        return output
    else:
        allModCombinations = getAllModCombinations()
        for combi in allModCombinations:
            label = ''.join(combi['mods']) if len(combi['mods']) > 0 else 'nomod'
            response = calculateNextModCombination(Map, combi['mods'], combi['reParse'])
            output[label] = response if returnAllDifficultyValues else response['total']
        
        return output

def calculateNextModCombination(Map, mods, reParse):
    if(reParse):
        Beatmap = beatmapParser.parseBeatmap(Map, mods)

    timeRate = getTimeRate(mods)
    difficultyHitObjects = difficultyHitObjectCreator.convertToDifficultyHitObjects(Beatmap.HitObjects, timeRate)
    return starRatingCalculator.calculate(difficultyHitObjects, timeRate)

def getOsuBeatmap(map_id):
    return osuService.getOsuBeatmap(map_id)

def parseMods(mods):
    if(mods == None):
        return []
    return mods

def getTimeRate(mods):
    if("DT" in mods):
        return 1.5
    if("HT" in mods):
        return 0.75
    return 1

def getAllModCombinations():
    return [
        { 'mods': [], 'reParse': True },
        { 'mods': ['DT'], 'reParse': False },
        { 'mods': ['HT'], 'reParse': False },
        { 'mods': ['HR'], 'reParse': True },
        { 'mods': ['HR', 'DT'], 'reParse': False },
        { 'mods': ['HR', 'HT'], 'reParse': False },
        { 'mods': ['EZ'], 'reParse': True },
        { 'mods': ['EZ', 'DT'], 'reParse': False },
        { 'mods': ['EZ', 'HT'], 'reParse': False },
    ]

def getLocalOsuBeatmap(filePath):
    return open(filePath, 'r').read()