from shapely import Polygon
import numpy as np


class GeometricFeatureExtractor():

    def get_edges_lengths(self,coords):
        coords_prev = np.array(coords[:-1]).reshape(-1,2)
        coords_next = np.array(coords[1:]).reshape(-1,2)
        return np.sqrt(np.sum((coords_next-coords_prev)**2,axis=1))
