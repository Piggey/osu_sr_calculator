# osu_sr_calculator

Package to calculate star rating of any osu beatmap with any mod combination.

Updated on: 19.02.2021

## Disclaimer
calculated star ratings may be varying slightly from original values (margin of 0.01)

## Usage
```python
from osu_sr_calculator import calculateStarRating
starRating = calculateStarRating(returnAllDifficultyValues, filepath, map_id, mods, allCombinations)
```
calculateStarRating method accepts these parameters:

- returnAllDifficultyValues: returns total star rating value if False. when set to True, method will also return aim and speed difficulty
- filepath (optional if map_id is set): Path to .osu file
- map_id (optional if filepath is set): BeatmapID number of a beatmap
- mods (optional): Specify which mods to include during star rating calculation
- allCombinations (optional): when set to True, will return star rating of every possible mod combination

## Examples
- local file nomod star rating:
```python
starRating = calculateStarRating(filepath='path/to/file.osu')
# Response: { 'nomod': x.xxxx }
```

- BeatmapID DT star rating:
```python
starRating = calculateStarRating(map_id=123456, mods=['DT'])
# Response: { 'DT': x.xxxx }
```

- All possible star ratings:
```python
starRatings = calculateStarRating(filepath='path/to/file.osu', allCombinations=True)
# Response:
# {
#     nomod: x.xxxx,
#     DT: x.xxxx,
#     HT: x.xxxx,
#     HR: x.xxxx,
#     HRDT: x.xxxx,
#     HRHT: x.xxxx,
#     EZ: x.xxxx,
#     EZDT: x.xxxx,
#     EZHT: x.xxxx,
# }
```

- Aim and Speed ratings:
```python
starRatings = calculateStarRating(filepath='path/to/file.osu', returnAllDifficultyValues=True)
# Response:
# {
#     nomod: {
#         aim: x.xxxx,
#         speed: x.xxxx,
#         total: x.xxxx,
#     }
# }
```