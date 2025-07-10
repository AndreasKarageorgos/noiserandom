from quantumRandom import QuantumRandom
from os import path,mkdir


path = "images"
try:
    mkdir(path)
except FileExistsError:
    pass

qRandom = QuantumRandom(path=path)

random_number = qRandom.randomInt()

print(random_number)