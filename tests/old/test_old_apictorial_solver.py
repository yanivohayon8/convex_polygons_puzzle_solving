import unittest
from src.solvers.apictorial import FirstSolver,GraphMatchingSolver
from src.data_types.puzzle import Puzzle
from src.evaluator import AreaOverlappingEvaluator
import matplotlib.pyplot as plt

class TestFirstSolver(unittest.TestCase):
    
    def _run(self,db,puzzle_num,puzzle_noise_level, is_load_cycles=False):
        puzzle_directory = f"data/ofir/{db}/Puzzle{puzzle_num}/{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        solver = FirstSolver(puzzle,db,puzzle_num,puzzle_noise_level)

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

    def _run_solver(self,db,puzzle_num,puzzle_noise_level,is_debug=True):
        # puzzle_directory = f"data/ofir/{db}/Puzzle{puzzle_num}/{puzzle_noise_level}"
        puzzle_directory = f"../ConvexDrawingDataset/{db}/Puzzle{puzzle_num}/{puzzle_noise_level}"

        puzzle = Puzzle(puzzle_directory)
        solver = GraphMatchingSolver(puzzle,db,puzzle_num,puzzle_noise_level)

        solver.load_bag_of_pieces()
        solver.extract_features()
        solver.pairwise()
        solver.build_mating_graph()
        
        solution = solver.global_optimize()

        precision = puzzle.evaluate_precision(solution.get_matings())
        print("\tmatings precision is ",precision)
        recall = puzzle.evaluate_recall(solution.get_matings())
        print("\tmatings recall is ",recall)
        
        # ground_truth_polygons = puzzle.get_ground_truth_puzzle()
        # evaluator = AreaOverlappingEvaluator(ground_truth_polygons)
        # overlapping_score = evaluator.evaluate(solution.get_polygons())
        # print("Solution overlapping score is ",overlapping_score)


    
    def test_Inv9084_puzzle_1(self):
        #image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        db = "1"
        puzzle_num = 19

        for puzzle_noise_level in range(4):
            print("******************************************")
            print(f"\tTest on noise level {puzzle_noise_level}")
            print("******************************************")
            self._run_solver(db,puzzle_num,puzzle_noise_level)
    
    def test_VilladeiMisteri_puzzle_1(self):
        image = "Roman_fresco_Villa_dei_Misteri_Pompeii_009"
        puzzle_num = 1

        for puzzle_noise_level in range(4):
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