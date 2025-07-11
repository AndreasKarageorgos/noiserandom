from noiseRandom import NoiseRandom
from os import path,mkdir


path = "/media/andreas/images"
try:
    #mkdir(path)
    print("ok")
except FileExistsError:
    pass

nRandom = NoiseRandom(path=path,strength=10)

random_number = nRandom.randomInt()

print(random_number)