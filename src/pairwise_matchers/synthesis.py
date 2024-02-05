from src.pairwise_matchers.pictorial import PictorialMatcher
from src.data_types.puzzle import Puzzle
from src.data_types.mating import Mating
from src import shared_variables
import numpy as np
from src.pairwise_matchers import factory
import random




class SynthesisMatcher(PictorialMatcher):

    def __init__(self, pieces,puzzle:Puzzle,
                 min_positive_score,percentage_false_positives) -> None:
        super().__init__(pieces, "")
        self.puzzle = puzzle
        self.min_positive_score = min_positive_score
        self.percentage_false_positives = percentage_false_positives

    def pairwise(self):
        num_false_positives = 0
        total_num_pairing = self.total_num_edges*(self.total_num_edges-1)/2

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
                    self.matching_edges_scores[edge1_i,edge2_j] = random.uniform(0.9,0.95)
                else:
                    if num_false_positives < self.percentage_false_positives * total_num_pairing:
                        coin = random.uniform(self.min_positive_score,0.95)
                        num_false_positives+=1
                    else:
                        coin = random.uniform(0,self.min_positive_score-0.01)

                    self.matching_edges_scores[edge1_i,edge2_j] = coin
        

class SynthesisMatcherBuilder():

    def __call__(self,pieces, puzzle,min_positive_score,percentage_false_positives, **ignored):
        return SynthesisMatcher(pieces,puzzle,min_positive_score,percentage_false_positives)

factory.register_builder(SynthesisMatcher.__name__,SynthesisMatcherBuilder())