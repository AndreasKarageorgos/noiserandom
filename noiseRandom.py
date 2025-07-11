from os import walk,sep,remove
from captureImage import captureImage
from secrets import choice
from hashlib import sha512

class NoiseRandom():
    
    def __init__(self,path:str,strength=1):
        self.path = path
        self.images = []
        self.strength = strength
        if(self.strength<1):
            self.strength = 1
        

    def randomInt(self):
        self.captureImages()
        with open(choice(self.images), "rb") as f:
            data = f.read()
            f.close()
        #self.deleteImages()
        starting_image_index = data.find(b"\xFF\xDA")
        ending_image_index = data.find(b"\xFF\xD9")
        digest = sha512(data[starting_image_index+1:ending_image_index]).digest()
        return int.from_bytes(digest)

    def deleteImages(self):
        for image_path in self.images:
            remove(image_path)
        self.images.clear()

    def captureImages(self):
        self.images = self.images + captureImage(self.path,self.strength)
        