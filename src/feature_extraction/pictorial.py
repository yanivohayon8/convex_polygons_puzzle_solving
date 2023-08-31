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
            img = image_edge(piece.img,piece.coordinates,edge_index,self.sampling_height)
            images_not_ordered.append(
                {
                    "original":img,
                    "flipped":np.flip(img,axis=(1))#np.flip(img,axis=(0,1))
                }
            )
        
        '''Tfira because of _preprocess in puzzle.py
        make the edge_length feature correspond in the indices to the images'''
        ordering_indexes = [piece.get_origin_index(i) for i in range(piece.get_num_coords())]
        piece.features[self.__class__.__name__] = [x for _,x in zip(ordering_indexes,images_not_ordered)]



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
    return img_translated_shift_down[:sampling_height,:edge_width]



def trans_image(img,center_x,center_y,degrees,t_row,t_col,scale=1):
    shape = ( img.shape[1], img.shape[0] ) # cv2.warpAffine expects shape in (length, height)

    matrix = cv2.getRotationMatrix2D(center=(center_x,center_y), angle=degrees, scale=scale )
    matrix[0,2] -= t_col
    matrix[1,2] -= t_row
    image = cv2.warpAffine( src=img, M=matrix, dsize=shape )

    return image

