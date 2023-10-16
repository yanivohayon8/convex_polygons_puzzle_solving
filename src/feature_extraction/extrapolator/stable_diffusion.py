# from src.feature_extraction.pictorial import  image_edge,EdgePictorialExtractor
from typing import Any
from src.feature_extraction import Extractor,factory
from src.feature_extraction.pictorial import find_rotation_angle,trans_image
from src.piece import Piece
import numpy as np
from src.feature_extraction import image_process

class SDEdgeImageExtractor(Extractor):
    
    def __init__(self, pieces,feature_name):
        super().__init__(pieces)
        self.feature_name = feature_name
    
    def _translate_edge(self,piece,angle,edge_row,edge_col,next_edge_row,next_edge_col):
        raise NotImplementedError("Implement me")

    def extract_for_piece(self, piece: Piece):
        piece.features[self.feature_name] = []
        shifted_coords = piece.extrapolation_details.match_piece_to_img(piece.raw_coordinates)
        
        for edge_index_ in range(len(shifted_coords)):
            edge_index = piece.get_origin_index(edge_index_)

            next_edge_index = (edge_index+1)%len(shifted_coords)
            angle = find_rotation_angle(shifted_coords,edge_index,next_edge_index)
            edge_row = shifted_coords[edge_index][1]
            edge_col = shifted_coords[edge_index][0]
            next_edge_row = shifted_coords[next_edge_index][1]
            next_edge_col = shifted_coords[next_edge_index][0]
            translated_img = self._translate_edge(piece,angle,
                                                  edge_row,edge_col,
                                                  next_edge_row,next_edge_col) 
            
            edge_width = int(np.sqrt((edge_col-next_edge_col)**2 + (edge_row-next_edge_row)**2)) #abs(curr_col-next_col)
            non_background_indices = np.argwhere(np.any(translated_img != [0,0,0],axis=2))
            max_row,max_col = np.max(non_background_indices,axis=0)
            min_row,min_col = np.min(non_background_indices,axis=0)
            cropped_img = translated_img[min_row:max_row,:edge_width]
            
            piece.features[self.feature_name].append(cropped_img)


class SDExtrapolatorExtractor(SDEdgeImageExtractor):
    
    def __init__(self, pieces):
        super().__init__(pieces, self.__class__.__name__)

    def _translate_edge(self,piece, angle, edge_row, edge_col, next_edge_row, next_edge_col):
        return trans_image(getattr(piece,"extrapolated_img") ,edge_col,edge_row,angle,edge_row,edge_col)


class SDOriginalExtractor(SDEdgeImageExtractor):
    
    def __init__(self, pieces):
        super().__init__(pieces,self.__class__.__name__)

    def _translate_edge(self, piece, angle, edge_row, edge_col, next_edge_row, next_edge_col):
        img = getattr(piece,"stable_diffusion_original_img")
        # without it, the image is hidding above the left corner. See TestPocPictorial in test_old_feature_extraction.py
        # I am assuming the compatibility would crop this image to have smaller height than this...
        # this might cause troubles...
        shiftdown_offset = 13 
        return trans_image(img,edge_col,edge_row,angle,
                           edge_row-shiftdown_offset,edge_col)


class NormalizeSDOriginalExtractor(SDOriginalExtractor):

    def __init__(self, pieces,crop_num_rows=5):
        super().__init__(pieces)
        self.axes_flipped = (0,1)
        self.crop_num_rows = crop_num_rows

    def run(self):
        super().run()
        images_as_list = []        
        name = self.__class__.__name__

        for piece in self.pieces:
            for edge in range(piece.get_num_coords()):
                piece.features[name][edge] = image_process.filp_image(piece.features[name][edge],
                                                                      axes=self.axes_flipped)
                piece.features[name][edge] = image_process.crop_rows(piece.features[name][edge],
                                                                     num_rows=self.crop_num_rows)
                images_as_list.append(piece.features[name][edge])

        channels_mean = image_process.compute_non_zero_pixels_channels_mean(images_as_list)

        for piece in self.pieces:
            for edge in range(piece.get_num_coords()):
                as_double = piece.features[name][edge].astype(np.double)
                piece.features[name][edge] = as_double -  channels_mean


# class NormalizeSDExtrapolatorExtractor(SDExtrapolatorExtractor):

#     def run(self):
#         super().run()
#         channels_sum = np.zeros((3,1))
#         pixels_count = 0

#         # Do we have a RISK for numerical instability here?

#         for piece in self.pieces:
#             for edge  in range(piece.get_num_coords()):
#                 img = piece.features[self.__class__.__name__][edge]
#                 channels_sum += np.sum(img,axis=(0,1)).reshape(3,1) 
#                 pixels_count+= img.shape[0]*img.shape[1]

#         # channels_mean = (channels_sum/pixels_count).astype(np.int).T
#         channels_mean = (channels_sum/pixels_count).astype(np.double).T
        
#         for piece in self.pieces:
#             for edge  in range(piece.get_num_coords()):
#                 img_correct_type = piece.features[self.__class__.__name__][edge].astype(np.double)
#                 piece.features[self.__class__.__name__][edge] = img_correct_type - channels_mean


'''

    REGISTERING BUILDERS

'''
class extraBuilder():
    def __call__(self, pieces, **_ignored) -> Any:
        for piece in pieces:
            piece.load_extrapolated_image()

class SDExtrapolatorBuilder(extraBuilder):
    def __call__(self, pieces, **_ignored) -> Any:        
        super().__call__(pieces,**_ignored)
        return SDExtrapolatorExtractor(pieces)

# class NormalizeSDExtrapolatorBuilder(extraBuilder):
#     def __call__(self, pieces, **_ignored) -> Any:        
#         super().__call__(pieces,**_ignored)
#         return NormalizeSDExtrapolatorExtractor(pieces)

class OriginalBuilder():
    def __call__(self, pieces, **_ignored) -> Any:
        for piece in pieces:
            piece.load_stable_diffusion_original_image()

class SDOriginalBuilder(OriginalBuilder):
    def __call__(self, pieces, **_ignored) -> Any:        
        super().__call__(pieces,**_ignored)
        return SDOriginalExtractor(pieces)

class NormalizeSDOriginalBuilder(OriginalBuilder):
    def __call__(self, pieces, **_ignored) -> Any:        
        super().__call__(pieces,**_ignored)
        return NormalizeSDOriginalExtractor(pieces)

factory.register_builder(SDExtrapolatorExtractor.__name__,
                         SDExtrapolatorBuilder())
# factory.register_builder(NormalizeSDExtrapolatorExtractor.__name__,
#                          NormalizeSDExtrapolatorBuilder())
factory.register_builder(SDOriginalExtractor.__name__,
                         SDOriginalBuilder())
factory.register_builder(NormalizeSDOriginalExtractor.__name__,
                         NormalizeSDOriginalBuilder())