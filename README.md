# osu-sr-calculator

Package to calculate star rating of any osu beatmap with any mod combination.

Updated on: 19.02.2021

## Usage
```python
from osu-sr-calculator import calculateStarRating
starRating = calculateStarRating(returnAllDifficultyValues, filepath, map_id, mods, allCombinations)
```
calculateStarRating method accepts these parameters:
> returnAllDifficultyValues: returns total star rating value if False. when set to True, method will also return aim and speed difficulty
> filepath (optional if map_id is set): Path to .osu file
> map_id (optional if filepath is set): BeatmapID number of a beatmap
> mods (optional): Specify which mods to include during star rating calculation
> allCombinations (optional): when set to True, will return star rating of every possible mod combination

## Examples
> nomod