import cv2
from os import sep
from random import randint
from secrets import choice,randbits
from time import sleep



def captureImage(path,total_images=1,camera=0):
    image_names = []
    cap = cv2.VideoCapture(camera)

    if not cap.isOpened():
        raise Exception("Cannot open camera")

    ret,frame = cap.read()
    sleep((1 + 1/(randbits(6)+0.000001))) #Waits for the cam to open.
    for i in range(total_images):
        if not ret:
            raise Exception("Can't receive frame (stream end?). Exiting ...")
        else:
            ret,frame = cap.read()
            # Save the captured image
            image_name = path + sep + str(i) + ".jpg"
            image_names.append(image_name)
            cv2.imwrite(image_name, frame)
    cap.release()
    cv2.destroyAllWindows()
    return image_names


if __name__ == "__main__":
    captureImage("images")