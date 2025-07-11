from os import walk,sep,remove
from captureImage import captureImage
from secrets import choice,randbits
from hashlib import sha512
import sys


class NoiseRandom():
    
    def __init__(self,path:str,strength=1,cameras=[0]):
        self.path = path
        self.images = []
        self.cameras = cameras
        self.strength = strength
        if(self.strength<1):
            self.strength = 1
        

    def randomInt(self) -> int:
        self.__captureImages()
        with open(choice(self.images), "rb") as f:
            data = f.read()
            f.close()
        self.__deleteImages()
        starting_image_index = data.find(b"\xFF\xDA")
        ending_image_index = data.find(b"\xFF\xD9")
        data = self.__scramble(data[starting_image_index+1:ending_image_index])
        
        
        sys.set_int_max_str_digits(len(data) * 3)
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

    def randomBytes(self,bytes:int) -> int:
        random_number = self.randomInt()
        num_bytes = (random_number.bit_length() + 7) //8
        big_num_bytes = random_number.to_bytes(num_bytes,"big")

        random_bytes = [choice(big_num_bytes) for _ in range(bytes)]
        new_int =  int.from_bytes(random_bytes,"big")

        new_int |= (1<<bytes*8-1)
        return new_int

    def __deleteImages(self) -> None:
        for image_path in self.images:
            remove(image_path)
        self.images.clear()

    def __captureImages(self) -> None:
        for camera in self.cameras:
            self.images = self.images + captureImage(self.path,self.strength,camera=camera)

    def __scramble(self,data):
        byte_list = list(data)
        data_size = len(byte_list)
        scrambled_data = b""
        for i in range(data_size*3):
            p1 = randbits(4*8) % data_size
            p2 = randbits(4*8) % data_size

            byte_list[p1], byte_list[p2] = byte_list[p2], byte_list[p1]

        for byte in byte_list:
            scrambled_data += byte.to_bytes()
        
        return scrambled_data