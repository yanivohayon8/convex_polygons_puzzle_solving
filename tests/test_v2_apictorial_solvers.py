import unittest
from src.solvers.apictorial_v2 import ZeroLoops360Solver
from src.puzzle import Puzzle
from src.evaluator import AreaOverlappingEvaluator
import matplotlib.pyplot as plt


class TestZeroLoops360Solver(unittest.TestCase):

    def _run_solver(self,puzzle_image,puzzle_num,puzzle_noise_level,is_debug=True):
        # puzzle_directory = f"data/ofir/{puzzle_image}/Puzzle{puzzle_num}/{puzzle_noise_level}"
        puzzle_directory = f"../ConvexDrawingDataset/{puzzle_image}/Puzzle{puzzle_num}/{puzzle_noise_level}"

        puzzle = Puzzle(puzzle_directory)
        solver = ZeroLoops360Solver(puzzle,puzzle_image,puzzle_num,puzzle_noise_level)

        solver.load_bag_of_pieces()
        solver.extract_features()
        solver.pairwise()
        solver.build_mating_graph()
        solver.build_zero_loops()
        
        solution = solver.global_optimize(is_debug_loops=True)

        precision = puzzle.evaluate_precision(solution.get_matings())
        print("\tmatings precision is ",precision)
        recall = puzzle.evaluate_recall(solution.get_matings())
        print("\tmatings recall is ",recall)

    
    def test_Inv9084_puzzle_1(self):
        image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1

        for puzzle_noise_level in range(2,4):
            print("******************************************")
            print(f"\tTest on noise level {puzzle_noise_level}")
            print("******************************************")
            self._run_solver(image,puzzle_num,puzzle_noise_level)
    
    def test_VilladeiMisteri_puzzle_1(self):
        image = "Roman_fresco_Villa_dei_Misteri_Pompeii_009"
        puzzle_num = 1

        for puzzle_noise_level in range(1,4):
            print("******************************************")
            print(f"\tTest on noise level {puzzle_noise_level}")
            print("******************************************")
            self._run_solver(image,puzzle_num,puzzle_noise_level)
    
    def test_Terentius_puzzle_1(self):
        image = "SCALED-3_Terentius_Neo_and_wife_MAN_Napoli_Inv9058_n01"
        puzzle_num = 1

        for puzzle_noise_level in range(1):
            print("******************************************")
            print(f"\tTest on noise level {puzzle_noise_level}")
            print("******************************************")
            self._run_solver(image,puzzle_num,puzzle_noise_level)
    
    def test_Terentius_puzzle_2(self):
        image = "SCALED-3_Terentius_Neo_and_wife_MAN_Napoli_Inv9058_n01"
        puzzle_num = 2

        for puzzle_noise_level in range(1):
            print("******************************************")
            print(f"\tTest on noise level {puzzle_noise_level}")
            print("******************************************")
            self._run_solver(image,puzzle_num,puzzle_noise_level)
    
    def test_pizza_1(self):
        image = "SCALED-3_pizza"
        puzzle_num = 1

        for puzzle_noise_level in range(1):
            print("******************************************")
            print(f"\tTest on noise level {puzzle_noise_level}")
            print("******************************************")
            self._run_solver(image,puzzle_num,puzzle_noise_level)



if __name__ == "__main__":
    unittest.main()