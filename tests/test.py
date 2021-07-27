import sys
sys.path.append('../')
from osu_sr_calculator.main import calculateStarRating

sr = calculateStarRating(map_id = 1911308)
print(f"gwib [fiery]: {sr}")

for i in range(10):
    sr = calculateStarRating(filepath='test.osu')
    sr2 = calculateStarRating(filepath="test_copy.osu")
    print(f"mapa 1: {sr}")
    print(f"mapa 2: {sr2}")