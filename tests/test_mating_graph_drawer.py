import unittest
from src.puzzle import Puzzle
from src.mating_graphs.matching_graph import MatchingGraphAndSpanTree
from src.feature_extraction import geometric as geo_extractor 
from src.pairwise_matchers import geometric as geo_pairwiser
from src.mating_graphs.drawer import MatchingGraphDrawer
import matplotlib.pyplot as plt



class TestGraphDrawer(unittest.TestCase):
    
    def _load_graph(self,puzzle_image,puzzle_num,puzzle_noise_level):
        
        puzzle = Puzzle(f"../ConvexDrawingDataset/{puzzle_image}/Puzzle{puzzle_num}/{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()

        edge_length_extractor = geo_extractor.EdgeLengthExtractor(bag_of_pieces)
        edge_length_extractor.run()

        edge_length_pairwiser = geo_pairwiser.EdgeMatcher(bag_of_pieces)
        edge_length_pairwiser.pairwise(puzzle.noise+1e-3)
        
        graph = MatchingGraphAndSpanTree(bag_of_pieces,
                                                edge_length_pairwiser.match_edges,
                                                edge_length_pairwiser.match_pieces_score)
        graph._build_matching_graph()
        graph._bulid_base_adjacency_graph()
        graph.find_matching()

        return graph

    def test_draw_ground_truth(self):
        puzzle_image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        ground_truth_graph = self._load_graph(puzzle_image,puzzle_num,0)
        drawer = MatchingGraphDrawer(ground_truth_graph)
        drawer._draw_ground_truth_adjacency()
        drawer._draw_ground_truth_matching()
        plt.show()
    
    def test_draw_graph_with_noise(self):
        puzzle_image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise_level = 1
        
        ground_truth_graph = self._load_graph(puzzle_image,puzzle_num,0)
        drawer = MatchingGraphDrawer(ground_truth_graph)
        
        graph = self._load_graph(puzzle_image,puzzle_num,puzzle_noise_level)
        drawer.draw_adjacency_graph(graph)



        plt.show()

if __name__ == "__main__":
    unittest.main()