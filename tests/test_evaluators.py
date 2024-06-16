import unittest
import sys
sys.path.append("./")

from src.evaluator import least_square_rigid_motion_svd,AreaOverlappingEvaluator,registration_only_one_piece
import numpy as np
from src.data_types.puzzle import Puzzle
from shapely import affinity
from src import shared_variables
import matplotlib.pyplot as plt
from shapely import Polygon,MultiPolygon

import random


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
        assert np.array_equal(R,np.array([
            [0,1],
            [-1,0]
        ]))
        assert np.array_equal(t,np.array([0,0]))

    def test_poc_(self):
        # Given points and ground truth
        points = np.array([
            [1, 0],
            [1, 1],
            [0, 1],
            [0, 0]
        ])

        ground_truth = np.array([
            [0, 0],
            [1, 0],
            [1, 1],
            [0, 1]
        ])

        # 1. Calculate the centroids
        centroid_points = np.mean(points, axis=0)
        centroid_ground_truth = np.mean(ground_truth, axis=0)

        # 2. Center the points
        points_centered = points - centroid_points
        ground_truth_centered = ground_truth - centroid_ground_truth

        # 3. Compute the optimal rotation matrix using SVD
        H = points_centered.T @ ground_truth_centered
        U, S, Vt = np.linalg.svd(H)
        R = Vt.T @ U.T

        # Handle reflection case
        if np.linalg.det(R) < 0:
            Vt[-1, :] *= -1
            R = Vt.T @ U.T

        # 4. Compute the translation vector
        t = centroid_ground_truth - R @ centroid_points

        print("Rotation matrix (R):")
        print(R)
        print("\nTranslation vector (t):")
        print(t)

class TestAreaOverlappingEvaluator(unittest.TestCase):
    
    def plot(self,polygons, ax = None):

        if ax is None:
            _,ax = plt.subplots()
        
        random.seed(10)

        for poly in polygons:
            xs,ys = poly.exterior.xy
            ax.fill(xs,ys, alpha=0.5,fc=(random.random(),random.random(),random.random()),ec="black")

        ax.set_aspect("equal")


    def test_gt_to_gt(self):
        db = "0-30"
        puzzle_num = "19_DB1"
        puzzle_noise_level = 0
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
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

        # assert abs(eval_score -1*len(ground_truth_polygons)) < 1e-5
        assert abs(eval_score -1) < 1e-5

    def test_gt_to_gt_translated(self):
        db = "0-30"
        puzzle_num = "19_DB1"
        puzzle_noise_level = 0
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        ground_truth_polygons = puzzle.get_ground_truth_puzzle()

        _,axes = plt.subplots(1,3)
        self.plot(ground_truth_polygons,ax=axes[0])
        axes[0].set_title("Ground Truth")


        tx = 10000 # arbitrary value
        ty = 10000 # arbitrary value
        translated_polygons = [affinity.translate(polygon,tx,ty) for polygon in ground_truth_polygons] 

        self.plot(translated_polygons,ax=axes[1])
        axes[1].set_title("Translated")


        translated_polygons_v2 = [Polygon(polygon) for polygon in translated_polygons] # creating a copy
        angle = 45
        sin_angle = np.sin(angle)
        cos_angle = np.cos(angle)
        small_piece_index = 2 # 0
        # translated_polygons_v2[small_piece_index] = affinity.affine_transform(translated_polygons_v2[small_piece_index],[cos_angle,-sin_angle,sin_angle,cos_angle,0,0])
        translated_polygons_v2[small_piece_index] = affinity.rotate(translated_polygons_v2[small_piece_index],angle)

        self.plot(translated_polygons_v2,ax=axes[2])
        axes[2].set_title("Translated only one piece")

        plt.show()


        evaluator = AreaOverlappingEvaluator(ground_truth_polygons)
        eval_score_perfect = evaluator.evaluate(translated_polygons)
        assert abs(eval_score_perfect -1) < 1e-5

        eval_score = evaluator.evaluate(translated_polygons_v2)
        assert eval_score < eval_score_perfect



    def test_translation_of_polygons(self):
        db = "0-30"
        puzzle_num = "19_DB1"
        puzzle_noise_level = 0
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        ground_truth_polygons = puzzle.get_ground_truth_puzzle()

        tx = 0 # 0
        ty = 0 # 0
        angle = 50 #50
        origin = MultiPolygon(ground_truth_polygons).centroid
        translated_polygons = [affinity.rotate(affinity.translate(polygon,tx,ty),angle,origin=origin) for polygon in ground_truth_polygons]

        self.plot(translated_polygons)

        evaluator = AreaOverlappingEvaluator(ground_truth_polygons)
        eval_score_perfect = evaluator.evaluate(translated_polygons)

        self.plot(evaluator.transfomed_polygons_solution)
        plt.show()


    def moving_polygons_by_svd_(self,solution_polygons,ground_truth_polygons):
        pieces_areas = list(map(lambda p: p.area,ground_truth_polygons))
        largest_piece_index = pieces_areas.index(max(pieces_areas))
        solution_largest_polygon = solution_polygons[largest_piece_index]
        ground_truth_largest_polygon = ground_truth_polygons[largest_piece_index]

        ground_truth_coords = np.array(solution_largest_polygon.exterior.coords)
        ground_truth_truth_coords = np.array(ground_truth_largest_polygon.exterior.coords)

        R,t = least_square_rigid_motion_svd(ground_truth_coords,ground_truth_truth_coords,np.ones(ground_truth_coords.shape[0]))
            
        translated_polygons = [affinity.translate(polygon,t[0],t[1]) for polygon in solution_polygons]
        center_of_all = MultiPolygon(translated_polygons).centroid
        angle = np.arccos(R[0,0])
        rotated_polygons = [affinity.rotate(polygon,-angle,use_radians=True,origin=center_of_all) for polygon in translated_polygons]

        return translated_polygons,rotated_polygons

    def test_svd_reliablity(self):
        db = "0-30"
        puzzle_num = "19_DB1"
        puzzle_noise_level = 0
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        ground_truth_polygons = puzzle.get_ground_truth_puzzle()

        tx = 3000 # 0
        ty = 3000 # 0
        angle = 50 #50
        origin = MultiPolygon(ground_truth_polygons).centroid
        shifted_polygons = [affinity.rotate(affinity.translate(polygon,tx,ty),angle,origin=origin) for polygon in ground_truth_polygons]

        translated_polygons,rotated_polygons = self.moving_polygons_by_svd_(shifted_polygons,ground_truth_polygons)

        _, axs = plt.subplots(2,2)
        self.plot(ground_truth_polygons,axs[0,0])
        axs[0,0].set_title("Ground Truth")
        self.plot(shifted_polygons,axs[0,1])
        axs[0,1].set_title("Shifted")
        self.plot(translated_polygons,axs[1,0])
        axs[1,0].set_title("translated")
        self.plot(rotated_polygons,axs[1,1])
        axs[1,1].set_title("rotated")

        plt.show()

        assert rotated_polygons[0].centroid.distance(ground_truth_polygons[0].centroid) < 1


class TestRegistrationNoweights(unittest.TestCase):

    def plot(self,polygons, ax = None):

        if ax is None:
            _,ax = plt.subplots()
        
        random.seed(10)

        for poly in polygons:
            xs,ys = poly.exterior.xy
            ax.fill(xs,ys, alpha=0.5,fc=(random.random(),random.random(),random.random()),ec="black")

        ax.set_aspect("equal")

    def test_toy(self):
        db = "0-30"
        puzzle_num = "19_DB1"
        puzzle_noise_level = 0
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        ground_truth_polygons = puzzle.get_ground_truth_puzzle()

        tx = 3000 # 0
        ty = 3000 # 0
        angle = 50 #50
        origin = MultiPolygon(ground_truth_polygons).centroid
        shifted_polygons = [affinity.rotate(affinity.translate(polygon,tx,ty),angle,origin=origin) for polygon in ground_truth_polygons]

        q_pos,translated_polygons,rotated_polygons = registration_only_one_piece(shifted_polygons,ground_truth_polygons)

        _, axs = plt.subplots(2,2)
        self.plot(ground_truth_polygons,axs[0,0])
        axs[0,0].set_title("Ground Truth")
        self.plot(shifted_polygons,axs[0,1])
        axs[0,1].set_title("Shifted")
        self.plot(translated_polygons,axs[1,0])
        axs[1,0].set_title("translated")
        self.plot(rotated_polygons,axs[1,1])
        axs[1,1].set_title("rotated")

        plt.show()



if __name__ == "__main__":
    unittest.main()