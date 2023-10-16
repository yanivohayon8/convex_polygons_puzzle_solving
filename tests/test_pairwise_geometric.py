from src.feature_extraction.geometric import EdgeLengthExtractor
from src.pairwise_matchers.geometric import EdgeMatcher
from src.piece import Piece


import unittest


class TestEdgeMatcher(unittest.TestCase):

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

        edge_length_extractor = EdgeLengthExtractor(bag_of_pieces) # This could be problematic if there are errors there
        edge_length_extractor.run()

        matcher = EdgeMatcher(bag_of_pieces,1e-3)
        matcher.pairwise()

        print("The match edges")
        print(matcher.match_edges)
        print("The scores")
        print(matcher.match_pieces_score)

        matings = matcher.get_pairwise_as_list()

        assert len(matings) == 4