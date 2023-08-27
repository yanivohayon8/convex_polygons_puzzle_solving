from PIL import Image
from PIL import ImageDraw
import numpy as np
import cv2
from src.feature_extraction.geometric import Extractor
from src.piece import Piece

class LamaEdgeExtrapolator(Extractor):

    def __init__(self, pieces,samling_width=10):
        super().__init__(pieces)
        self.sampling_width = samling_width
    
    def extract_for_piece(self,piece:Piece):
        piece.features["edges_extrapolated_lama"] = []
        coords = [(int(coord[0]),int(coord[1])) for coord in piece.coordinates + [piece.coordinates[0]]]
        debug_masked_images = []

        for prev_coord,next_coord in zip(coords[:-1],coords[1:]):
            masked_image,line_pixels = mask_line(piece.extrapolated_img,prev_coord,next_coord,self.sampling_width)
            piece.features["edges_extrapolated_lama"].append(line_pixels)
            debug_masked_images.append(masked_image)
        
        return debug_masked_images



def mask_line(image:np.array, start_point, end_point, width):
    mask = np.zeros_like(image)
    cv2.line(mask,start_point,end_point,(1,1,1),width)
    masked_image = image.copy() #cv2.bitwise_and(image,mask)
    masked_image[mask==0] = 0
    line_pixels = np.argwhere(masked_image!=0)
    return masked_image,line_pixels
