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

    matrix = cv2.getRotationMatrix2D(center=(center_x,center_y), angle=degrees, scale=scale )
    image = cv2.warpAffine( src=img, M=matrix, dsize=shape )

    x = int( center_x - width/2  ) # switching because warpAffine?
    y = int( center_y - height/2 )

    return image[ y:y+height, x:x+width ]

def trans_image(img,center_x,center_y,degrees,t_row,t_col,scale=1):
    shape = ( img.shape[1], img.shape[0] ) # cv2.warpAffine expects shape in (length, height)

    matrix = cv2.getRotationMatrix2D(center=(center_x,center_y), angle=degrees, scale=scale )
    matrix[0,2] -= t_col
    matrix[1,2] -= t_row
    image = cv2.warpAffine( src=img, M=matrix, dsize=shape )

    return image

    
def rotate_and_crop(image, rectangle, angle):
    # Unpack the rectangle coordinates
    x1, y1, x2, y2 = rectangle
    
    cropped_image = image[y1:y2, x1:x2] # image coordinages are from top left
        
    # Get the center of the cropped image
    center = (int((x2 - x1) / 2), int((y2 - y1) / 2)) # 
    
    # Prepare the rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Perform the rotation
    rotated = cv2.warpAffine(cropped_image, M, (x2 - x1, y2 - y1))#  x and y "opposite according to the documentation"
    
    return rotated,cropped_image