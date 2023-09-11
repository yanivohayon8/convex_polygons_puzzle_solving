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
        db = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise_level = 0
        puzzle_directory = f"data/ofir/{db}/Puzzle{puzzle_num}/{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        ground_truth_solution = puzzle.get_ground_truth_puzzle()
        print(ground_truth_solution)

    def test_ground_truth_puzzle_loading_mutual_folder(self):
        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 0
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        puzzle.load()
        ground_truth_solution = puzzle.get_ground_truth_puzzle()
        print(puzzle.matings_max_difference)
        print(ground_truth_solution)

        bag_of_pieces = puzzle.get_bag_of_pieces()

        # assert "0_mask" in bag_of_pieces[0].extrapolated_img_path
        assert "0_ext" in bag_of_pieces[0].extrapolated_img_path

        assert bag_of_pieces[0].raw_coordinates[0][0]-(-187) < 1
        assert bag_of_pieces[0].raw_coordinates[0][1]-(-922) < 1
        assert bag_of_pieces[0].extrapolation_details.width == 30
        




if __name__ == '__main__':
    unittest.main()