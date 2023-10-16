
from typing import Any
import numpy as np
from src.mating import Mating
from src.pairwise_matchers import factory

class EdgeMatcher():
    
    def __init__(self,pieces,confidence_interval) -> None:
        self.pieces = pieces
        self.match_edges = None
        self.match_pieces_score = None
        self.confidence_interval = confidence_interval

    def pairwise(self):
        '''
        confidence_interval - the max noise applied on the edge
        '''
        edge_lengths = [piece.features["edges_length"] for piece in self.pieces]
        num_pieces = len(edge_lengths)
        matching_edges = [[] for _ in range(num_pieces**2)]
        matching_scores = [[] for _ in range(num_pieces**2)]

        for i in range(num_pieces):
            for j in range(num_pieces):
                if i!=j:
                    piece_i = edge_lengths[i].reshape(-1,1)
                    piece_j = edge_lengths[j].reshape(1,-1)
                    subs = np.abs(piece_i-piece_j) # tiling
                    match_edges_diff = subs[subs<self.confidence_interval]

                    if match_edges_diff.size > 0:
                        matching_edges[i*num_pieces+j].append(np.argwhere(subs<self.confidence_interval))
                        score = self.confidence_interval*np.ones_like(match_edges_diff) - match_edges_diff
                        score[score<0] = 0
                        matching_scores[i*num_pieces+j] = score

        self.match_edges = np.array(matching_edges,dtype="object").reshape((num_pieces,num_pieces))
        self.match_pieces_score = np.array(matching_scores,dtype="object").reshape((num_pieces,num_pieces))

    def get_pairwise_as_list(self):
        num_pieces = len(self.pieces)
        matings = []

        for piece_i in range(num_pieces):
            piece_i_id = self.pieces[piece_i].id
            for piece_j in range(piece_i+1,num_pieces):
                piece_j_id = self.pieces[piece_j].id
                mating_edges = self.match_edges[piece_i,piece_j]
                if len(mating_edges)>0:
                    for k,mat_edge in enumerate(mating_edges):
                        new_links = []

                        for mating in mat_edge:
                            edge_ii = mating[0]
                            edge_jj = mating[1]
                            matings.append(Mating(piece_1=piece_i_id,edge_1=edge_ii,
                                                  piece_2=piece_j_id,edge_2=edge_jj))
        
        return matings
                        

class EdgeMatcherBuilder():

    def __call__(self, pieces,confidence_interval, **_ignored) -> Any:
        return EdgeMatcher(pieces,confidence_interval)

factory.register_builder(EdgeMatcher.__name__,EdgeMatcherBuilder())