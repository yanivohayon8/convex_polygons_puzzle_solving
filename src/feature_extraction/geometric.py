from shapely import Polygon
import numpy as np


class GeometricFeatureExtractor():

    def get_edges_lengths(self,coords):
#        coords = self.polygon.coords
        num_coords = len(coords)
        curr_coords = coords[0]
        edges_lengths = []
        for coord_index in range(1,num_coords):
            next_coords = coords[coord_index]
            edges_lengths.append(
                np.sqrt(
                    (curr_coords[0]-next_coords[0])**2 + 
                    (curr_coords[1]-next_coords[0])**2
                )
            )    
        return edges_lengths
