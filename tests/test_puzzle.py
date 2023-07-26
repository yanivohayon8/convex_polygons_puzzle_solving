import unittest
from src.puzzle import Puzzle


class TestLoader(unittest.TestCase):

    # def test_simple(self):
    #     puzzle_directory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0"
    #     loader = puzzle.Puzzle(puzzle_directory + "/ground_truth_puzzle.csv",
    #                     puzzle_directory + "/ground_truth_rels.csv", 
    #                     puzzle_directory + "/pieces.csv")
    #     loader.load()

    def test_ground_truth_puzzle_loading(self):
        puzzle_image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise_level = 0
        puzzle_directory = f"data/ofir/{puzzle_image}/Puzzle{puzzle_num}/{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        ground_truth_solution = puzzle.get_ground_truth_puzzle()
        print(ground_truth_solution)



if __name__ == '__main__':
    unittest.main()