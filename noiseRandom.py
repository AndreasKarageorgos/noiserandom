from os import walk,sep,remove
from captureImage import captureImage
from secrets import choice,randbits
from hashlib import sha512
import sys
import numpy as np
from array import array


class NoiseRandom():
    
    def __init__(self,path:str,strength=1,cameras=[0]):
        self.path = path
        self.images = []
        self.cameras = cameras
        self.strength = strength
        if(self.strength<1):
            self.strength = 1
        

    def randomInt(self,getBytes=False)->int|bytes:
        self.__captureImages()
        with open(choice(self.images), "rb") as f:
            data = f.read()
            f.close()
        self.__deleteImages()
        if(getBytes):
            return data
        starting_image_index = data.find(b"\xFF\xDA")
        ending_image_index = data.find(b"\xFF\xD9")
        data = self.__scramble(data[starting_image_index+1:ending_image_index])
        sys.set_int_max_str_digits(len(data) * 3)
        return  int.from_bytes(data,"big")
    
    def random1024(self)->int:
        return self.randomBytes(1024//8)
    
    def random2048(self)->int:
        return self.randomBytes(2048//8)

    def random4096(self)->int:
        return self.randomBytes(4096//8)

    def randomBytes(self,total_bytes:int) -> int:
        random_pool = list(self.randomInt(True))
        selected_bytes = [choice(random_pool) & 0xFF for _ in range(total_bytes)]
        selected_bytes[0] |= (1<<7)
        for i in range(len(selected_bytes)):
            selected_bytes[i] = selected_bytes[i].to_bytes(1,byteorder="big",signed=False)
        selected_bytes = b"".join(selected_bytes)
        return int.from_bytes(selected_bytes,"big",signed=False)

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