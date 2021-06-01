from osu_sr_calculator.main import calculateStarRating

for i in range(10):
    sr = calculateStarRating(filepath='/home/piggey/Projects/osu_sr_calculator/tests/test.osu')
    print(sr)