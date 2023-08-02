import unittest
from src.solvers.apictorial import FirstSolver,GraphMatchingSolver
from src.puzzle import Puzzle
from src.evaluator import AreaOverlappingEvaluator
import matplotlib.pyplot as plt

class TestFirstSolver(unittest.TestCase):
    
    def _run(self,puzzle_image,puzzle_num,puzzle_noise_level, is_load_cycles=False):
        puzzle_directory = f"data/ofir/{puzzle_image}/Puzzle{puzzle_num}/{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        solver = FirstSolver(puzzle,puzzle_image,puzzle_num,puzzle_noise_level)

        solver.load_bag_of_pieces()
        solver.extract_features()
        solver.pairwise()

        if is_load_cycles:
            try:
                solver.load_cycles()
            except OSError:
                solver.compute_cycles(True)
        else:
            solver.build_mating_graph()
            # solver.mating_graph.draw_compressed_piece_clustered()
            # solver.mating_graph.draw_all(layout="spectral")
            # solver.mating_graph.draw_compressed(layout="spectral")
            solver.compute_cycles(is_save_cycles=False)
            
        
        solver.build_zero_loops()
        solutions = solver.global_optimize()
        
        ground_truth_polygons = puzzle.get_ground_truth_puzzle()
        evaluator = AreaOverlappingEvaluator(ground_truth_polygons)
        
        for solution in solutions:
            score = evaluator.evaluate(solution.get_polygons())
            print("Overlapping score is ",score)
            print("Matings correct score is ",puzzle.evaluate_rels(solution.get_matings()))

        
    def test_Inv9084_puzzle_1_noise_0(self):
        image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise_level = 0

        self._run(image,puzzle_num,puzzle_noise_level)

    def test_Inv9084_puzzle_1_noise_1(self):
        image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise_level = 1

        self._run(image,puzzle_num,puzzle_noise_level)
    
    def test_Inv9084_puzzle_1_noise_2(self):
        image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise_level = 2

        self._run(image,puzzle_num,puzzle_noise_level)

    def test_Inv9084_puzzle_1_noise_3(self):
        image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise_level = 3

        self._run(image,puzzle_num,puzzle_noise_level)
    
    def test_Inv9084_puzzle_1_noise_4(self):
        image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise_level = 4

        self._run(image,puzzle_num,puzzle_noise_level)

    def test_Inv9084_puzzle_1_noise_5(self):
        image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise_level = 5

        self._run(image,puzzle_num,puzzle_noise_level)

    def test_Inv9084_puzzle_1_noise_6(self):
        image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise_level = 6

        self._run(image,puzzle_num,puzzle_noise_level)

    def test_p5_puzzle_1_noise_0(self):
        image = "p5"
        puzzle_num = 1
        puzzle_noise_level = 0

        self._run(image,puzzle_num,puzzle_noise_level)

        

class TestMatchingGraphSolver(unittest.TestCase):

    def _run_solver(self,puzzle_image,puzzle_num,puzzle_noise_level,is_debug=True):
        puzzle_directory = f"data/ofir/{puzzle_image}/Puzzle{puzzle_num}/{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        solver = GraphMatchingSolver(puzzle,puzzle_image,puzzle_num,puzzle_noise_level)

        solver.load_bag_of_pieces()
        solver.extract_features()
        solver.pairwise()
        solver.build_mating_graph()

        if is_debug:
            solver.mating_graph.draw_adjacency_graph()
            solver.mating_graph.draw()
            plt.show()


    
    def test_Inv9084_puzzle_1(self,puzzle_noise_level=0):
        image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1

        self._run_solver(image,puzzle_num,puzzle_noise_level)



if __name__ == "__main__":
    unittest.main()