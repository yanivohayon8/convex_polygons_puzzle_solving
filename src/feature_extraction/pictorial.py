import numpy as np
import cv2 


class PixelEnviormnetExtractor():

    def __init__(self) -> None:
        pass

    def pad_img(self,img, width):
        return np.pad(img,width)

    # def get_pixel_env(self,img, center_x:int,center_y:int,width:int,height,is_repad_img = False):
    #     '''
    #         center - the pixel around to compute the enviorment
    #         radius - how far going from the center...
    #     '''
    #     # padded_img = img

    #     # if is_repad_img or self.padded_img is None:
    #     #      padded_img = self.pad_img(img,radius)
        

    #     return img[center_x-radius:center_x+radius,center_y-radius:radius+center_y]

def slice_image(img,center_x,center_y,degrees,width,height,scale=1):
    shape = ( img.shape[1], img.shape[0] ) # cv2.warpAffine expects shape in (length, height)

    matrix = cv2.getRotationMatrix2D( center=(center_x,center_y), angle=degrees, scale=scale )
    image = cv2.warpAffine( src=img, M=matrix, dsize=shape )

    x = int( center_x - width/2  )
    y = int( center_y - height/2 )

    return image[  x:x+width,y:y+height ]#image[ y:y+height, x:x+width ]

    
