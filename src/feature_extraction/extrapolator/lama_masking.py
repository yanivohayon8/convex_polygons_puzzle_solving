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

class OriginalImgExtractor(Extractor):

    def __init__(self, pieces,extrapolator_samling_width=10):
        super().__init__(pieces)
        self.sampling_width = extrapolator_samling_width*2 # becuse part of the masking line overlapped with the background

    def extract_for_piece(self,piece:Piece): 
        piece.features["edges_pictorial_content"] = []
        coords = [(int(coord[0]),int(coord[1])) for coord in piece.coordinates + [piece.coordinates[0]]]
        debug_masked_images = []

        for prev_coord,next_coord in zip(coords[:-1],coords[1:]):
            img_rgb = cv2.cvtColor(piece.img,cv2.COLOR_RGBA2RGB)
            masked_image,line_pixels_with_background = mask_line(img_rgb,prev_coord,next_coord,self.sampling_width)

            line_pixels = line_pixels_with_background[line_pixels_with_background>0]

            piece.features["edges_pictorial_content"].append(line_pixels)
            debug_masked_images.append(masked_image)
        
        return debug_masked_images

def mask_line(image:np.array, start_point, end_point, width):
    mask = np.zeros_like(image)
    cv2.line(mask,start_point,end_point,(1,1,1),width)

    # masked_image = cv2.bitwise_and(image,mask)
    masked_image = image.copy() * mask
    # masked_image[mask==0] = 0
    # masked_image[np.all(mask==0,axis=1)] = 0

    # line_pixels = np.argwhere(masked_image!=0)
    line_pixels = masked_image[np.any(masked_image!=0,axis=2)]

    return masked_image,line_pixels
