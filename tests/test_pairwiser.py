import unittest 
from src.pairwise_matchers.geometric import GeometricPairwiseMatcher
import numpy as np
import matplotlib.pyplot as plt

class TestGeometric(unittest.TestCase):
    
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
            np.array([ 673.26585727, 1524.74870568,  747.75346429,  263.26379564]),

        ])


        puzzle_diameter = 3007.6720313778787
        xi = 3.007672031377879
        noise = 1 #xi*puzzle_diameter/100

        pairwiser = GeometricPairwiseMatcher()
        pairwiser.pairwise_edges_lengths(edges_lengths,confidence_interval=noise)

        heat_map = pairwiser.adjacency_matrix()

        fig,ax = plt.subplots()
        ax.imshow(heat_map)

        num_pieces = edges_lengths.shape[0]
        ax.set_xticks(np.arange(num_pieces)) # , labels=
        ax.set_yticks(np.arange(num_pieces)) # , labels=

        plt.setp(ax.get_xticklabels(),rotation=45,ha="right",rotation_mode="anchor")
        
        for piece_i in range(num_pieces):
            for piece_j in range(num_pieces):
                ax.text(piece_j,piece_i, round(heat_map[piece_i,piece_j],2),
                        ha="center",va="center",color="w")
        
        ax.set_title("Piece Adjacency heat map")
        fig.tight_layout()

        #plt.show()
        plt.waitforbuttonpress()

        print(pairwiser.match_edges)
        

if __name__ == "__main__":
    unittest.main()