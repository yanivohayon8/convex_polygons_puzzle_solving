
# from src.feature_extraction import FeatureExtractor
import numpy as np

class GeometricPairwiseMatcher():

    def pairwise_edges_lengths(self,edge_lengths:np.array,confidence_interval=20.0):
        #edge_lengths_tile = np.tile(edge_lengths.T,(1,edge_lengths.shape[1]))
        match_pieces = {}
        num_pieces = len(edge_lengths)
        for i in range(num_pieces):
            for j in range(num_pieces):
                if i!=j:
                    print(edge_lengths[i].shape)
                    piece_i = edge_lengths[i].reshape(-1,1)
                    piece_j = edge_lengths[j].reshape(1,-1)
                    subs = np.abs(piece_i-piece_j) # tiling
                    match_edges_diff = subs[subs<confidence_interval]

                    if match_edges_diff.size > 0:
                        # Ensure without duplicates
                        if not f"{i},{j}" in match_pieces.keys() and not f"{j},{i}" in match_pieces.keys():
                            match_pieces[f"{i},{j}"] = np.min(match_edges_diff)
    
        return match_pieces