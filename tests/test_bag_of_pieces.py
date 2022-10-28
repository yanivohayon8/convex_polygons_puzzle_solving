import unittest
import src.bag_of_pieces as bag_of_pieces


class TestLoader(unittest.TestCase):

    def test_simple(self):
        puzzle_directory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0"
        loader = bag_of_pieces.bag_of_pieces(puzzle_directory + "/ground_truth_puzzle.csv",
                        puzzle_directory + "/ground_truth_rels.csv", 
                        puzzle_directory + "/pieces.csv")
        loader.load()
        print(loader.df_puzzle.head())
        print(loader.df_rels.head())
        print(loader.df_pieces.head())

if __name__ == '__main__':
    unittest.main()