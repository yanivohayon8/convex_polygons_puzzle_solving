from src.pairwise_matchers.pictorial import PictorialMatcher
from src.data_types.puzzle import Puzzle
from src.data_types.mating import Mating
from src import shared_variables
import numpy as np
from src.pairwise_matchers import factory


class SynthesisMatcher(PictorialMatcher):

    def __init__(self, pieces,puzzle:Puzzle) -> None:
        super().__init__(pieces, "")
        self.puzzle = puzzle

    def pairwise(self):
        for edge1_i in range(self.total_num_edges):
    
            for edge2_j in range(self.total_num_edges):
            
                if self.edge2pieceid[edge1_i] == self.edge2pieceid[edge2_j]:
                    continue

                piece1_i = self.edge2piece_index[edge1_i]
                edge1_local_i = self.global_index2local_index[edge1_i]

                piece2_j = self.edge2piece_index[edge2_j]
                edge2_local_j = self.global_index2local_index[edge2_j]
                

                mating = Mating(piece_1=self.pieces[piece1_i].id, piece_2= self.pieces[piece2_j].id,
                                edge_1 = edge1_local_i, edge_2 = edge2_local_j)


                if self.puzzle.is_ground_truth_mating(mating):
                    self.matching_edges_scores[edge1_i,edge2_j] = 1
                else:
                    self.matching_edges_scores[edge1_i,edge2_j] = 0
        

class SynthesisMatcherBuilder():

    def __call__(self,pieces, puzzle, **ignored):
        return SynthesisMatcher(pieces,puzzle)

factory.register_builder(SynthesisMatcher.__name__,SynthesisMatcherBuilder())