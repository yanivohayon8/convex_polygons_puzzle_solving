import unittest
from src.puzzle import Puzzle
from src.mating_graphs.matching_graph import MatchingGraphWrapper
from src.feature_extraction import geometric as geo_extractor 
from src.pairwise_matchers import geometric as geo_pairwiser
from src.mating_graphs.drawer import MatchingGraphDrawer
import matplotlib.pyplot as plt
import numpy as np
from src.piece import Piece
from src.feature_extraction.extrapolator.lama_masking import LamaEdgeExtrapolator
from src.pairwise_matchers.pictorial import NaiveExtrapolatorMatcher,ConvolutionV1Matcher

class TestGraphDrawer(unittest.TestCase):
    
    def _load_graph(self,db,puzzle_num,puzzle_noise_level,
                    pictorial_matcher="naive"):
        
        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()

        id2piece = {}

        for piece in bag_of_pieces:
            id2piece[piece.id] = piece
            piece.load_extrapolated_image()

        edge_length_extractor = geo_extractor.EdgeLengthExtractor(bag_of_pieces)
        edge_length_extractor.run()

        angles_extractor = geo_extractor.AngleLengthExtractor(bag_of_pieces)
        angles_extractor.run()

        lama_extractor = LamaEdgeExtrapolator(bag_of_pieces)
        lama_extractor.run()

        edge_length_pairwiser = geo_pairwiser.EdgeMatcher(bag_of_pieces)
        edge_length_pairwiser.pairwise(puzzle.matings_max_difference+1e-3)

        if pictorial_matcher == "naive":
            pictorial_matcher = NaiveExtrapolatorMatcher(bag_of_pieces)
            pictorial_matcher.pairwise()
        elif pictorial_matcher == "convV1":
            pictorial_matcher = ConvolutionV1Matcher(bag_of_pieces,self.extrapolation_width)
            pictorial_matcher.pairwise()

        wrapper = MatchingGraphWrapper(bag_of_pieces,id2piece,
                                                edge_length_pairwiser.match_edges,
                                                edge_length_pairwiser.match_pieces_score,
                                                pictorial_matcher=pictorial_matcher)
        wrapper.build_graph()
        # wrapper.find_matching()

        return wrapper

    def _draw(self,wrapper:MatchingGraphWrapper,ground_truth_wrapper:MatchingGraphWrapper,ax1,ax2):
        drawer = MatchingGraphDrawer(ground_truth_wrapper)
        drawer.init()

        drawer.draw_adjacency_graph(wrapper,ax=ax1)
        ax1.set_title("Noised")

        drawer.draw_adjacency_graph(ground_truth_wrapper,ax=ax2)
        ax2.set_title("Noiseless")

        drawer.draw_graph_matching(wrapper)
        drawer.draw_graph_filtered_matching(wrapper)

    def test_draw_ground_truth(self):
        db = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 3
        ground_truth_graph = self._load_graph(db,puzzle_num,0)
        drawer = MatchingGraphDrawer(ground_truth_graph)
        drawer._draw_ground_truth_adjacency()
        # drawer._draw_ground_truth_matching()
        plt.show()
    
    def test_draw_Inv9084_with_noise(self):
        db = "1" 
        puzzle_num = 19 #13 #19
        puzzle_noise_level = 1
        pictorial_matcher = "convV1" #"convV1"
        self.extrapolation_width = 10

        ground_truth_wrapper = self._load_graph(db,puzzle_num,0,
                                                pictorial_matcher=pictorial_matcher)
        wrapper = self._load_graph(db,puzzle_num,puzzle_noise_level,
                                   pictorial_matcher=pictorial_matcher)

        fig, axs = plt.subplots(1,2)
        self._draw(wrapper,ground_truth_wrapper,axs[0],axs[1])

        plt.show()
        
    

        
        

if __name__ == "__main__":
    unittest.main()