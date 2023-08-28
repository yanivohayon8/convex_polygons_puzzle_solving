import unittest 
from src.pairwise_matchers.geometric import GeometricPairwiseMatcher,EdgeMatcher
import numpy as np
import matplotlib.pyplot as plt
from src.feature_extraction.geometric import EdgeLengthExtractor
from src.pairwise_matchers.geometric import EdgeMatcher
from src.piece import Piece
from src.feature_extraction.extrapolator.lama_masking import LamaEdgeExtrapolator
from src.pairwise_matchers.pictorial import NaiveExtrapolatorMatcher

class TestlamaMatcher(unittest.TestCase):

    def test_toy_example(self):
        # bag_of_pieces = [
        #     Piece("3",[(359.6934234692053,0.0),(0.0,1182.1466364589978),(552.5547553983743,664.8981548785887)],extrapolated_img_path='../ConvexDrawingDataset/DB1/Puzzle19/noise_0\\extrapolated\\rgb-3_mask.png'),
        #     Piece("4",[(892.8888169403926,2033.45176941104),(0.0,0.0),(211.833995449535,1002.4259449236998)],extrapolated_img_path='../ConvexDrawingDataset/DB1/Puzzle19/noise_0\\extrapolated\\rgb-4_mask.png'),
        #     Piece("5",[(0.0,1595.1806656860645),(160.30040305844886,1601.4394492589781),(474.0201114068477,912.6414795354285),(11.914194622491777,0.0)],extrapolated_img_path='../ConvexDrawingDataset/DB1/Puzzle19/noise_0\\extrapolated\\rgb-5_mask.png'),
        #     Piece("6",[(1022.2569034805347,0.0),(0.0,68.71924696099452),(321.1597911884128,744.9290577022039)],extrapolated_img_path='../ConvexDrawingDataset/DB1/Puzzle19/noise_0\\extrapolated\\rgb-6_mask.png')
        # ]

        bag_of_pieces = [
            Piece("3",[(359.6934234692053,0.0),(0.0,1182.1466364589978),(552.5547553983743,664.8981548785887)],extrapolated_img_path='../ConvexDrawingDataset/DB1/Puzzle19/noise_0\\extrapolated\\rgb-3_mask.png'),
            Piece("4",[(892.8888169403926,2033.45176941104),(0.0,0.0),(211.833995449535,1002.4259449236998)],extrapolated_img_path='../ConvexDrawingDataset/DB1/Puzzle19/noise_0\\extrapolated\\rgb-4_mask.png')
        ]

        for piece in bag_of_pieces:
            piece.load_extrapolated_image()
        
        feature_extractor = LamaEdgeExtrapolator(bag_of_pieces)
        feature_extractor.run()

        matcher = NaiveExtrapolatorMatcher(bag_of_pieces)
        matcher.pairwise()

        score = matcher.get_score("3","0","4","2")
        print(score)
        assert np.isnan(matcher.get_score("3","0","3","2"))
        assert np.isnan(matcher.get_score("3","0","3","1"))
        assert np.isnan(matcher.get_score("3","0","3","0"))
        assert np.isnan(matcher.get_score("4","0","4","2"))
        assert np.isnan(matcher.get_score("4","0","4","1"))
        assert np.isnan(matcher.get_score("4","0","4","0"))



        
        
        
        


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

        matcher = EdgeMatcher(bag_of_pieces)
        matcher.pairwise(1e-3)

        print("The match edges")
        print(matcher.match_edges)
        print("The scores")
        print(matcher.match_pieces_score)


'''
Old# Todo: write unit test for EdgeMatcher class

'''
class TestGeometric_Old(unittest.TestCase):
    
    def test_Inv9084_puzzle_1_noise_0(self):
        edges_lengths = np.array([
            np.array([1652.17413843, 1129.10319381, 1595.22517657,  488.18193589]),
            np.array([488.18193145, 806.35067968, 973.67087051]),
            np.array([806.35069792, 160.42254484, 692.30414656]),
            np.array([ 692.30415948,  756.87697074, 1235.6577307 ]),
            np.array([1235.65771389, 1024.56403487, 2220.85045619]),
            np.array([1595.22519874, 1022.96451656,  756.87695689,  160.4225449 ]),
            np.array([1022.96451726,  748.60088725, 1024.56403076]),
            np.array([1062.97593227,  674.18139265,  932.33867735]),
            np.array([ 932.33868471,  264.66809436, 1129.10323532]),
            np.array([ 674.18138322, 1527.09691397,  748.60088748,  264.66808857])

        ])

        noise = 1e-3

        pairwiser = GeometricPairwiseMatcher()
        pairwiser.pairwise_edges_lengths(edges_lengths,confidence_interval=noise)
        pairwiser.adjacency_matrix()
        fig,ax = plt.subplots()
        pairwiser.plot_heat_map(ax,fig)
        plt.waitforbuttonpress()

    def test_Inv9084_puzzle_1_noise_1(self):
        edges_lengths = np.array([
            np.array([1651.72390127, 1126.69428015, 1592.45686476,  487.76545279]),
            np.array([485.10522711, 806.04903711, 971.39228994]),
            np.array([803.04910143, 158.7807397 , 690.41483373]),
            np.array([ 690.09324581,  756.04213798, 1235.20247625]),
            np.array([1236.17184229, 1020.47208218, 2217.49155725]),
            np.array([1593.71659059, 1021.13843792,  756.43003847,  159.33799994]),
            np.array([1020.44830287,  746.35767875, 1020.9147307 ]),
            np.array([1057.77093195,  670.54278589,  929.15343577]),
            np.array([ 930.18667907,  263.89589441, 1127.21116365]),
            np.array([ 673.26585727, 1524.74870568,  747.75346429,  263.26379564])
        ])


        puzzle_diameter = 3007.6720313778787
        xi = 3.007672031377879
        noise = xi#*puzzle_diameter/100

        pairwiser = GeometricPairwiseMatcher()
        pairwiser.pairwise_edges_lengths(edges_lengths,confidence_interval=noise)
        pairwiser.adjacency_matrix()
        fig,ax = plt.subplots()
        pairwiser.plot_heat_map(ax,fig)
        plt.waitforbuttonpress()
        

if __name__ == "__main__":
    unittest.main()