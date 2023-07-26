import unittest
from src.evaluator import least_square_rigid_motion_svd
import numpy as np

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

        R,t = least_square_rigid_motion_svd(points,weights,ground_truth)
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

        R,t = least_square_rigid_motion_svd(points,weights,ground_truth)
        assert np.array_equal(t,np.array([0,0]))
        assert np.array_equal(R,np.array([
            [0,1],
            [-1,0]
        ]))

if __name__ == "__main__":
    unittest.main()