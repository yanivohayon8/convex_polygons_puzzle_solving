from shapely import Polygon
import numpy as np
from src.feature_extraction import Extractor
from src.piece import Piece

class EdgeLengthExtractor(Extractor):

    def _get_polygon_edges_lengths(self,coords):
        coords_prev = np.array(coords[:-1]).reshape(-1,2)
        coords_next = np.array(coords[1:]).reshape(-1,2)
        return np.sqrt(np.sum((coords_next-coords_prev)**2,axis=1))
    
    def extract_for_piece(self,piece:Piece):
        piece.features["edges_length"] =  self._get_polygon_edges_lengths(piece.get_coords())
    

class AngleLengthExtractor(Extractor):  

    def _get_angle_of_vectors_(self,coord_left,coord_middle,coord_right):
        vector_1 = np.array(coord_left-coord_middle)
        vector_2 = np.array(coord_right-coord_middle)
        dot = vector_1.dot(vector_2)
        denominator = (np.linalg.norm(vector_1) * np.linalg.norm(vector_2))
        return np.arccos(dot/denominator)

    def _get_polygon_angles(self,coords):
        num_coords = coords.shape[0]-1
        polygon_angles = [
            np.degrees(
                self._get_angle_of_vectors_(coords[(i-1)%num_coords],
                                           coords[i],
                                           coords[(i+1)%num_coords])
                ) for i in range(num_coords)
        ]
        
        return polygon_angles
    
    def extract_for_piece(self,piece:Piece):
        piece.features["angles"] = self._get_polygon_angles(np.array(piece.get_coords()))



'''

    Old:

'''
class GeometricFeatureExtractor():

    def __init__(self) -> None:
        pass

    def get_polygon_edges_lengths(self,coords):
        coords_prev = np.array(coords[:-1]).reshape(-1,2)
        coords_next = np.array(coords[1:]).reshape(-1,2)
        return np.sqrt(np.sum((coords_next-coords_prev)**2,axis=1))

    def get_angle_of_vectors_(self,coord_left,coord_middle,coord_right):
        vector_1 = np.array(coord_left-coord_middle)
        vector_2 = np.array(coord_right-coord_middle)
        dot = vector_1.dot(vector_2)
        denominator = (np.linalg.norm(vector_1) * np.linalg.norm(vector_2))
        return np.arccos(dot/denominator)

    def get_polygon_angles(self,coords):
        num_coords = coords.shape[0]-1
        polygon_angles = [
            np.degrees(
                self.get_angle_of_vectors_(coords[(i-1)%num_coords],
                                           coords[i],
                                           coords[(i+1)%num_coords])
                ) for i in range(num_coords)
        ]
        
        return polygon_angles
