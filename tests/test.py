from osu_sr_calculator.main import calculateStarRating

for i in range(10):
    sr = calculateStarRating(filepath='/home/piggey/Projects/osu_sr_calculator/tests/test.osu')
    sr2 = calculateStarRating(filepath="/home/piggey/Projects/osu_sr_calculator/tests/test_copy.osu")
    print(f"mapa 1: {sr}")
    print(f"mapa 2: {sr2}")