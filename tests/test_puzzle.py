import unittest
from src.data_types.puzzle import Puzzle
import matplotlib.pyplot as plt

class TestLoader(unittest.TestCase):

    def test_ground_truth_puzzle_loading_mutual_folder(self):
        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 0
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        puzzle.load()
        print(puzzle.matings_max_difference)
        bag_of_pieces = puzzle.get_bag_of_pieces()

        # assert "0_mask" in bag_of_pieces[0].extrapolated_img_path
        assert "0_ext" in bag_of_pieces[0].extrapolated_img_path
        assert bag_of_pieces[0].raw_coordinates[0][0]-(-187) < 1
        assert bag_of_pieces[0].raw_coordinates[0][1]-(-922) < 1
        assert bag_of_pieces[0].extrapolation_details.height == 30

        ground_truth_solution = puzzle.get_ground_truth_puzzle()
        print(ground_truth_solution)
    
    def test_load_images(self):
        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 0
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()
        # puzzle.load_images()

        plt.imshow(bag_of_pieces[0].extrapolated_img)
        plt.show()


    def test_load_puzzle_with_missing_pieces(self):
        db = "5"
        puzzle_num = "1"
        puzzle_noise_level = 0
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()
        print(puzzle.matings_max_difference)
        assert len(bag_of_pieces) == 9


if __name__ == '__main__':
    unittest.main()