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
from src.pairwise_matchers.pictorial import NaiveExtrapolatorMatcher

class TestGraphDrawer(unittest.TestCase):
    
    def _load_graph(self,db,puzzle_num,puzzle_noise_level):
        
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

        pictorial_matcher = NaiveExtrapolatorMatcher(bag_of_pieces)
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

    def test_draw_ground_truth(self):
        db = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 3
        ground_truth_graph = self._load_graph(db,puzzle_num,0)
        drawer = MatchingGraphDrawer(ground_truth_graph)
        drawer._draw_ground_truth_adjacency()
        # drawer._draw_ground_truth_matching()
        plt.show()
    
    def test_draw_Inv9084_with_noise(self):
        db = "1" #"Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 19
        puzzle_noise_level = 1
        
        ground_truth_wrapper = self._load_graph(db,puzzle_num,0)
        wrapper = self._load_graph(db,puzzle_num,puzzle_noise_level)

        fig, axs = plt.subplots(1,2)
        self._draw(wrapper,ground_truth_wrapper,axs[0],axs[1])

        plt.show()

        # raw_cycles = wrapper.compute_cycles(max_length=10)
        # print(len(list(raw_cycles)))

        
    
    def test_VilladeiMisteri_puzzle_1(self,puzzle_noise_level = 0):
        db = "Roman_fresco_Villa_dei_Misteri_Pompeii_009"
        puzzle_num = 2
        puzzle_noise_level = 0
        
        ground_truth_graph = self._load_graph(db,puzzle_num,0)
        graph = self._load_graph(db,puzzle_num,puzzle_noise_level)
        
        fig, axs = plt.subplots(1,2)
        self._draw(graph,ground_truth_graph,axs[0],axs[1])
        plt.show()

    # def test_toy_example(self):
    #     bag_of_pieces = [
    #         Piece("3",[(0.0, 850.612398532945), (896.2748322309999, 0.0), (160.42144514933895, 177.15118274973247)]),
    #         Piece("4",[(1359.7642214436985, 1755.909454053577), (0.0, 0.0), (448.8169164864121, 921.029227021798)]),
    #         Piece("5",[(0.0, 1398.3336137642618), (138.11642193177977, 1479.9378226308218), (741.2116531849097, 1022.620788274944), (767.7281675820086, 0.0)]),
    #         Piece("6",[(317.0016030246443, 972.6080337150196), (747.3753572848327, 42.81779674124118), (0.0, 0.0)])
    #     ]

    #     match_edges = np.array(
    #         [
    #         [list([]), list([np.array([[0, 2]], dtype=np.int64)]),list([np.array([[1, 1]], dtype=np.int64)]), list([])],
    #         [list([np.array([[2, 0]], dtype=np.int64)]), list([]), list([]),list([np.array([[1, 0]], dtype=np.int64)])],
    #         [list([np.array([[1, 1]], dtype=np.int64)]), list([]), list([]),list([np.array([[2, 2]], dtype=np.int64)])],
    #         [list([]), list([np.array([[0, 1]], dtype=np.int64)]),list([np.array([[2, 2]], dtype=np.int64)]), list([])]
    #         ], dtype=object)

    #     match_pieces_score =np.array(
    #         [
    #         [list([]), np.array([0.00098319]), np.array([0.00098616]), list([])],
    #         [np.array([0.00098319]), list([]), list([]), np.array([0.00099589])],
    #         [np.array([0.00098616]), list([]), list([]), np.array([0.00099931])],
    #         [list([]), np.array([0.00099589]), np.array([0.00099931]), list([])]
    #         ],dtype=object)
        
    #     wrapper = MatchingGraphWrapper(bag_of_pieces,match_edges,match_pieces_score)
    #     wrapper.build_graph()

    #     drawer = MatchingGraphDrawer(None)
    #     drawer._draw_general_layout(wrapper.adjacency_graph)
        
        

if __name__ == "__main__":
    unittest.main()