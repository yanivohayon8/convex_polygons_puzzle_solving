import unittest
from src.solvers.pictorial.without_missing_pieces.v1 import  LoopMergerSolver
from src import shared_variables
from src.evaluator import AreaOverlappingEvaluator

class TestLoopMergerSolver(unittest.TestCase):

    def test_solver_compiles(self):
        db=1
        puzzle_num=19
        puzzle_noise_level=0

        solver = LoopMergerSolver(db,puzzle_num,puzzle_noise_level)
        solution = solver.solve(compatibility_threshold=0.38)

        precision = shared_variables.puzzle.evaluate_precision(solution.get_matings())
        print("\tmatings precision is ",precision)
        recall = shared_variables.puzzle.evaluate_recall(solution.get_matings())
        print("\tmatings recall is ",recall)
        
        area_evaluator = AreaOverlappingEvaluator(shared_variables.puzzle.get_ground_truth_puzzle())
        area_overlap = area_evaluator.evaluate(solution.get_polygons())
        print("\t area overlap: ", area_overlap)

        print("All compile")
    

    def _run(self,db,puzzle_num,puzzle_noise_level):
        
        solver = LoopMergerSolver(db,puzzle_num,puzzle_noise_level)
        solution = solver.solve()

        precision = shared_variables.puzzle.evaluate_precision(solution.get_matings())
        print("\tmatings precision is ",precision)
        recall = shared_variables.puzzle.evaluate_recall(solution.get_matings())
        print("\tmatings recall is ",recall)
        
        area_evaluator = AreaOverlappingEvaluator(shared_variables.puzzle.get_ground_truth_puzzle())
        area_overlap = area_evaluator.evaluate(solution.get_polygons())
        print("\t area overlap: ", area_overlap)

    def test_db_1_puzzle_19_noise_1(self):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 1
        self._run(db,puzzle_num,puzzle_noise_level)
    
    def test_db_1_puzzle_19_noise_2(self):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 2
        self._run(db,puzzle_num,puzzle_noise_level)
    
    def test_db_1_puzzle_20_noise_0(self):
        db = 1
        puzzle_num = 20
        puzzle_noise_level = 0
        self._run(db,puzzle_num,puzzle_noise_level)



if __name__ == "__main__":
    unittest.main()