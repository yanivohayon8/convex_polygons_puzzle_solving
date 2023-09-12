import numpy as np
import cv2 
from src.feature_extraction.geometric import Extractor
from src.piece import Piece



class EdgePictorialExtractor(Extractor):
    def __init__(self, pieces,sampling_height=10):
        super().__init__(pieces)
        self.sampling_height = sampling_height

    def extract_for_piece(self,piece:Piece): 
        piece.features[self.__class__.__name__] = []
        
        images_not_ordered = []

        for edge_index in range(piece.get_num_coords()):

            img = image_edge(piece.img,piece.coordinates,piece.get_origin_index(edge_index),
                             self.sampling_height)
            # images_not_ordered.append(
            piece.features[self.__class__.__name__].append(
                {
                    "original":img,
                    "flipped":np.flip(img,axis=(1))#np.flip(img,axis=(0,1))
                }
            )
        
        '''Tfira because of _preprocess in puzzle.py
        make the edge_length feature correspond in the indices to the images'''
        # ordering_indexes = [piece.get_origin_index(i) for i in range(piece.get_num_coords())]
        # piece.features[self.__class__.__name__] = [x for _,x in zip(ordering_indexes,images_not_ordered)]
        


class EdgePictorialAndNormalizeExtractor(EdgePictorialExtractor):

    def run(self):
        super().run()
        images = []
        channels_sum = np.zeros((3,1))
        pixels_count = 0

        # Do we have a RISK for numerical instability here?

        for piece in self.pieces:
            for edge  in range(piece.get_num_coords()):
                img = piece.features[self.__class__.__name__][edge]["original"]
                channels_sum += np.sum(img,axis=(0,1)).reshape(3,1) 
                pixels_count+= img.shape[0]*img.shape[1]

        channels_mean = (channels_sum/pixels_count).astype(np.int).T
        
        for piece in self.pieces:
            for edge  in range(piece.get_num_coords()): # ["original","flipped"]
                for key_ in piece.features[self.__class__.__name__][edge].keys():
                    img_correct_type = piece.features[self.__class__.__name__][edge][key_].astype(np.int)
                    piece.features[self.__class__.__name__][edge][key_] = img_correct_type - channels_mean


class EdgePictorialExtractorOnExtrapolation(EdgePictorialExtractor):

    def __init__(self, pieces,outward_distance, sampling_height=10):
        super().__init__(pieces, sampling_height)
        self.outward_distance = outward_distance

    def extract_for_piece(self, piece: Piece):
        piece.features[self.__class__.__name__] = []
        
        outwarded_polygon =  piece.push_original_coordinates(self.outward_distance)# corresponds to params.txt #self.sampling_height
        outwarded_coordinates = outwarded_polygon.exterior.coords[:-1]

        for edge_index in range(len(outwarded_coordinates)):

            img = image_edge(piece.extrapolated_img,outwarded_coordinates,piece.get_origin_index(edge_index),
                             self.sampling_height)
            # images_not_ordered.append(
            piece.features[self.__class__.__name__].append(
                {
                    "original":img,
                    "flipped":np.flip(img,axis=(1))#np.flip(img,axis=(0,1))
                }
            )


def find_rotation_angle(piece_coordinates:list,edge_index:int,next_edge_index:int):
    edge_row = piece_coordinates[edge_index][1]
    edge_col = piece_coordinates[edge_index][0]
    next_edge_row = piece_coordinates[next_edge_index][1]
    next_edge_col = piece_coordinates[next_edge_index][0]
    angle = np.arctan((next_edge_row-edge_row)/(next_edge_col-edge_col))*180/np.pi

    if next_edge_col-edge_col < 0:
        angle +=180
    
    return angle

def padd_image_before_translate(img:np.array,edge_width):
    num_row_padded = 0
        
    if edge_width>img.shape[0]:
        num_row_padded = edge_width - img.shape[0]
    
    num_col_padded = 0
    
    if edge_width>img.shape[1]:
        num_col_padded = edge_width - img.shape[1]

    return np.pad(img,((0,num_row_padded),(0,num_col_padded),(0,0)),constant_values=0)

def image_edge(img:np.ndarray,piece_coordinates:list,edge_index:int,sampling_height:int):
    next_edge_index = (edge_index+1)%len(piece_coordinates)
    edge_row = piece_coordinates[edge_index][1]
    edge_col = piece_coordinates[edge_index][0]
    next_edge_row = piece_coordinates[next_edge_index][1]
    next_edge_col = piece_coordinates[next_edge_index][0]
    edge_width = int(np.sqrt((edge_col-next_edge_col)**2 + (edge_row-next_edge_row)**2)) #abs(curr_col-next_col)
    angle = np.arctan((next_edge_row-edge_row)/(next_edge_col-edge_col))*180/np.pi

    if next_edge_col-edge_col < 0:
        angle +=180
    
    num_row_padded = 0
        
    if edge_width>img.shape[0]:
        num_row_padded = edge_width - img.shape[0]
    
    num_col_padded = 0
    
    if edge_width>img.shape[1]:
        num_col_padded = edge_width - img.shape[1]

    img_padded = np.pad(img,((0,num_row_padded),(0,num_col_padded),(0,0)),constant_values=0)
    img_translated_shift_down = trans_image(img_padded,edge_col,edge_row,angle,edge_row-sampling_height,edge_col)
    # img_translated_shift_down = trans_image(img_padded,edge_col,edge_row,angle,edge_row,edge_col)
    return img_translated_shift_down[:sampling_height,:edge_width]#[:sampling_height,:edge_width]



def trans_image(img,center_x,center_y,degrees,t_row,t_col,scale=1):
    shape = ( img.shape[1], img.shape[0] ) # cv2.warpAffine expects shape in (length, height)

    matrix = cv2.getRotationMatrix2D(center=(center_x,center_y), angle=degrees, scale=scale )
    matrix[0,2] -= t_col
    matrix[1,2] -= t_row
    image = cv2.warpAffine( src=img, M=matrix, dsize=shape )

    return image

