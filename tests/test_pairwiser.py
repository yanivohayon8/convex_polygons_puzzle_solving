import unittest 
from src.pairwise_matchers.geometric import GeometricPairwiseMatcher
import numpy as np
import matplotlib.pyplot as plt

# Todo: write unit test for EdgeMatcher class

'''
Old
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