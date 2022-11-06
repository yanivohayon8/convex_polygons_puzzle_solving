import cv2
import numpy as np

class Frame():
    pass
    def __init__(self,size=(1024,1024,3),named_window="Vika"):
        self.img = np.zeros(size, np.unint8)
        self.named_window = named_window
        self.is_initialized = False

    def show(self):
        if not self.is_initialized:
            cv2.namedWindow(self.named_window)
        cv2.imshow(self.named_window,self.img)
    
    def destroy(self):
        cv2.destroyAllWindows()

