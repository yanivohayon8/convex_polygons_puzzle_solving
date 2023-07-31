import unittest
import numpy as np
from src.piece import Piece
from src.edge_mating_graph import EdgeMatingGraph,plot_graph
# from src.puzzle import Puzzle

import networkx as nx
import matplotlib.pyplot as plt


class TestNXPloting(unittest.TestCase):
    def test_plot_toy(self):
        G = nx.Graph()
        G.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (4, 5), (4, 6), (5, 6)])

        # Create a new figure and axis
        fig, ax = plt.subplots()

        # Plot the graph using the function
        plot_graph(G, layout="spring", title="Sample Graph", ax=ax)

        # Display the plot
        plt.show()

class TestFirstGraph(unittest.TestCase):
    
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

        mating_graph = EdgeMatingGraph(bag_of_pieces,match_edges,match_pieces_score)
        mating_graph.build_graph()
        
        fig, ax = plt.subplots()
        mating_graph.draw(ax=ax)
        plt.show()
        # plt.waitforbuttonpress()





if __name__ == "__main__":
    unittest.main()