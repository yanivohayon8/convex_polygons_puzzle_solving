import numpy as np

class PixelEnviormnetExtractor():
    
    def __init__(self,img) -> None:
        self.img = img
        self.padded_img = None

    def pad_img(self,width):
        self.padded_img = np.pad(self.img,width)

    def get_pixel_env(self,center_x:int,center_y:int,radius:int,is_repad_img = False):
        '''
            center - the pixel around to compute the enviorment
            radius - how far going from the center...
        '''

        if is_repad_img or self.padded_img is None:
             self.pad_img(radius)

        return self.padded_img[center_x-radius:center_x+radius,center_y-radius:radius+center_y]

