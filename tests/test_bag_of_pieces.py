import unittest
import src.puzzle as puzzle


class TestLoader(unittest.TestCase):

    def test_simple(self):
        puzzle_directory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0"
        loader = puzzle.Puzzle(puzzle_directory + "/ground_truth_puzzle.csv",
                        puzzle_directory + "/ground_truth_rels.csv", 
                        puzzle_directory + "/pieces.csv")
        loader.load()



if __name__ == '__main__':
    unittest.main()