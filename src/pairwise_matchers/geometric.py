
# from src.feature_extraction import FeatureExtractor
import numpy as np

class GeometricPairwiseMatcher():

    def pairwise_edges_lengths(self,edge_lengths:np.array,confidence_interval=20.0):
        edge_lengths_tile = np.tile(edge_lengths.T,(1,edge_lengths.shape[1]))
        pass