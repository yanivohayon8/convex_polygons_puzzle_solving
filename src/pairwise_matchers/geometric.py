
import numpy as np
from src.pairwise_matchers import PairwiseMatcher

class GeometricPairwiseMatcher(PairwiseMatcher):

    def __init__(self) -> None:
        super().__init__()
        self.match_edges = {}

    def pairwise_edges_lengths(self,edge_lengths:np.array,confidence_interval=1.0):
        num_pieces = len(edge_lengths)
        matching_edges = [[] for _ in range(num_pieces**2)]
        matching_scores = [[] for _ in range(num_pieces**2)]

        for i in range(num_pieces):
            for j in range(num_pieces):
                if i!=j:
                    piece_i = edge_lengths[i].reshape(-1,1)
                    piece_j = edge_lengths[j].reshape(1,-1)
                    subs = np.abs(piece_i-piece_j) # tiling
                    match_edges_diff = subs[subs<confidence_interval]

                    if match_edges_diff.size > 0:
                        matching_edges[i*num_pieces+j].append(np.argwhere(subs<confidence_interval))
                        matching_scores[i*num_pieces+j] = match_edges_diff

        self.match_edges = np.array(matching_edges,dtype="object").reshape((num_pieces,num_pieces))
        self.match_pieces_score = np.array(matching_scores,dtype="object").reshape((num_pieces,num_pieces))
    
    



                
