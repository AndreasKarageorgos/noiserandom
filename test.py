from noiseRandom import NoiseRandom
from os import path,mkdir


path = "images"
try:
    mkdir(path)
except FileExistsError:
    pass

nRandom = NoiseRandom(path=path)

random_number = nRandom.randomInt()

print(random_number)