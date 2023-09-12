# from src.feature_extraction.pictorial import  image_edge,EdgePictorialExtractor
from src.feature_extraction.geometric import Extractor
from src.feature_extraction.pictorial import find_rotation_angle,trans_image
from src.piece import Piece
import numpy as np

class SDExtrapolatorExtractor(Extractor):
    
    def __init__(self, pieces,extrapolation_height=13):
        super().__init__(pieces)
        self.extrapolation_height = extrapolation_height

    def extract_for_piece(self, piece: Piece):
        piece.features[self.__class__.__name__] = []
        
        raw_coords = piece.raw_coordinates
        shifted_coords = piece.extrapolation_details.match_piece_to_img(raw_coords)
        

        for edge_index_ in range(len(shifted_coords)):
            edge_index = piece.get_origin_index(edge_index_)

            next_edge_index = (edge_index+1)%len(shifted_coords)
            angle = find_rotation_angle(shifted_coords,edge_index,next_edge_index)
            edge_row = shifted_coords[edge_index][1]
            edge_col = shifted_coords[edge_index][0]
            next_edge_row = shifted_coords[next_edge_index][1]
            next_edge_col = shifted_coords[next_edge_index][0]
            edge_width = int(np.sqrt((edge_col-next_edge_col)**2 + (edge_row-next_edge_row)**2)) #abs(curr_col-next_col)
            translated_img = trans_image(piece.extrapolated_img,edge_col,edge_row,angle,edge_row,edge_col)

            non_background_indices = np.argwhere(np.any(translated_img != [0,0,0],axis=2))
            min_row,min_col = np.min(non_background_indices,axis=0)
            max_row,max_col = np.max(non_background_indices,axis=0)

            img = translated_img[:self.extrapolation_height,min_col:min_col+edge_width]
            # img = translated_img[:max_row,min_col:min_col+edge_width]

            piece.features[self.__class__.__name__].append(
                {
                    "same":img,
                    "flipped":np.flip(img,axis=(0))#np.flip(img,axis=(0,1))
                }
            )

class SDOriginalExtractor(Extractor):
    
    def __init__(self, pieces,sampling_height=13):
        super().__init__(pieces)
        self.sampling_height = sampling_height

    def extract_for_piece(self, piece: Piece):
        piece.features[self.__class__.__name__] = []
    
        raw_coords = piece.raw_coordinates
        shifted_coords = piece.extrapolation_details.match_piece_to_img(raw_coords)
        
        for edge_index_ in range(len(shifted_coords)):
            edge_index = piece.get_origin_index(edge_index_)

            next_edge_index = (edge_index+1)%len(shifted_coords)
            angle = find_rotation_angle(shifted_coords,edge_index,next_edge_index)
            edge_row = shifted_coords[edge_index][1]
            edge_col = shifted_coords[edge_index][0]
            next_edge_row = shifted_coords[next_edge_index][1]
            next_edge_col = shifted_coords[next_edge_index][0]
            edge_width = int(np.sqrt((edge_col-next_edge_col)**2 + (edge_row-next_edge_row)**2)) #abs(curr_col-next_col)
            translated_img = trans_image(piece.stable_diffusion_original_img,
                                         edge_col,edge_row,angle,edge_row-self.sampling_height,edge_col)

            non_background_indices = np.argwhere(np.any(translated_img != [0,0,0],axis=2))
            min_row,min_col = np.min(non_background_indices,axis=0)
            img = translated_img[:self.sampling_height,min_col:min_col+edge_width]

            piece.features[self.__class__.__name__].append(
                {
                    "same":img,
                    "flipped":np.flip(img,axis=(0,1))#np.flip(img,axis=(0,1))
                }
            )

class NormalizeSDExtrapolatorExtractor(SDExtrapolatorExtractor):

    def run(self):
        super().run()
        channels_sum = np.zeros((3,1))
        pixels_count = 0

        # Do we have a RISK for numerical instability here?

        for piece in self.pieces:
            for edge  in range(piece.get_num_coords()):
                img = piece.features[self.__class__.__name__][edge]["same"]
                channels_sum += np.sum(img,axis=(0,1)).reshape(3,1) 
                pixels_count+= img.shape[0]*img.shape[1]

        channels_mean = (channels_sum/pixels_count).astype(np.int).T
        
        for piece in self.pieces:
            for edge  in range(piece.get_num_coords()): # ["original","flipped"]
                for key_ in piece.features[self.__class__.__name__][edge].keys():
                    img_correct_type = piece.features[self.__class__.__name__][edge][key_].astype(np.int)
                    piece.features[self.__class__.__name__][edge][key_] = img_correct_type - channels_mean


class NormalizeSDOriginalExtractor(SDOriginalExtractor):

    def run(self):
        super().run()
        channels_sum = np.zeros((3,1))
        pixels_count = 0

        # Do we have a RISK for numerical instability here?

        for piece in self.pieces:
            for edge  in range(piece.get_num_coords()):
                img = piece.features[self.__class__.__name__][edge]["same"]
                channels_sum += np.sum(img,axis=(0,1)).reshape(3,1) 
                pixels_count+= img.shape[0]*img.shape[1]

        channels_mean = (channels_sum/pixels_count).astype(np.int).T
        
        for piece in self.pieces:
            for edge  in range(piece.get_num_coords()): # ["original","flipped"]
                for key_ in piece.features[self.__class__.__name__][edge].keys():
                    img_correct_type = piece.features[self.__class__.__name__][edge][key_].astype(np.int)
                    piece.features[self.__class__.__name__][edge][key_] = img_correct_type - channels_mean
