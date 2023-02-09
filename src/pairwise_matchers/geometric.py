
import numpy as np
from src.pairwise_matchers import PairwiseMatcher

class GeometricPairwiseMatcher(PairwiseMatcher):

    def __init__(self) -> None:
        super().__init__()
        self.match_edges = {}

    def pairwise_edges_lengths(self,edge_lengths:np.array,confidence_interval=20.0):
        num_pieces = len(edge_lengths)
        for i in range(num_pieces):
            for j in range(num_pieces):
                if i!=j:
                    piece_i = edge_lengths[i].reshape(-1,1)
                    piece_j = edge_lengths[j].reshape(1,-1)
                    subs = np.abs(piece_i-piece_j) # tiling
                    match_edges_diff = subs[subs<confidence_interval]

                    if match_edges_diff.size > 0:
                        # Ensure without duplicates
                        if not f"{i},{j}" in self.match_pieces_score.keys() and not f"{j},{i}" in self.match_pieces_score.keys():
                            self.match_pieces_score[f"{i},{j}"] = np.min(match_edges_diff)
                            self.match_edges[f"{i},{j}"] = np.argwhere(subs<confidence_interval)