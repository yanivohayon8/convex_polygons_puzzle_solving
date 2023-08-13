import unittest
import numpy as np
from src.piece import Piece
from src.mating_graphs.inter_env_graph import InterEnvGraph
from src.mating_graphs.matching_graph import MatchingGraphWrapper
from src.puzzle import Puzzle
from src.feature_extraction import geometric as geo_extractor 
from src.pairwise_matchers import geometric as geo_pairwiser

import networkx as nx
import matplotlib.pyplot as plt



class TestNXPloting(unittest.TestCase):
    def test_plot_toy(self):
        G = nx.Graph()
        G.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (4, 5), (4, 6), (5, 6)])

        # Create a new figure and axis
        fig, ax = plt.subplots()

        layout="spring"
        title="Sample Graph"
        layouts = {
        "spring": nx.spring_layout,
        "random": nx.random_layout,
        "circular": nx.circular_layout,
        "kamada_kawai": nx.kamada_kawai_layout,
        # Add more layout options as needed
         }


        # Create the layout for the nodes
        pos = layouts[layout](G)

        # Draw the nodes and edges of the graph on the provided axis
        nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue",
                font_size=10, ax=ax)

        # Set the title for the plot
        ax.set_title(title)

        # Display the plot
        plt.show()

    def test_color_edges(self):
        # Create a sample graph with weighted edges
        G = nx.Graph()
        G.add_edge('A', 'B', weight=4)
        G.add_edge('B', 'C', weight=2)
        G.add_edge('C', 'D', weight=8)
        G.add_edge('D', 'A', weight=6)

        # Extract edge weights and nodes from the graph
        edge_weights = [data['weight'] for _, _, data in G.edges(data=True)]
        nodes = G.nodes()

        # Create the plot
        pos = nx.circular_layout(G)  # You can use other layout algorithms
        nx.draw(G, pos, with_labels=True, node_size=1000, node_color='lightblue', font_size=10, font_color='black')

        # Draw edges with colors based on weights and add colorbar
        edges = nx.draw_networkx_edges(G, pos, edge_color=edge_weights, edge_cmap=plt.cm.viridis, width=2)
        colorbar = plt.colorbar(edges)
        colorbar.set_label('Edge Weight')

        plt.title('Weighted NetworkX Graph')
        plt.show()

class TestInterEnvGraph(unittest.TestCase):
    
    def test_plot_toy_example(self):
        # puzzle = Puzzle(f"data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0")
        # puzzle.load()
        # bag_of_pieces = puzzle.get_bag_of_pieces()

        # piece 3,4,5,6 from data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0
        bag_of_pieces = [
            Piece("3",[(0.0, 850.612398532945), (896.2748322309999, 0.0), (160.42144514933895, 177.15118274973247)]),
            Piece("4",[(1359.7642214436985, 1755.909454053577), (0.0, 0.0), (448.8169164864121, 921.029227021798)]),
            Piece("5",[(0.0, 1398.3336137642618), (138.11642193177977, 1479.9378226308218), (741.2116531849097, 1022.620788274944), (767.7281675820086, 0.0)]),
            Piece("6",[(317.0016030246443, 972.6080337150196), (747.3753572848327, 42.81779674124118), (0.0, 0.0)])
        ]

        match_edges = np.array(
            [
            [list([]), list([np.array([[0, 2]], dtype=np.int64)]),list([np.array([[1, 1]], dtype=np.int64)]), list([])],
            [list([np.array([[2, 0]], dtype=np.int64)]), list([]), list([]),list([np.array([[1, 0]], dtype=np.int64)])],
            [list([np.array([[1, 1]], dtype=np.int64)]), list([]), list([]),list([np.array([[2, 2]], dtype=np.int64)])],
            [list([]), list([np.array([[0, 1]], dtype=np.int64)]),list([np.array([[2, 2]], dtype=np.int64)]), list([])]
            ], dtype=object)

        match_pieces_score =np.array(
            [
            [list([]), np.array([0.00098319]), np.array([0.00098616]), list([])],
            [np.array([0.00098319]), list([]), list([]), np.array([0.00099589])],
            [np.array([0.00098616]), list([]), list([]), np.array([0.00099931])],
            [list([]), np.array([0.00099589]), np.array([0.00099931]), list([])]
            ],dtype=object)

        mating_graph = InterEnvGraph(bag_of_pieces,match_edges,match_pieces_score)
        # mating_graph.build_graph()
        mating_graph._bulid_relationship_nodes()
        assert len(list(mating_graph.edges_mating_graph.nodes)) == 13
        mating_graph._bulid_enviorments_nodes()
        assert len(list(mating_graph.edges_mating_graph.nodes)) == 13*2
        mating_graph._connect_env_nodes()
        assert len(list(mating_graph.edges_mating_graph.nodes)) == 13*2
        mating_graph._connect_relationship_nodes()
        assert len(list(mating_graph.edges_mating_graph.nodes)) == 13*2
        
        #fig, ax = plt.subplots()
        mating_graph.draw_all()
        mating_graph.draw_compressed(layout="planar")
        mating_graph.draw_compressed_piece_clustered()
        plt.show()
        # plt.waitforbuttonpress()


class TestMatchingGraphAndSpanTree(unittest.TestCase):
    
    def test_toy_example(self):
        # puzzle = Puzzle(f"data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0")
        # puzzle.load()
        # bag_of_pieces = puzzle.get_bag_of_pieces()

        # piece 3,4,5,6 from data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0
        bag_of_pieces = [
            Piece("3",[(0.0, 850.612398532945), (896.2748322309999, 0.0), (160.42144514933895, 177.15118274973247)]),
            Piece("4",[(1359.7642214436985, 1755.909454053577), (0.0, 0.0), (448.8169164864121, 921.029227021798)]),
            Piece("5",[(0.0, 1398.3336137642618), (138.11642193177977, 1479.9378226308218), (741.2116531849097, 1022.620788274944), (767.7281675820086, 0.0)]),
            Piece("6",[(317.0016030246443, 972.6080337150196), (747.3753572848327, 42.81779674124118), (0.0, 0.0)])
        ]

        match_edges = np.array(
            [
            [list([]), list([np.array([[0, 2]], dtype=np.int64)]),list([np.array([[1, 1]], dtype=np.int64)]), list([])],
            [list([np.array([[2, 0]], dtype=np.int64)]), list([]), list([]),list([np.array([[1, 0]], dtype=np.int64)])],
            [list([np.array([[1, 1]], dtype=np.int64)]), list([]), list([]),list([np.array([[2, 2]], dtype=np.int64)])],
            [list([]), list([np.array([[0, 1]], dtype=np.int64)]),list([np.array([[2, 2]], dtype=np.int64)]), list([])]
            ], dtype=object)

        match_pieces_score =np.array(
            [
            [list([]), np.array([0.00098319]), np.array([0.00098616]), list([])],
            [np.array([0.00098319]), list([]), list([]), np.array([0.00099589])],
            [np.array([0.00098616]), list([]), list([]), np.array([0.00099931])],
            [list([]), np.array([0.00099589]), np.array([0.00099931]), list([])]
            ],dtype=object)
        
        mating_graph = MatchingGraphWrapper(bag_of_pieces,match_edges,match_pieces_score)
        mating_graph._build_matching_graph()
        matching_nodes = mating_graph.get_matching_graph_nodes()
        assert len(matching_nodes) == 4*2 # because it is 4 triangles matching around vertex

        mating_graph._bulid_only_pieces_graph()

        plt.show()

    
    def _bulid_wrapper(self,puzzle_image,puzzle_num,puzzle_noise_level):
        puzzle = Puzzle(f"../ConvexDrawingDataset/{puzzle_image}/Puzzle{puzzle_num}/{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()
        id2piece = {}

        for piece in bag_of_pieces:
            id2piece[piece.id] = piece

        edge_length_extractor = geo_extractor.EdgeLengthExtractor(bag_of_pieces)
        edge_length_extractor.run()

        angles_extractor = geo_extractor.AngleLengthExtractor(bag_of_pieces)
        angles_extractor.run()

        edge_length_pairwiser = geo_pairwiser.EdgeMatcher(bag_of_pieces)
        edge_length_pairwiser.pairwise(puzzle.matings_max_difference+1e-3)
        
        wrapper = MatchingGraphWrapper(bag_of_pieces,id2piece,
                                                edge_length_pairwiser.match_edges,
                                                edge_length_pairwiser.match_pieces_score)
        wrapper._build_matching_graph()
        wrapper._bulid_only_pieces_graph()
        wrapper._build_adjacency_graph()
        # matching = mating_graph.find_matching()

        return wrapper

    def _compute_cycles(self,wrapper:MatchingGraphWrapper):
        raw_cycles = wrapper.compute_cycles(max_length=10)
        print(len(list(raw_cycles)))

    def test_red_blue_route_Inv9084_puzzle_1(self,puzzle_noise_level =1 ):
        image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise_level = 1
        wrapper = self._bulid_wrapper(image,puzzle_num,puzzle_noise_level)
        # self._compute_cycles(wrapper)

        cycles = []
        wrapper._compute_red_blue_cycles("P_7_E_1","P_9_E_0",cycles)
        print(cycles)
    
    def test_360_loops_Inv9084_puzzle_1(self,puzzle_noise_level =1 ):
        image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise_level = 1
        wrapper = self._bulid_wrapper(image,puzzle_num,puzzle_noise_level)
        # self._compute_cycles(wrapper)

        cycles = []
        visited = ["P_7_E_2"]
        visited.append("P_7_E_1")

        wrapper.compute_red_blue_360_loops("P_7_E_2","P_9_E_0",cycles,
                                           visited=visited)
        assert len(cycles) == 1

        cycles = []
        visited = ["P_7_E_0"]
        visited.append("P_7_E_1")

        wrapper.compute_red_blue_360_loops(visited[-2],"P_9_E_0",cycles,
                                           visited=visited)
        
        
        print(cycles)
        assert len(cycles) == 0
        
        cycles = []
        visited = ["P_8_E_2"]
        visited.append("P_8_E_1")

        wrapper.compute_red_blue_360_loops(visited[-2],"P_9_E_3",cycles,
                                           visited=visited)
        
        print(cycles)

        
    
    def test_VilladeiMisteri_puzzle_1(self,puzzle_noise_level = 0):
        image = "Roman_fresco_Villa_dei_Misteri_Pompeii_009"
        puzzle_num = 1
        wrapper = self._bulid_wrapper(image,puzzle_num,puzzle_noise_level)


    def test_len_pair_p5_puzzle_1(self):
        image = "p5"
        puzzle_num = 1
        puzzle_noise_level = 0
        wrapper = self._bulid_wrapper(image,puzzle_num,puzzle_noise_level)

if __name__ == "__main__":
    unittest.main()