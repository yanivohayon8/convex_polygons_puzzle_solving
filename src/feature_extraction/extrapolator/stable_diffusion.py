# from src.feature_extraction.pictorial import  image_edge,EdgePictorialExtractor
from src.feature_extraction.geometric import Extractor
from src.feature_extraction.pictorial import find_rotation_angle,trans_image
from src.piece import Piece
import numpy as np

class StableDiffusionExtrapolationExtractor(Extractor):
    
    def __init__(self, pieces,extrapolation_height=13):
        super().__init__(pieces)
        self.extrapolation_height = extrapolation_height

    def extract_for_piece(self, piece: Piece):
        piece.features[self.__class__.__name__] = []
        
        raw_coords = piece.raw_coordinates
        shifted_coords = piece.extrapolation_details.match_piece_to_img(raw_coords)
        

        for edge_index in range(len(shifted_coords)):

            img = get_edge_image(piece.extrapolated_img,
                                 shifted_coords,
                             edge_index,#piece.get_origin_index(edge_index),
                             self.extrapolation_height)
            
            piece.features[self.__class__.__name__].append(
                {
                    "original":img,
                    "flipped":np.flip(img,axis=(1))#np.flip(img,axis=(0,1))
                }
            )




def get_edge_image(extrapolation_img:np.ndarray,original_coordinates:list,edge_index:int,extrapolation_height:int):
    next_edge_index = (edge_index+1)%len(original_coordinates)
    angle = find_rotation_angle(original_coordinates,edge_index,next_edge_index)
    edge_row = original_coordinates[edge_index][1]
    edge_col = original_coordinates[edge_index][0]
    next_edge_row = original_coordinates[next_edge_index][1]
    next_edge_col = original_coordinates[next_edge_index][0]
    edge_width = int(np.sqrt((edge_col-next_edge_col)**2 + (edge_row-next_edge_row)**2)) #abs(curr_col-next_col)
    translated_img = trans_image(extrapolation_img,edge_col,edge_row,angle,edge_row,edge_col)

    non_background_indices = np.argwhere(np.any(translated_img != [0,0,0],axis=2))
    min_row,min_col = np.min(non_background_indices,axis=0)

    return translated_img[:extrapolation_height,min_col:min_col+edge_width]