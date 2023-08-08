import unittest
from src.puzzle import Puzzle
from src.mating_graphs.matching_graph import MatchingGraphWrapper
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
        edge_length_pairwiser.pairwise(puzzle.matings_max_difference+1e-3)
        
        wrapper = MatchingGraphWrapper(bag_of_pieces,
                                                edge_length_pairwiser.match_edges,
                                                edge_length_pairwiser.match_pieces_score)
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

    def test_draw_ground_truth(self):
        puzzle_image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 3
        ground_truth_graph = self._load_graph(puzzle_image,puzzle_num,0)
        drawer = MatchingGraphDrawer(ground_truth_graph)
        drawer._draw_ground_truth_adjacency()
        # drawer._draw_ground_truth_matching()
        plt.show()
    
    def test_draw_Inv9084_with_noise(self):
        puzzle_image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise_level = 1
        
        ground_truth_wrapper = self._load_graph(puzzle_image,puzzle_num,0)
        wrapper = self._load_graph(puzzle_image,puzzle_num,puzzle_noise_level)

        fig, axs = plt.subplots(1,2)
        self._draw(wrapper,ground_truth_wrapper,axs[0],axs[1])

        plt.show()

        raw_cycles = wrapper.compute_cycles(max_length=10)
        print(len(list(raw_cycles)))
    
    def test_VilladeiMisteri_puzzle_1(self,puzzle_noise_level = 0):
        puzzle_image = "Roman_fresco_Villa_dei_Misteri_Pompeii_009"
        puzzle_num = 2
        puzzle_noise_level = 1
        
        ground_truth_graph = self._load_graph(puzzle_image,puzzle_num,0)
        graph = self._load_graph(puzzle_image,puzzle_num,puzzle_noise_level)
        
        fig, axs = plt.subplots(1,2)
        self._draw(graph,ground_truth_graph,axs[0],axs[1])
        plt.show()

if __name__ == "__main__":
    unittest.main()