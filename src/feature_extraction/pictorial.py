import numpy as np

class PixelEnviormnetExtractor():

    def __init__(self) -> None:
        pass

    def pad_img(self,img, width):
        return np.pad(img,width)

    def get_pixel_env(self,img, center_x:int,center_y:int,radius:int,is_repad_img = False):
        '''
            center - the pixel around to compute the enviorment
            radius - how far going from the center...
        '''
        padded_img = img

        if is_repad_img or self.padded_img is None:
             padded_img = self.pad_img(radius)
        

        return padded_img[center_x-radius:center_x+radius,center_y-radius:radius+center_y]

