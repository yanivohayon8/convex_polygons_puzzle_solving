import unittest
import sys
sys.path.append("./")

from src.evaluator import least_square_rigid_motion_svd,AreaOverlappingEvaluator
import numpy as np
from src.data_types.puzzle import Puzzle

class TestLeastSquareRigidBody(unittest.TestCase):

    def test_only_translate_needed(self):
        points = np.array([
            [2,2],
            [3,2],
            [3,3],
            [2,3]
        ])

        ground_truth = np.array([
            [0,0],
            [1,0],
            [1,1],
            [0,1]
        ])

        weights = np.array([1,1,1,1])

        R,t = least_square_rigid_motion_svd(points,ground_truth,weights)
        assert np.array_equal(t,np.array([-2,-2]))
        assert np.array_equal(R,np.identity(2))

    def test_only_rotation_needed(self):
        points = np.array([
            [1,0],
            [1,1],
            [0,1],
            [0,0]
        ])

        ground_truth = np.array([
            [0,0],
            [1,0],
            [1,1],
            [0,1]
        ])

        weights = np.array([1,1,1,1])

        R,t = least_square_rigid_motion_svd(points,ground_truth,weights)
        assert np.array_equal(t,np.array([0,0]))
        assert np.array_equal(R,np.array([
            [0,1],
            [-1,0]
        ]))


class TestAreaOverlappingEvaluator(unittest.TestCase):
    
    def test_gt_to_gt_Inve9084_1_0(self):
        db = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise_level = 0
        puzzle_directory = f"data/ofir/{db}/Puzzle{puzzle_num}/{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        ground_truth_polygons = puzzle.get_ground_truth_puzzle()

        evaluator = AreaOverlappingEvaluator(ground_truth_polygons)
        evaluator._compute_weights()
        assert 1-sum(evaluator.weights)<1e-3

        R,t = evaluator._compute_transformation(ground_truth_polygons)
        assert np.array_equal(t,np.array([0,0]))
        assert np.linalg.norm(R) - np.linalg.norm(np.identity(2)) < 1e-4
    
        evaluator._transform_solution_polygons(ground_truth_polygons)
        eval_score = evaluator._score()

        assert abs(eval_score -1*len(ground_truth_polygons)) < 1e-5



if __name__ == "__main__":
    unittest.main()