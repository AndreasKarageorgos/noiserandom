from os import walk,sep,remove
from captureImage import captureImage
from secrets import choice
import sys

class NoiseRandom():
    
    def __init__(self,path:str,strength=1):
        self.path = path
        self.images = []
        self.strength = strength
        if(self.strength<1):
            self.strength = 1
        

    def randomInt(self) -> int:
        self.captureImages()
        with open(choice(self.images), "rb") as f:
            data = f.read()
            f.close()
        self.deleteImages()
        starting_image_index = data.find(b"\xFF\xDA")
        ending_image_index = data.find(b"\xFF\xD9")
        data = data[starting_image_index+1:ending_image_index]
        sys.set_int_max_str_digits(len(data) * 3)  #429496729
        return  int.from_bytes(data,"big")
    

    def random1024(self) -> int:
        random_number = self.randomInt()
        num_bytes = (random_number.bit_length() + 7) //8
        big_num_bytes = random_number.to_bytes(num_bytes,"big")

        random_bytes = [choice(big_num_bytes) for _ in range(128)]
        new_int =  int.from_bytes(random_bytes,"big")

        new_int |= (1<<128*8-1)
        return new_int

    def random2048(self) -> int:
        random_number = self.randomInt()
        num_bytes = (random_number.bit_length() + 7) //8
        big_num_bytes = random_number.to_bytes(num_bytes,"big")

        random_bytes = [choice(big_num_bytes) for _ in range(256)]
        new_int =  int.from_bytes(random_bytes,"big")

        new_int |= (1<<256*8-1)
        return new_int
    
    def random4096(self) -> int:
        random_number = self.randomInt()
        num_bytes = (random_number.bit_length() + 7) //8
        big_num_bytes = random_number.to_bytes(num_bytes,"big")

        random_bytes = [choice(big_num_bytes) for _ in range(512)]
        new_int =  int.from_bytes(random_bytes,"big")

        new_int |= (1<<512*8-1)
        return new_int


    def deleteImages(self):
        for image_path in self.images:
            remove(image_path)
        self.images.clear()

    def captureImages(self):
        self.images = self.images + captureImage(self.path,self.strength)
        