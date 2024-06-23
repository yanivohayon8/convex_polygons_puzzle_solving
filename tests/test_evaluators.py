import unittest
import sys
sys.path.append("./")

from src.evaluator import least_square_rigid_motion_svd,AreaOverlappingEvaluator,registration_only_one_piece,Qpos
import numpy as np
from src.data_types.puzzle import Puzzle
from shapely import affinity
from src import shared_variables
import matplotlib.pyplot as plt
from shapely import Polygon,MultiPolygon
import random

from functools import reduce

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


    def moving_by_one_piece(self,solution_polygons,ground_truth_polygons):
        pieces_areas = list(map(lambda p: p.area,ground_truth_polygons))
        largest_piece_index = pieces_areas.index(max(pieces_areas))

        solution_largest_polygon = solution_polygons[largest_piece_index]
        ground_truth_largest_polygon = ground_truth_polygons[largest_piece_index]
        ground_truth_coords = np.array(solution_largest_polygon.exterior.coords)
        ground_truth_truth_coords = np.array(ground_truth_largest_polygon.exterior.coords)
        weights = np.ones(ground_truth_coords.shape[0])
        R,t = least_square_rigid_motion_svd(ground_truth_coords,ground_truth_truth_coords,weights)

        center_of_all = MultiPolygon(solution_polygons).centroid
        angle = np.arccos(R[0,0])
        rotated_polygons = [affinity.rotate(polygon,-angle,use_radians=True,origin=center_of_all) for polygon in solution_polygons]
        
        # t = solution_largest_polygon.centroid - ground_truth_largest_polygon.centroid
        t = MultiPolygon(ground_truth_polygons).centroid - MultiPolygon(rotated_polygons).centroid
        translated_polygons = [affinity.translate(polygon,t.x,t.y) for polygon in rotated_polygons]

        # translated_polygons = [affinity.translate(rot_polygon,-(gt_polygon.centroid.x - rot_polygon.centroid.x) ,-(gt_polygon.centroid.y - rot_polygon.centroid.y)) for rot_polygon,gt_polygon in zip(rotated_polygons,solution_polygons)]

        return translated_polygons,rotated_polygons
   
    def moving_polygons_by_svd_alll(self,solution_polygons,ground_truth_polygons):
        total_area = reduce(lambda acc,polygon: acc+polygon.area,solution_polygons,0)
        weights = np.array([polygon.area/(total_area+1e-5) for polygon in solution_polygons for _ in list(polygon.exterior.coords)[:-1]])
        # weights = np.array([1 for polygon in solution_polygons for _ in list(polygon.exterior.coords)])
        solution_points = np.array([coord for polygon in solution_polygons for coord in list(polygon.exterior.coords)[:-1]])
        ground_truth_points = np.array([coord for polygon in ground_truth_polygons for coord in list(polygon.exterior.coords)[:-1]])
        R,t = least_square_rigid_motion_svd(solution_points,ground_truth_points,weights)

        center_of_all = MultiPolygon(solution_polygons).centroid
        angle = np.arccos(R[0,0])
        rotated_polygons = [affinity.rotate(polygon,-angle,use_radians=True,origin=center_of_all) for polygon in solution_polygons]
        translated_polygons = [affinity.translate(polygon,t[0],t[1]) for polygon in rotated_polygons]
        
        # translated_polygons = [affinity.translate(polygon,-3000,-4500) for polygon in rotated_polygons]

        return translated_polygons,rotated_polygons

    def test_svd_reliablity(self):
        db = "0-30"
        puzzle_num = "19_DB1"
        puzzle_noise_level = 1
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        ground_truth_polygons = puzzle.get_ground_truth_puzzle()

        tx = 3000 # 0
        ty = 4500 # 0
        angle = 50 #2 #50
        origin = MultiPolygon(ground_truth_polygons).centroid
        shifted_polygons = [affinity.rotate(affinity.translate(polygon,tx,ty),angle,origin=origin) for polygon in ground_truth_polygons]

        # translated_polygons,rotated_polygons = self.moving_by_one_piece(shifted_polygons,ground_truth_polygons)
        translated_polygons,rotated_polygons = self.moving_polygons_by_svd_alll(shifted_polygons,ground_truth_polygons)

        _, axs = plt.subplots(2,2)
        self.plot(ground_truth_polygons,axs[0,0])
        axs[0,0].set_title("Ground Truth")
        self.plot(shifted_polygons,axs[0,1])
        axs[0,1].set_title("Shifted")
        self.plot(rotated_polygons,axs[1,0])
        axs[1,0].set_title("rotated")
        self.plot(translated_polygons,axs[1,1])
        axs[1,1].set_title("translated")

        plt.show()

        assert rotated_polygons[0].centroid.distance(ground_truth_polygons[0].centroid) < 1


class TestRegistrationNoweights(unittest.TestCase):

    def plot(self,polygons, ax = None,seed = 10):

        if ax is None:
            _,ax = plt.subplots()
        
        random.seed(seed)

        for poly in polygons:
            xs,ys = poly.exterior.xy
            ax.fill(xs,ys, alpha=0.5,fc=(random.random(),random.random(),random.random()),ec="black")

        ax.set_aspect("equal")

    def test_toy(self):
        db = "0-30"
        puzzle_num = "19_DB1"
        puzzle_noise_level = 1
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


    def poc_response(self,ground_truth_polygons,response, chosen_piece_index):
        _, axs = plt.subplots()

        self.plot(ground_truth_polygons,axs)

        solution_polygons = [Polygon(piece_json["coordinates"]) for piece_json in response["piecesFinalCoords"]]
        center_of_solution = MultiPolygon(solution_polygons).centroid
        fixed_piece = 5

        pieces_areas = list(map(lambda p: p.area,ground_truth_polygons))
        # chosen_piece_index = 1#0#pieces_areas.index(max(pieces_areas))

        solution_largest_polygon = solution_polygons[chosen_piece_index]
        ground_truth_largest_polygon = ground_truth_polygons[chosen_piece_index]
        solution_coords = np.array(solution_largest_polygon.exterior.coords)[:-1]
        ground_truth_truth_coords = np.array(ground_truth_largest_polygon.exterior.coords)[:-1]
        weights = np.ones(solution_coords.shape[0])
        R,t = least_square_rigid_motion_svd(solution_coords,ground_truth_truth_coords,weights)

        angle = np.arccos(R[0,0])
        final_solution_polygons = [affinity.rotate(polygon,-angle,use_radians=True,origin=center_of_solution) for polygon in solution_polygons]

        tx = ground_truth_largest_polygon.centroid.x-final_solution_polygons[chosen_piece_index].centroid.x
        ty = ground_truth_largest_polygon.centroid.y-final_solution_polygons[chosen_piece_index].centroid.y

        final_solution_polygons = [affinity.translate(polygon,tx,ty) for polygon in final_solution_polygons]
        # final_solution_polygons = [affinity.translate(polygon,t[0],t[1]) for polygon in final_solution_polygons]


        self.plot(final_solution_polygons,axs,seed=9)



        plt.show()


    def test_poc_response(self):
        db = "0-30"
        puzzle_num = "19_DB1"
        puzzle_noise_level = 1
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        ground_truth_polygons = puzzle.get_ground_truth_puzzle()

        response = {
            "AfterEnableCollision": {
                "springs": [
                    {
                        "firstPieceId": "7",
                        "firstPieceVertex": 1,
                        "secondPieceId": "9",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 10.142101287841797
                    },
                    {
                        "firstPieceId": "7",
                        "firstPieceVertex": 2,
                        "secondPieceId": "9",
                        "secondPieceVertex": 3,
                        "snapshotedLength": 11.260101318359375
                    },
                    {
                        "firstPieceId": "7",
                        "firstPieceVertex": 0,
                        "secondPieceId": "8",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 20.635299682617188
                    },
                    {
                        "firstPieceId": "7",
                        "firstPieceVertex": 1,
                        "secondPieceId": "8",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 20.327173233032227
                    },
                    {
                        "firstPieceId": "8",
                        "firstPieceVertex": 1,
                        "secondPieceId": "9",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 15.948013305664063
                    },
                    {
                        "firstPieceId": "8",
                        "firstPieceVertex": 2,
                        "secondPieceId": "9",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 14.22866153717041
                    },
                    {
                        "firstPieceId": "6",
                        "firstPieceVertex": 1,
                        "secondPieceId": "9",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 13.986743927001953
                    },
                    {
                        "firstPieceId": "6",
                        "firstPieceVertex": 2,
                        "secondPieceId": "9",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 15.092012405395508
                    },
                    {
                        "firstPieceId": "0",
                        "firstPieceVertex": 2,
                        "secondPieceId": "8",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 7.531733989715576
                    },
                    {
                        "firstPieceId": "0",
                        "firstPieceVertex": 3,
                        "secondPieceId": "8",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 12.917973518371582
                    },
                    {
                        "firstPieceId": "5",
                        "firstPieceVertex": 2,
                        "secondPieceId": "6",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 15.013673782348633
                    },
                    {
                        "firstPieceId": "5",
                        "firstPieceVertex": 3,
                        "secondPieceId": "6",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 14.896913528442383
                    },
                    {
                        "firstPieceId": "4",
                        "firstPieceVertex": 1,
                        "secondPieceId": "6",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 9.381514549255371
                    },
                    {
                        "firstPieceId": "4",
                        "firstPieceVertex": 2,
                        "secondPieceId": "6",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 11.278538703918457
                    },
                    {
                        "firstPieceId": "5",
                        "firstPieceVertex": 3,
                        "secondPieceId": "0",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 17.220252990722656
                    },
                    {
                        "firstPieceId": "5",
                        "firstPieceVertex": 0,
                        "secondPieceId": "0",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 17.102039337158203
                    },
                    {
                        "firstPieceId": "0",
                        "firstPieceVertex": 0,
                        "secondPieceId": "1",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 11.324124336242676
                    },
                    {
                        "firstPieceId": "0",
                        "firstPieceVertex": 1,
                        "secondPieceId": "1",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 11.957756996154785
                    },
                    {
                        "firstPieceId": "3",
                        "firstPieceVertex": 1,
                        "secondPieceId": "5",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 11.744946479797363
                    },
                    {
                        "firstPieceId": "3",
                        "firstPieceVertex": 2,
                        "secondPieceId": "5",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 10.237936973571777
                    },
                    {
                        "firstPieceId": "2",
                        "firstPieceVertex": 1,
                        "secondPieceId": "5",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 21.767284393310547
                    },
                    {
                        "firstPieceId": "2",
                        "firstPieceVertex": 2,
                        "secondPieceId": "5",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 21.589750289916992
                    },
                    {
                        "firstPieceId": "3",
                        "firstPieceVertex": 0,
                        "secondPieceId": "4",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 10.96021556854248
                    },
                    {
                        "firstPieceId": "3",
                        "firstPieceVertex": 1,
                        "secondPieceId": "4",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 8.148117065429688
                    },
                    {
                        "firstPieceId": "3",
                        "firstPieceVertex": 2,
                        "secondPieceId": "2",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 19.059406280517578
                    },
                    {
                        "firstPieceId": "3",
                        "firstPieceVertex": 0,
                        "secondPieceId": "2",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 14.149581909179688
                    },
                    {
                        "firstPieceId": "1",
                        "firstPieceVertex": 1,
                        "secondPieceId": "2",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 12.62522029876709
                    },
                    {
                        "firstPieceId": "1",
                        "firstPieceVertex": 2,
                        "secondPieceId": "2",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 18.883333206176758
                    }
                ],
                "sumSpringsLength": 386.0
            },
            "piecesBeforeEnableCollision": [
                {
                    "coordinates": [
                        [
                            1930.1241455078125,
                            478.7597351074219
                        ],
                        [
                            1529.546630859375,
                            245.06185913085938
                        ],
                        [
                            -16.576766967773438,
                            682.7735595703125
                        ],
                        [
                            678.8386840820313,
                            1548.4256591796875
                        ]
                    ],
                    "pieceId": "0"
                },
                {
                    "coordinates": [
                        [
                            1936.2601318359375,
                            488.2793273925781
                        ],
                        [
                            1865.0911865234375,
                            -451.6658630371094
                        ],
                        [
                            1521.1409912109375,
                            236.55889892578125
                        ]
                    ],
                    "pieceId": "1"
                },
                {
                    "coordinates": [
                        [
                            1872.827392578125,
                            -441.6885070800781
                        ],
                        [
                            1479.560791015625,
                            126.71660614013672
                        ],
                        [
                            1503.2862548828125,
                            230.41151428222656
                        ]
                    ],
                    "pieceId": "2"
                },
                {
                    "coordinates": [
                        [
                            1885.993896484375,
                            -436.5062561035156
                        ],
                        [
                            739.084228515625,
                            11.081694602966309
                        ],
                        [
                            1469.1905517578125,
                            110.7234878540039
                        ]
                    ],
                    "pieceId": "3"
                },
                {
                    "coordinates": [
                        [
                            1875.2860107421875,
                            -438.84466552734375
                        ],
                        [
                            -260.4713439941406,
                            -4.7607421875
                        ],
                        [
                            740.8103637695313,
                            3.1185147762298584
                        ]
                    ],
                    "pieceId": "4"
                },
                {
                    "coordinates": [
                        [
                            1513.0748291015625,
                            249.65475463867188
                        ],
                        [
                            1460.519775390625,
                            116.1689682006836
                        ],
                        [
                            742.9752197265625,
                            0.0
                        ],
                        [
                            0.0,
                            678.110107421875
                        ]
                    ],
                    "pieceId": "5"
                },
                {
                    "coordinates": [
                        [
                            732.6068725585938,
                            10.858534812927246
                        ],
                        [
                            -264.0743103027344,
                            -13.422011375427246
                        ],
                        [
                            5.653380870819092,
                            664.3275756835938
                        ]
                    ],
                    "pieceId": "6"
                },
                {
                    "coordinates": [
                        [
                            670.642822265625,
                            1545.0858154296875
                        ],
                        [
                            7.158278942108154,
                            936.2391967773438
                        ],
                        [
                            -379.63482666015625,
                            1472.7401123046875
                        ]
                    ],
                    "pieceId": "7"
                },
                {
                    "coordinates": [
                        [
                            685.2988891601563,
                            1559.6121826171875
                        ],
                        [
                            -12.493132591247559,
                            689.1021118164063
                        ],
                        [
                            -4.0378570556640625,
                            919.2733154296875
                        ]
                    ],
                    "pieceId": "8"
                },
                {
                    "coordinates": [
                        [
                            -2.586364507675171,
                            933.4277954101563
                        ],
                        [
                            -4.985809326171875,
                            675.0316162109375
                        ],
                        [
                            -262.9203796386719,
                            -27.36091423034668
                        ],
                        [
                            -370.9144287109375,
                            1479.865966796875
                        ]
                    ],
                    "pieceId": "9"
                }
            ],
            "piecesFinalCoords": [
                {
                    "coordinates": [
                        [
                            1930.1241455078125,
                            478.7597351074219
                        ],
                        [
                            1529.546630859375,
                            245.06185913085938
                        ],
                        [
                            -16.576766967773438,
                            682.7735595703125
                        ],
                        [
                            678.8386840820313,
                            1548.4256591796875
                        ]
                    ],
                    "pieceId": "0"
                },
                {
                    "coordinates": [
                        [
                            1936.2601318359375,
                            488.2793273925781
                        ],
                        [
                            1865.0911865234375,
                            -451.6658630371094
                        ],
                        [
                            1521.1409912109375,
                            236.55889892578125
                        ]
                    ],
                    "pieceId": "1"
                },
                {
                    "coordinates": [
                        [
                            1872.827392578125,
                            -441.6885070800781
                        ],
                        [
                            1479.560791015625,
                            126.71660614013672
                        ],
                        [
                            1503.2862548828125,
                            230.41151428222656
                        ]
                    ],
                    "pieceId": "2"
                },
                {
                    "coordinates": [
                        [
                            1885.993896484375,
                            -436.5062561035156
                        ],
                        [
                            739.084228515625,
                            11.081694602966309
                        ],
                        [
                            1469.1905517578125,
                            110.7234878540039
                        ]
                    ],
                    "pieceId": "3"
                },
                {
                    "coordinates": [
                        [
                            1875.2860107421875,
                            -438.84466552734375
                        ],
                        [
                            -260.4713439941406,
                            -4.7607421875
                        ],
                        [
                            740.8103637695313,
                            3.1185147762298584
                        ]
                    ],
                    "pieceId": "4"
                },
                {
                    "coordinates": [
                        [
                            1513.0748291015625,
                            249.65475463867188
                        ],
                        [
                            1460.519775390625,
                            116.1689682006836
                        ],
                        [
                            742.9752197265625,
                            0.0
                        ],
                        [
                            0.0,
                            678.110107421875
                        ]
                    ],
                    "pieceId": "5"
                },
                {
                    "coordinates": [
                        [
                            732.6068725585938,
                            10.858534812927246
                        ],
                        [
                            -264.0743103027344,
                            -13.422011375427246
                        ],
                        [
                            5.653380870819092,
                            664.3275756835938
                        ]
                    ],
                    "pieceId": "6"
                },
                {
                    "coordinates": [
                        [
                            670.642822265625,
                            1545.0858154296875
                        ],
                        [
                            7.158278942108154,
                            936.2391967773438
                        ],
                        [
                            -379.63482666015625,
                            1472.7401123046875
                        ]
                    ],
                    "pieceId": "7"
                },
                {
                    "coordinates": [
                        [
                            685.2988891601563,
                            1559.6121826171875
                        ],
                        [
                            -12.493132591247559,
                            689.1021118164063
                        ],
                        [
                            -4.0378570556640625,
                            919.2733154296875
                        ]
                    ],
                    "pieceId": "8"
                },
                {
                    "coordinates": [
                        [
                            -2.586364507675171,
                            933.4277954101563
                        ],
                        [
                            -4.985809326171875,
                            675.0316162109375
                        ],
                        [
                            -262.9203796386719,
                            -27.36091423034668
                        ],
                        [
                            -370.9144287109375,
                            1479.865966796875
                        ]
                    ],
                    "pieceId": "9"
                }
            ],
            "piecesFinalTransformation": [
                {
                    "pieceId": "0",
                    "rotationRadians": -2.657514810562134,
                    "translateVectorX": 928.5106201171875,
                    "translateVectorY": 804.6798095703125
                },
                {
                    "pieceId": "1",
                    "rotationRadians": -18.95050621032715,
                    "translateVectorX": 1774.1640625,
                    "translateVectorY": 91.05681610107422
                },
                {
                    "pieceId": "2",
                    "rotationRadians": -0.8310062289237976,
                    "translateVectorX": 1618.556884765625,
                    "translateVectorY": -28.186796188354492
                },
                {
                    "pieceId": "3",
                    "rotationRadians": 3.585374593734741,
                    "translateVectorX": 1364.755615234375,
                    "translateVectorY": -104.90035247802734
                },
                {
                    "pieceId": "4",
                    "rotationRadians": -9.907032012939453,
                    "translateVectorX": 785.2077026367188,
                    "translateVectorY": -146.82960510253906
                },
                {
                    "pieceId": "5",
                    "rotationRadians": 0.0,
                    "translateVectorX": 0.0,
                    "translateVectorY": 0.0
                },
                {
                    "pieceId": "6",
                    "rotationRadians": -2.453127861022949,
                    "translateVectorX": 158.06198120117188,
                    "translateVectorY": 220.5886688232422
                },
                {
                    "pieceId": "7",
                    "rotationRadians": 1.8316062688827515,
                    "translateVectorX": 99.38811492919922,
                    "translateVectorY": 1318.021728515625
                },
                {
                    "pieceId": "8",
                    "rotationRadians": 6.320694923400879,
                    "translateVectorX": 222.9232635498047,
                    "translateVectorY": 1055.995849609375
                },
                {
                    "pieceId": "9",
                    "rotationRadians": -43.570457458496094,
                    "translateVectorX": -198.01901245117188,
                    "translateVectorY": 764.249755859375
                }
            ]
        }

        
        self.poc_response(ground_truth_polygons,response,0)



    def test_poc_response_puzzle_20(self):
        db = "0-30"
        puzzle_num = "20_DB1"
        puzzle_noise_level = 0 
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        ground_truth_polygons = puzzle.get_ground_truth_puzzle()
        

        response = {
    "AfterEnableCollision": {
        "springs": [
            {
                "firstPieceId": "0",
                "firstPieceVertex": 0,
                "secondPieceId": "1",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.877740859985352
            },
            {
                "firstPieceId": "0",
                "firstPieceVertex": 1,
                "secondPieceId": "1",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.5752534866333
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 1,
                "secondPieceId": "6",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.62152099609375
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 2,
                "secondPieceId": "6",
                "secondPieceVertex": 2,
                "snapshotedLength": 11.187615394592285
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 0,
                "secondPieceId": "2",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.565146446228027
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 1,
                "secondPieceId": "2",
                "secondPieceVertex": 3,
                "snapshotedLength": 10.814048767089844
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 2,
                "secondPieceId": "6",
                "secondPieceVertex": 1,
                "snapshotedLength": 9.05125904083252
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 3,
                "secondPieceId": "6",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.0037202835083
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 1,
                "secondPieceId": "3",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.638257026672363
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 2,
                "secondPieceId": "3",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.946775436401367
            },
            {
                "firstPieceId": "3",
                "firstPieceVertex": 1,
                "secondPieceId": "6",
                "secondPieceVertex": 2,
                "snapshotedLength": 12.007481575012207
            },
            {
                "firstPieceId": "3",
                "firstPieceVertex": 2,
                "secondPieceId": "6",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.624547958374023
            },
            {
                "firstPieceId": "3",
                "firstPieceVertex": 0,
                "secondPieceId": "4",
                "secondPieceVertex": 0,
                "snapshotedLength": 11.04115104675293
            },
            {
                "firstPieceId": "3",
                "firstPieceVertex": 1,
                "secondPieceId": "4",
                "secondPieceVertex": 3,
                "snapshotedLength": 12.949817657470703
            },
            {
                "firstPieceId": "4",
                "firstPieceVertex": 2,
                "secondPieceId": "9",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.348978996276855
            },
            {
                "firstPieceId": "4",
                "firstPieceVertex": 3,
                "secondPieceId": "9",
                "secondPieceVertex": 3,
                "snapshotedLength": 11.090944290161133
            },
            {
                "firstPieceId": "4",
                "firstPieceVertex": 1,
                "secondPieceId": "7",
                "secondPieceVertex": 0,
                "snapshotedLength": 6.518191814422607
            },
            {
                "firstPieceId": "4",
                "firstPieceVertex": 2,
                "secondPieceId": "7",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.9669828414917
            },
            {
                "firstPieceId": "4",
                "firstPieceVertex": 0,
                "secondPieceId": "5",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.443843841552734
            },
            {
                "firstPieceId": "4",
                "firstPieceVertex": 1,
                "secondPieceId": "5",
                "secondPieceVertex": 2,
                "snapshotedLength": 13.6191987991333
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 1,
                "secondPieceId": "8",
                "secondPieceVertex": 1,
                "snapshotedLength": 11.657068252563477
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 2,
                "secondPieceId": "8",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.543535232543945
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 1,
                "secondPieceId": "9",
                "secondPieceVertex": 1,
                "snapshotedLength": 8.04755687713623
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 2,
                "secondPieceId": "9",
                "secondPieceVertex": 0,
                "snapshotedLength": 7.4482102394104
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 0,
                "secondPieceId": "8",
                "secondPieceVertex": 0,
                "snapshotedLength": 20.964881896972656
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 1,
                "secondPieceId": "8",
                "secondPieceVertex": 2,
                "snapshotedLength": 8.675169944763184
            },
            {
                "firstPieceId": "8",
                "firstPieceVertex": 1,
                "secondPieceId": "9",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.787622451782227
            },
            {
                "firstPieceId": "8",
                "firstPieceVertex": 2,
                "secondPieceId": "9",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.612993240356445
            }
        ],
        "sumSpringsLength": 286.0
    },
    "piecesBeforeEnableCollision": [
        {
            "coordinates": [
                [
                    121.5724868774414,
                    586.669921875
                ],
                [
                    2586.11083984375,
                    14.513014793395996
                ],
                [
                    1553.4591064453125,
                    -237.5755157470703
                ]
            ],
            "pieceId": "0"
        },
        {
            "coordinates": [
                [
                    117.65860748291016,
                    577.1942138671875
                ],
                [
                    483.8046875,
                    900.0853881835938
                ],
                [
                    2582.216064453125,
                    5.123137950897217
                ]
            ],
            "pieceId": "1"
        },
        {
            "coordinates": [
                [
                    123.61144256591797,
                    567.8272094726563
                ],
                [
                    0.0743865966796875,
                    1533.6302490234375
                ],
                [
                    497.62152099609375,
                    1052.244140625
                ],
                [
                    488.5539855957031,
                    892.078369140625
                ]
            ],
            "pieceId": "2"
        },
        {
            "coordinates": [
                [
                    -6.971358776092529,
                    1525.2113037109375
                ],
                [
                    2588.43017578125,
                    5.350112438201904
                ],
                [
                    492.21417236328125,
                    1045.5245361328125
                ]
            ],
            "pieceId": "3"
        },
        {
            "coordinates": [
                [
                    0.0,
                    1517.871826171875
                ],
                [
                    1214.109375,
                    1288.1107177734375
                ],
                [
                    2127.345947265625,
                    484.1003112792969
                ],
                [
                    2596.567138671875,
                    0.0
                ]
            ],
            "pieceId": "4"
        },
        {
            "coordinates": [
                [
                    10.091780662536621,
                    1521.9306640625
                ],
                [
                    2230.40771484375,
                    1473.255126953125
                ],
                [
                    1223.05859375,
                    1286.2242431640625
                ]
            ],
            "pieceId": "5"
        },
        {
            "coordinates": [
                [
                    478.56329345703125,
                    892.2328491210938
                ],
                [
                    486.89459228515625,
                    1052.438720703125
                ],
                [
                    2584.339111328125,
                    14.739989280700684
                ]
            ],
            "pieceId": "6"
        },
        {
            "coordinates": [
                [
                    1216.073974609375,
                    1279.8060302734375
                ],
                [
                    2089.622314453125,
                    747.4822387695313
                ],
                [
                    2139.53955078125,
                    487.5640563964844
                ]
            ],
            "pieceId": "7"
        },
        {
            "coordinates": [
                [
                    1226.6998291015625,
                    1278.86962890625
                ],
                [
                    2230.880615234375,
                    1482.223388671875
                ],
                [
                    2099.456787109375,
                    745.248779296875
                ]
            ],
            "pieceId": "8"
        },
        {
            "coordinates": [
                [
                    2135.80126953125,
                    479.1812744140625
                ],
                [
                    2088.245361328125,
                    739.5419921875
                ],
                [
                    2225.2578125,
                    1475.4981689453125
                ],
                [
                    2606.83056640625,
                    -3.158569097518921
                ]
            ],
            "pieceId": "9"
        }
    ],
    "piecesFinalCoords": [
        {
            "coordinates": [
                [
                    119.68611907958984,
                    512.0487060546875
                ],
                [
                    2587.82177734375,
                    -44.380184173583984
                ],
                [
                    1556.798828125,
                    -303.049072265625
                ]
            ],
            "pieceId": "0"
        },
        {
            "coordinates": [
                [
                    121.4198989868164,
                    522.7890014648438
                ],
                [
                    485.55181884765625,
                    847.949951171875
                ],
                [
                    2589.49072265625,
                    -33.939361572265625
                ]
            ],
            "pieceId": "1"
        },
        {
            "coordinates": [
                [
                    118.15070343017578,
                    532.8311767578125
                ],
                [
                    -8.342742919921875,
                    1498.2508544921875
                ],
                [
                    490.6768493652344,
                    1018.390625
                ],
                [
                    482.0995178222656,
                    858.1981201171875
                ]
            ],
            "pieceId": "2"
        },
        {
            "coordinates": [
                [
                    -2.445220947265625,
                    1507.1048583984375
                ],
                [
                    2593.11865234375,
                    -12.481688499450684
                ],
                [
                    496.7899169921875,
                    1027.471435546875
                ]
            ],
            "pieceId": "3"
        },
        {
            "coordinates": [
                [
                    0.0,
                    1517.871826171875
                ],
                [
                    1214.109375,
                    1288.1107177734375
                ],
                [
                    2127.345947265625,
                    484.1003112792969
                ],
                [
                    2596.567138671875,
                    0.0
                ]
            ],
            "pieceId": "4"
        },
        {
            "coordinates": [
                [
                    4.0454864501953125,
                    1526.4052734375
                ],
                [
                    2224.69140625,
                    1496.286376953125
                ],
                [
                    1218.940673828125,
                    1300.8441162109375
                ]
            ],
            "pieceId": "5"
        },
        {
            "coordinates": [
                [
                    491.0278015136719,
                    857.0499267578125
                ],
                [
                    499.65283203125,
                    1017.240478515625
                ],
                [
                    2595.18798828125,
                    -24.30915641784668
                ]
            ],
            "pieceId": "6"
        },
        {
            "coordinates": [
                [
                    1212.29931640625,
                    1281.848876953125
                ],
                [
                    2086.259765625,
                    750.2021484375
                ],
                [
                    2136.377197265625,
                    490.32208251953125
                ]
            ],
            "pieceId": "7"
        },
        {
            "coordinates": [
                [
                    1227.3883056640625,
                    1296.40380859375
                ],
                [
                    2233.707275390625,
                    1488.897216796875
                ],
                [
                    2094.329833984375,
                    753.385498046875
                ]
            ],
            "pieceId": "8"
        },
        {
            "coordinates": [
                [
                    2137.63427734375,
                    482.980712890625
                ],
                [
                    2090.623779296875,
                    743.4406127929688
                ],
                [
                    2229.177490234375,
                    1479.1068115234375
                ],
                [
                    2607.652587890625,
                    -0.3471374213695526
                ]
            ],
            "pieceId": "9"
        }
    ],
    "piecesFinalTransformation": [
        {
            "pieceId": "0",
            "rotationRadians": 12.951749801635742,
            "translateVectorX": 1421.436279296875,
            "translateVectorY": 54.87250900268555
        },
        {
            "pieceId": "1",
            "rotationRadians": 15.531571388244629,
            "translateVectorX": 1065.48681640625,
            "translateVectorY": 445.6004943847656
        },
        {
            "pieceId": "2",
            "rotationRadians": -26.31316566467285,
            "translateVectorX": 219.2039337158203,
            "translateVectorY": 991.6400146484375
        },
        {
            "pieceId": "3",
            "rotationRadians": -0.9080601930618286,
            "translateVectorX": 1029.15380859375,
            "translateVectorY": 840.6981811523438
        },
        {
            "pieceId": "4",
            "rotationRadians": 0.0,
            "translateVectorX": 0.0,
            "translateVectorY": 0.0
        },
        {
            "pieceId": "5",
            "rotationRadians": -1.6413837671279907,
            "translateVectorX": 1149.2252197265625,
            "translateVectorY": 1441.17919921875
        },
        {
            "pieceId": "6",
            "rotationRadians": 21.19413948059082,
            "translateVectorX": 1195.28955078125,
            "translateVectorY": 616.6610717773438
        },
        {
            "pieceId": "7",
            "rotationRadians": -17.420860290527344,
            "translateVectorX": 1811.6453857421875,
            "translateVectorY": 840.7916870117188
        },
        {
            "pieceId": "8",
            "rotationRadians": -0.9184766411781311,
            "translateVectorX": 1851.8084716796875,
            "translateVectorY": 1179.5615234375
        },
        {
            "pieceId": "9",
            "rotationRadians": 2.116039276123047,
            "translateVectorX": 2303.93408203125,
            "translateVectorY": 683.9618530273438
        }
    ]
}


        self.poc_response(ground_truth_polygons,response,0)

    def test_poc_response_puzzle_19DBPAST2staged(self):
        db = "0-30"
        puzzle_num = "19DBPAST2staged"
        puzzle_noise_level = 0 
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        ground_truth_polygons = puzzle.get_ground_truth_puzzle()

        response = {
        
        
    "AfterEnableCollision": {
        "springs": [
            {
                "firstPieceId": "0",
                "firstPieceVertex": 0,
                "secondPieceId": "1",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.917414665222168
            },
            {
                "firstPieceId": "0",
                "firstPieceVertex": 1,
                "secondPieceId": "1",
                "secondPieceVertex": 3,
                "snapshotedLength": 10.219512939453125
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 2,
                "secondPieceId": "4",
                "secondPieceVertex": 1,
                "snapshotedLength": 9.87955379486084
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 3,
                "secondPieceId": "4",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.234469413757324
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 1,
                "secondPieceId": "2",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.434589385986328
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 2,
                "secondPieceId": "2",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.87761116027832
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 1,
                "secondPieceId": "6",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.522393226623535
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 2,
                "secondPieceId": "6",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.229329109191895
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 0,
                "secondPieceId": "3",
                "secondPieceVertex": 0,
                "snapshotedLength": 11.008228302001953
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 1,
                "secondPieceId": "3",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.297056198120117
            },
            {
                "firstPieceId": "3",
                "firstPieceVertex": 1,
                "secondPieceId": "10",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.47563362121582
            },
            {
                "firstPieceId": "3",
                "firstPieceVertex": 2,
                "secondPieceId": "10",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.133009910583496
            },
            {
                "firstPieceId": "4",
                "firstPieceVertex": 1,
                "secondPieceId": "5",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.080572128295898
            },
            {
                "firstPieceId": "4",
                "firstPieceVertex": 2,
                "secondPieceId": "5",
                "secondPieceVertex": 3,
                "snapshotedLength": 10.049464225769043
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 2,
                "secondPieceId": "22",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.111474990844727
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 3,
                "secondPieceId": "22",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.023399353027344
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 1,
                "secondPieceId": "18",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.723337173461914
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 2,
                "secondPieceId": "18",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.91222858428955
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 0,
                "secondPieceId": "6",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.961305618286133
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 1,
                "secondPieceId": "6",
                "secondPieceVertex": 2,
                "snapshotedLength": 11.05591869354248
            },
            {
                "firstPieceId": "6",
                "firstPieceVertex": 1,
                "secondPieceId": "7",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.9026460647583
            },
            {
                "firstPieceId": "6",
                "firstPieceVertex": 2,
                "secondPieceId": "7",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.11030101776123
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 1,
                "secondPieceId": "11",
                "secondPieceVertex": 0,
                "snapshotedLength": 11.050721168518066
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 2,
                "secondPieceId": "11",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.954449653625488
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 0,
                "secondPieceId": "8",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.805530548095703
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 1,
                "secondPieceId": "8",
                "secondPieceVertex": 2,
                "snapshotedLength": 11.578559875488281
            },
            {
                "firstPieceId": "8",
                "firstPieceVertex": 1,
                "secondPieceId": "15",
                "secondPieceVertex": 1,
                "snapshotedLength": 15.260697364807129
            },
            {
                "firstPieceId": "8",
                "firstPieceVertex": 2,
                "secondPieceId": "15",
                "secondPieceVertex": 0,
                "snapshotedLength": 12.472540855407715
            },
            {
                "firstPieceId": "8",
                "firstPieceVertex": 0,
                "secondPieceId": "9",
                "secondPieceVertex": 0,
                "snapshotedLength": 13.62034797668457
            },
            {
                "firstPieceId": "8",
                "firstPieceVertex": 1,
                "secondPieceId": "9",
                "secondPieceVertex": 2,
                "snapshotedLength": 15.865697860717773
            },
            {
                "firstPieceId": "9",
                "firstPieceVertex": 1,
                "secondPieceId": "23",
                "secondPieceVertex": 3,
                "snapshotedLength": 10.785911560058594
            },
            {
                "firstPieceId": "9",
                "firstPieceVertex": 2,
                "secondPieceId": "23",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.540759086608887
            },
            {
                "firstPieceId": "9",
                "firstPieceVertex": 0,
                "secondPieceId": "10",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.374635696411133
            },
            {
                "firstPieceId": "9",
                "firstPieceVertex": 1,
                "secondPieceId": "10",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.522747039794922
            },
            {
                "firstPieceId": "10",
                "firstPieceVertex": 1,
                "secondPieceId": "16",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.860681533813477
            },
            {
                "firstPieceId": "10",
                "firstPieceVertex": 2,
                "secondPieceId": "16",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.082367897033691
            },
            {
                "firstPieceId": "11",
                "firstPieceVertex": 1,
                "secondPieceId": "18",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.508530616760254
            },
            {
                "firstPieceId": "11",
                "firstPieceVertex": 2,
                "secondPieceId": "18",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.498061180114746
            },
            {
                "firstPieceId": "11",
                "firstPieceVertex": 0,
                "secondPieceId": "12",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.915160179138184
            },
            {
                "firstPieceId": "11",
                "firstPieceVertex": 1,
                "secondPieceId": "12",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.116662979125977
            },
            {
                "firstPieceId": "12",
                "firstPieceVertex": 1,
                "secondPieceId": "21",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.204345703125
            },
            {
                "firstPieceId": "12",
                "firstPieceVertex": 2,
                "secondPieceId": "21",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.053685188293457
            },
            {
                "firstPieceId": "12",
                "firstPieceVertex": 0,
                "secondPieceId": "13",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.738227844238281
            },
            {
                "firstPieceId": "12",
                "firstPieceVertex": 1,
                "secondPieceId": "13",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.077652931213379
            },
            {
                "firstPieceId": "13",
                "firstPieceVertex": 1,
                "secondPieceId": "24",
                "secondPieceVertex": 1,
                "snapshotedLength": 9.837160110473633
            },
            {
                "firstPieceId": "13",
                "firstPieceVertex": 2,
                "secondPieceId": "24",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.277090072631836
            },
            {
                "firstPieceId": "13",
                "firstPieceVertex": 0,
                "secondPieceId": "14",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.339057922363281
            },
            {
                "firstPieceId": "13",
                "firstPieceVertex": 1,
                "secondPieceId": "14",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.025172233581543
            },
            {
                "firstPieceId": "14",
                "firstPieceVertex": 1,
                "secondPieceId": "25",
                "secondPieceVertex": 1,
                "snapshotedLength": 9.665310859680176
            },
            {
                "firstPieceId": "14",
                "firstPieceVertex": 2,
                "secondPieceId": "25",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.793017387390137
            },
            {
                "firstPieceId": "14",
                "firstPieceVertex": 0,
                "secondPieceId": "15",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.165597915649414
            },
            {
                "firstPieceId": "14",
                "firstPieceVertex": 1,
                "secondPieceId": "15",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.1922607421875
            },
            {
                "firstPieceId": "15",
                "firstPieceVertex": 1,
                "secondPieceId": "26",
                "secondPieceVertex": 1,
                "snapshotedLength": 9.982022285461426
            },
            {
                "firstPieceId": "15",
                "firstPieceVertex": 2,
                "secondPieceId": "26",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.001755714416504
            },
            {
                "firstPieceId": "16",
                "firstPieceVertex": 1,
                "secondPieceId": "23",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.910200119018555
            },
            {
                "firstPieceId": "16",
                "firstPieceVertex": 2,
                "secondPieceId": "23",
                "secondPieceVertex": 3,
                "snapshotedLength": 9.884443283081055
            },
            {
                "firstPieceId": "16",
                "firstPieceVertex": 0,
                "secondPieceId": "17",
                "secondPieceVertex": 0,
                "snapshotedLength": 11.357844352722168
            },
            {
                "firstPieceId": "16",
                "firstPieceVertex": 1,
                "secondPieceId": "17",
                "secondPieceVertex": 2,
                "snapshotedLength": 7.934224605560303
            },
            {
                "firstPieceId": "17",
                "firstPieceVertex": 1,
                "secondPieceId": "23",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.984820365905762
            },
            {
                "firstPieceId": "17",
                "firstPieceVertex": 2,
                "secondPieceId": "23",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.272586822509766
            },
            {
                "firstPieceId": "18",
                "firstPieceVertex": 1,
                "secondPieceId": "19",
                "secondPieceVertex": 0,
                "snapshotedLength": 11.634832382202148
            },
            {
                "firstPieceId": "18",
                "firstPieceVertex": 2,
                "secondPieceId": "19",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.025787353515625
            },
            {
                "firstPieceId": "19",
                "firstPieceVertex": 1,
                "secondPieceId": "22",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.230944633483887
            },
            {
                "firstPieceId": "19",
                "firstPieceVertex": 2,
                "secondPieceId": "22",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.15886402130127
            },
            {
                "firstPieceId": "19",
                "firstPieceVertex": 0,
                "secondPieceId": "20",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.328317642211914
            },
            {
                "firstPieceId": "19",
                "firstPieceVertex": 1,
                "secondPieceId": "20",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.41045093536377
            },
            {
                "firstPieceId": "20",
                "firstPieceVertex": 1,
                "secondPieceId": "22",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.079397201538086
            },
            {
                "firstPieceId": "20",
                "firstPieceVertex": 2,
                "secondPieceId": "22",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.554826736450195
            },
            {
                "firstPieceId": "20",
                "firstPieceVertex": 0,
                "secondPieceId": "21",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.65949821472168
            },
            {
                "firstPieceId": "20",
                "firstPieceVertex": 1,
                "secondPieceId": "21",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.138458251953125
            },
            {
                "firstPieceId": "21",
                "firstPieceVertex": 1,
                "secondPieceId": "24",
                "secondPieceVertex": 0,
                "snapshotedLength": 11.15848445892334
            },
            {
                "firstPieceId": "21",
                "firstPieceVertex": 2,
                "secondPieceId": "24",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.11844253540039
            },
            {
                "firstPieceId": "24",
                "firstPieceVertex": 1,
                "secondPieceId": "25",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.897817611694336
            },
            {
                "firstPieceId": "24",
                "firstPieceVertex": 2,
                "secondPieceId": "25",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.654745101928711
            },
            {
                "firstPieceId": "25",
                "firstPieceVertex": 1,
                "secondPieceId": "26",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.987682342529297
            },
            {
                "firstPieceId": "25",
                "firstPieceVertex": 2,
                "secondPieceId": "26",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.904173851013184
            }
        ],
        "sumSpringsLength": 751.0
    },
    "piecesBeforeEnableCollision": [
        {
            "coordinates": [
                [
                    -804.8419799804688,
                    5412.80517578125
                ],
                [
                    -91.2513656616211,
                    329.4200744628906
                ],
                [
                    -813.7645263671875,
                    1483.17138671875
                ]
            ],
            "pieceId": "0"
        },
        {
            "coordinates": [
                [
                    -812.1604614257813,
                    5406.1123046875
                ],
                [
                    -224.3003692626953,
                    8873.763671875
                ],
                [
                    -0.8411406874656677,
                    1889.289794921875
                ],
                [
                    -81.99691009521484,
                    325.0808410644531
                ]
            ],
            "pieceId": "1"
        },
        {
            "coordinates": [
                [
                    890.0546875,
                    10374.6767578125
                ],
                [
                    1672.086669921875,
                    12150.6796875
                ],
                [
                    5814.0810546875,
                    7048.21533203125
                ]
            ],
            "pieceId": "10"
        },
        {
            "coordinates": [
                [
                    945.2552490234375,
                    10282.2275390625
                ],
                [
                    1746.2271728515625,
                    5051.85693359375
                ],
                [
                    1680.6048583984375,
                    2556.562255859375
                ]
            ],
            "pieceId": "11"
        },
        {
            "coordinates": [
                [
                    947.5440673828125,
                    10291.875
                ],
                [
                    5452.52197265625,
                    1657.0948486328125
                ],
                [
                    1749.021484375,
                    5061.58251953125
                ]
            ],
            "pieceId": "12"
        },
        {
            "coordinates": [
                [
                    937.8394775390625,
                    10291.064453125
                ],
                [
                    5848.31005859375,
                    2503.560791015625
                ],
                [
                    5459.05078125,
                    1664.77197265625
                ]
            ],
            "pieceId": "13"
        },
        {
            "coordinates": [
                [
                    948.1620483398438,
                    10291.6484375
                ],
                [
                    6710.9599609375,
                    3306.3125
                ],
                [
                    5858.32763671875,
                    2503.953857421875
                ]
            ],
            "pieceId": "14"
        },
        {
            "coordinates": [
                [
                    957.954345703125,
                    10294.3779296875
                ],
                [
                    7649.0322265625,
                    5368.05322265625
                ],
                [
                    6720.771484375,
                    3309.060791015625
                ]
            ],
            "pieceId": "15"
        },
        {
            "coordinates": [
                [
                    1680.92529296875,
                    12155.0517578125
                ],
                [
                    3128.217529296875,
                    12108.70703125
                ],
                [
                    5823.09716796875,
                    7052.728515625
                ]
            ],
            "pieceId": "16"
        },
        {
            "coordinates": [
                [
                    1681.2724609375,
                    12166.408203125
                ],
                [
                    5333.236328125,
                    12752.73828125
                ],
                [
                    3128.4501953125,
                    12116.6376953125
                ]
            ],
            "pieceId": "17"
        },
        {
            "coordinates": [
                [
                    1671.8253173828125,
                    2552.9365234375
                ],
                [
                    1736.356689453125,
                    5048.26123046875
                ],
                [
                    2796.937744140625,
                    2012.67236328125
                ]
            ],
            "pieceId": "18"
        },
        {
            "coordinates": [
                [
                    1725.715576171875,
                    5052.970703125
                ],
                [
                    2390.2529296875,
                    3709.316162109375
                ],
                [
                    2798.284423828125,
                    2021.5968017578125
                ]
            ],
            "pieceId": "19"
        },
        {
            "coordinates": [
                [
                    -219.52818298339844,
                    8881.904296875
                ],
                [
                    872.8179321289063,
                    10367.3125
                ],
                [
                    -8.472442626953125,
                    1897.0450439453125
                ]
            ],
            "pieceId": "2"
        },
        {
            "coordinates": [
                [
                    1731.7332763671875,
                    5060.0986328125
                ],
                [
                    6702.5087890625,
                    -10.572432518005371
                ],
                [
                    2396.3525390625,
                    3716.48388671875
                ]
            ],
            "pieceId": "20"
        },
        {
            "coordinates": [
                [
                    1741.2203369140625,
                    5055.23828125
                ],
                [
                    5458.25732421875,
                    1665.534912109375
                ],
                [
                    6710.119140625,
                    -17.271041870117188
                ]
            ],
            "pieceId": "21"
        },
        {
            "coordinates": [
                [
                    2386.0185546875,
                    3718.627685546875
                ],
                [
                    6692.87060546875,
                    -7.621764659881592
                ],
                [
                    2794.4716796875,
                    2031.011474609375
                ]
            ],
            "pieceId": "22"
        },
        {
            "coordinates": [
                [
                    3137.05615234375,
                    12113.185546875
                ],
                [
                    5342.53466796875,
                    12746.890625
                ],
                [
                    7689.4453125,
                    5370.5078125
                ],
                [
                    5814.45654296875,
                    7047.927734375
                ]
            ],
            "pieceId": "23"
        },
        {
            "coordinates": [
                [
                    5469.28955078125,
                    1663.8602294921875
                ],
                [
                    5858.12158203125,
                    2502.84765625
                ],
                [
                    6718.46533203125,
                    -20.942686080932617
                ]
            ],
            "pieceId": "24"
        },
        {
            "coordinates": [
                [
                    5862.0126953125,
                    2513.027099609375
                ],
                [
                    6714.86083984375,
                    3315.15673828125
                ],
                [
                    6720.29638671875,
                    -11.463164329528809
                ]
            ],
            "pieceId": "25"
        },
        {
            "coordinates": [
                [
                    6724.30029296875,
                    3318.420166015625
                ],
                [
                    7653.1787109375,
                    5377.13427734375
                ],
                [
                    6729.646484375,
                    -8.20159912109375
                ]
            ],
            "pieceId": "26"
        },
        {
            "coordinates": [
                [
                    -209.09117126464844,
                    8885.404296875
                ],
                [
                    1678.0394287109375,
                    12142.0625
                ],
                [
                    880.033447265625,
                    10373.17578125
                ]
            ],
            "pieceId": "3"
        },
        {
            "coordinates": [
                [
                    -72.23892211914063,
                    328.1631164550781
                ],
                [
                    -9.901046752929688,
                    1893.236083984375
                ],
                [
                    6689.8056640625,
                    3.051757574081421
                ]
            ],
            "pieceId": "4"
        },
        {
            "coordinates": [
                [
                    0.0,
                    1891.342041015625
                ],
                [
                    1662.177978515625,
                    2551.725341796875
                ],
                [
                    2791.92724609375,
                    2021.224853515625
                ],
                [
                    6699.38037109375,
                    0.0
                ]
            ],
            "pieceId": "5"
        },
        {
            "coordinates": [
                [
                    -0.8640288710594177,
                    1902.269287109375
                ],
                [
                    864.8204345703125,
                    10374.1484375
                ],
                [
                    1668.9814453125,
                    2543.012451171875
                ]
            ],
            "pieceId": "6"
        },
        {
            "coordinates": [
                [
                    866.5504150390625,
                    10383.8994140625
                ],
                [
                    956.1519165039063,
                    10280.3876953125
                ],
                [
                    1671.375244140625,
                    2552.83349609375
                ]
            ],
            "pieceId": "7"
        },
        {
            "coordinates": [
                [
                    876.3884887695313,
                    10388.3681640625
                ],
                [
                    7664.29296875,
                    5368.06103515625
                ],
                [
                    966.5965576171875,
                    10285.384765625
                ]
            ],
            "pieceId": "8"
        },
        {
            "coordinates": [
                [
                    889.596923828125,
                    10385.0439453125
                ],
                [
                    5804.181640625,
                    7044.64892578125
                ],
                [
                    7680.15625,
                    5368.32958984375
                ]
            ],
            "pieceId": "9"
        }
    ],
    "piecesFinalCoords": [
        {
            "coordinates": [
                [
                    -804.8419799804688,
                    5412.80517578125
                ],
                [
                    -91.2513656616211,
                    329.4200744628906
                ],
                [
                    -813.7645263671875,
                    1483.17138671875
                ]
            ],
            "pieceId": "0"
        },
        {
            "coordinates": [
                [
                    -812.1604614257813,
                    5406.1123046875
                ],
                [
                    -224.3003692626953,
                    8873.763671875
                ],
                [
                    -0.8411406874656677,
                    1889.289794921875
                ],
                [
                    -81.99691009521484,
                    325.0808410644531
                ]
            ],
            "pieceId": "1"
        },
        {
            "coordinates": [
                [
                    890.0546875,
                    10374.6767578125
                ],
                [
                    1672.086669921875,
                    12150.6796875
                ],
                [
                    5814.0810546875,
                    7048.21533203125
                ]
            ],
            "pieceId": "10"
        },
        {
            "coordinates": [
                [
                    945.2552490234375,
                    10282.2275390625
                ],
                [
                    1746.2271728515625,
                    5051.85693359375
                ],
                [
                    1680.6048583984375,
                    2556.562255859375
                ]
            ],
            "pieceId": "11"
        },
        {
            "coordinates": [
                [
                    947.5440673828125,
                    10291.875
                ],
                [
                    5452.52197265625,
                    1657.0948486328125
                ],
                [
                    1749.021484375,
                    5061.58251953125
                ]
            ],
            "pieceId": "12"
        },
        {
            "coordinates": [
                [
                    937.8394775390625,
                    10291.064453125
                ],
                [
                    5848.31005859375,
                    2503.560791015625
                ],
                [
                    5459.05078125,
                    1664.77197265625
                ]
            ],
            "pieceId": "13"
        },
        {
            "coordinates": [
                [
                    948.1620483398438,
                    10291.6484375
                ],
                [
                    6710.9599609375,
                    3306.3125
                ],
                [
                    5858.32763671875,
                    2503.953857421875
                ]
            ],
            "pieceId": "14"
        },
        {
            "coordinates": [
                [
                    957.954345703125,
                    10294.3779296875
                ],
                [
                    7649.0322265625,
                    5368.05322265625
                ],
                [
                    6720.771484375,
                    3309.060791015625
                ]
            ],
            "pieceId": "15"
        },
        {
            "coordinates": [
                [
                    1680.92529296875,
                    12155.0517578125
                ],
                [
                    3128.217529296875,
                    12108.70703125
                ],
                [
                    5823.09716796875,
                    7052.728515625
                ]
            ],
            "pieceId": "16"
        },
        {
            "coordinates": [
                [
                    1681.2724609375,
                    12166.408203125
                ],
                [
                    5333.236328125,
                    12752.73828125
                ],
                [
                    3128.4501953125,
                    12116.6376953125
                ]
            ],
            "pieceId": "17"
        },
        {
            "coordinates": [
                [
                    1671.8253173828125,
                    2552.9365234375
                ],
                [
                    1736.356689453125,
                    5048.26123046875
                ],
                [
                    2796.937744140625,
                    2012.67236328125
                ]
            ],
            "pieceId": "18"
        },
        {
            "coordinates": [
                [
                    1725.715576171875,
                    5052.970703125
                ],
                [
                    2390.2529296875,
                    3709.316162109375
                ],
                [
                    2798.284423828125,
                    2021.5968017578125
                ]
            ],
            "pieceId": "19"
        },
        {
            "coordinates": [
                [
                    -219.52818298339844,
                    8881.904296875
                ],
                [
                    872.8179321289063,
                    10367.3125
                ],
                [
                    -8.472442626953125,
                    1897.0450439453125
                ]
            ],
            "pieceId": "2"
        },
        {
            "coordinates": [
                [
                    1731.7332763671875,
                    5060.0986328125
                ],
                [
                    6702.5087890625,
                    -10.572432518005371
                ],
                [
                    2396.3525390625,
                    3716.48388671875
                ]
            ],
            "pieceId": "20"
        },
        {
            "coordinates": [
                [
                    1741.2203369140625,
                    5055.23828125
                ],
                [
                    5458.25732421875,
                    1665.534912109375
                ],
                [
                    6710.119140625,
                    -17.271041870117188
                ]
            ],
            "pieceId": "21"
        },
        {
            "coordinates": [
                [
                    2386.0185546875,
                    3718.627685546875
                ],
                [
                    6692.87060546875,
                    -7.621764659881592
                ],
                [
                    2794.4716796875,
                    2031.011474609375
                ]
            ],
            "pieceId": "22"
        },
        {
            "coordinates": [
                [
                    3137.05615234375,
                    12113.185546875
                ],
                [
                    5342.53466796875,
                    12746.890625
                ],
                [
                    7689.4453125,
                    5370.5078125
                ],
                [
                    5814.45654296875,
                    7047.927734375
                ]
            ],
            "pieceId": "23"
        },
        {
            "coordinates": [
                [
                    5469.28955078125,
                    1663.8602294921875
                ],
                [
                    5858.12158203125,
                    2502.84765625
                ],
                [
                    6718.46533203125,
                    -20.942686080932617
                ]
            ],
            "pieceId": "24"
        },
        {
            "coordinates": [
                [
                    5862.0126953125,
                    2513.027099609375
                ],
                [
                    6714.86083984375,
                    3315.15673828125
                ],
                [
                    6720.29638671875,
                    -11.463164329528809
                ]
            ],
            "pieceId": "25"
        },
        {
            "coordinates": [
                [
                    6724.30029296875,
                    3318.420166015625
                ],
                [
                    7653.1787109375,
                    5377.13427734375
                ],
                [
                    6729.646484375,
                    -8.20159912109375
                ]
            ],
            "pieceId": "26"
        },
        {
            "coordinates": [
                [
                    -209.09117126464844,
                    8885.404296875
                ],
                [
                    1678.0394287109375,
                    12142.0625
                ],
                [
                    880.033447265625,
                    10373.17578125
                ]
            ],
            "pieceId": "3"
        },
        {
            "coordinates": [
                [
                    -72.23892211914063,
                    328.1631164550781
                ],
                [
                    -9.901046752929688,
                    1893.236083984375
                ],
                [
                    6689.8056640625,
                    3.051757574081421
                ]
            ],
            "pieceId": "4"
        },
        {
            "coordinates": [
                [
                    0.0,
                    1891.342041015625
                ],
                [
                    1662.177978515625,
                    2551.725341796875
                ],
                [
                    2791.92724609375,
                    2021.224853515625
                ],
                [
                    6699.38037109375,
                    0.0
                ]
            ],
            "pieceId": "5"
        },
        {
            "coordinates": [
                [
                    -0.8640288710594177,
                    1902.269287109375
                ],
                [
                    864.8204345703125,
                    10374.1484375
                ],
                [
                    1668.9814453125,
                    2543.012451171875
                ]
            ],
            "pieceId": "6"
        },
        {
            "coordinates": [
                [
                    866.5504150390625,
                    10383.8994140625
                ],
                [
                    956.1519165039063,
                    10280.3876953125
                ],
                [
                    1671.375244140625,
                    2552.83349609375
                ]
            ],
            "pieceId": "7"
        },
        {
            "coordinates": [
                [
                    876.3884887695313,
                    10388.3681640625
                ],
                [
                    7664.29296875,
                    5368.06103515625
                ],
                [
                    966.5965576171875,
                    10285.384765625
                ]
            ],
            "pieceId": "8"
        },
        {
            "coordinates": [
                [
                    889.596923828125,
                    10385.0439453125
                ],
                [
                    5804.181640625,
                    7044.64892578125
                ],
                [
                    7680.15625,
                    5368.32958984375
                ]
            ],
            "pieceId": "9"
        }
    ],
    "piecesFinalTransformation": [
        {
            "pieceId": "0",
            "rotationRadians": -12.581486701965332,
            "translateVectorX": -569.9539184570313,
            "translateVectorY": 2408.46435546875
        },
        {
            "pieceId": "1",
            "rotationRadians": -25.144596099853516,
            "translateVectorX": -334.3105163574219,
            "translateVectorY": 4701.38916015625
        },
        {
            "pieceId": "10",
            "rotationRadians": 31.413475036621094,
            "translateVectorX": 2792.073974609375,
            "translateVectorY": 9857.8583984375
        },
        {
            "pieceId": "11",
            "rotationRadians": -0.009098979644477367,
            "translateVectorX": 1457.363037109375,
            "translateVectorY": 5963.54833984375
        },
        {
            "pieceId": "12",
            "rotationRadians": -0.009002288803458214,
            "translateVectorX": 2716.36181640625,
            "translateVectorY": 5670.18310546875
        },
        {
            "pieceId": "13",
            "rotationRadians": -0.007121407892554998,
            "translateVectorX": 4081.7333984375,
            "translateVectorY": 4819.79736328125
        },
        {
            "pieceId": "14",
            "rotationRadians": -0.007160348352044821,
            "translateVectorX": 4505.8154296875,
            "translateVectorY": 5367.3056640625
        },
        {
            "pieceId": "15",
            "rotationRadians": -0.007157361600548029,
            "translateVectorX": 5109.2529296875,
            "translateVectorY": 6323.8310546875
        },
        {
            "pieceId": "16",
            "rotationRadians": 31.413509368896484,
            "translateVectorX": 3544.07861328125,
            "translateVectorY": 10438.8291015625
        },
        {
            "pieceId": "17",
            "rotationRadians": 31.411142349243164,
            "translateVectorX": 3380.987060546875,
            "translateVectorY": 12345.259765625
        },
        {
            "pieceId": "18",
            "rotationRadians": 6.274524211883545,
            "translateVectorX": 2068.37255859375,
            "translateVectorY": 3204.6240234375
        },
        {
            "pieceId": "19",
            "rotationRadians": -0.0047096069902181625,
            "translateVectorX": 2304.752197265625,
            "translateVectorY": 3594.629150390625
        },
        {
            "pieceId": "2",
            "rotationRadians": -25.146371841430664,
            "translateVectorX": 214.93910217285156,
            "translateVectorY": 7048.75537109375
        },
        {
            "pieceId": "20",
            "rotationRadians": -0.004647381603717804,
            "translateVectorX": 3610.19873046875,
            "translateVectorY": 2922.002685546875
        },
        {
            "pieceId": "21",
            "rotationRadians": -0.005017527379095554,
            "translateVectorX": 4636.53173828125,
            "translateVectorY": 2234.500732421875
        },
        {
            "pieceId": "22",
            "rotationRadians": -0.004460354335606098,
            "translateVectorX": 3957.786376953125,
            "translateVectorY": 1914.0052490234375
        },
        {
            "pieceId": "23",
            "rotationRadians": 31.41005516052246,
            "translateVectorX": 5424.27587890625,
            "translateVectorY": 9659.0576171875
        },
        {
            "pieceId": "24",
            "rotationRadians": 12.559757232666016,
            "translateVectorX": 6015.29296875,
            "translateVectorY": 1381.9217529296875
        },
        {
            "pieceId": "25",
            "rotationRadians": 12.558940887451172,
            "translateVectorX": 6432.39013671875,
            "translateVectorY": 1938.907470703125
        },
        {
            "pieceId": "26",
            "rotationRadians": 6.275728702545166,
            "translateVectorX": 7035.708984375,
            "translateVectorY": 2895.7841796875
        },
        {
            "pieceId": "3",
            "rotationRadians": -18.861019134521484,
            "translateVectorX": 782.9932861328125,
            "translateVectorY": 10466.8798828125
        },
        {
            "pieceId": "4",
            "rotationRadians": 0.00017287067021243274,
            "translateVectorX": 2202.556396484375,
            "translateVectorY": 741.483642578125
        },
        {
            "pieceId": "5",
            "rotationRadians": 0.0,
            "translateVectorX": 0.0,
            "translateVectorY": 0.0
        },
        {
            "pieceId": "6",
            "rotationRadians": -25.144529342651367,
            "translateVectorX": 844.3126220703125,
            "translateVectorY": 4939.8095703125
        },
        {
            "pieceId": "7",
            "rotationRadians": -18.86125946044922,
            "translateVectorX": 1164.69189453125,
            "translateVectorY": 7739.0400390625
        },
        {
            "pieceId": "8",
            "rotationRadians": 6.277372360229492,
            "translateVectorX": 3169.092041015625,
            "translateVectorY": 8680.6044921875
        },
        {
            "pieceId": "9",
            "rotationRadians": 31.410642623901367,
            "translateVectorX": 4791.31298828125,
            "translateVectorY": 7599.33984375
        }
    ]
}

        self.poc_response(ground_truth_polygons,response,0)


        # scaling down 
        scaled_ground_truth_polygons = []
        scale = 3 # recorded in the shift_data project

        for poly in ground_truth_polygons:
            xs,ys = poly.exterior.xy

            xs = [x*scale for x in xs]
            ys = [y*scale for y in ys]

            scaled_ground_truth_polygons.append(Polygon(list(zip(xs,ys))))

        self.poc_response(scaled_ground_truth_polygons,response,0)



class TestQpos(unittest.TestCase):

    def plot(self,polygons, ax = None,seed = 10):

        if ax is None:
            _,ax = plt.subplots()
        
        random.seed(seed)

        for poly in polygons:
            xs,ys = poly.exterior.xy
            ax.fill(xs,ys, alpha=0.5,fc=(random.random(),random.random(),random.random()),ec="black")

        ax.set_aspect("equal")

    def test_compiles(self):
        db = "0-30"
        puzzle_num = "19_DB1"
        puzzle_noise_level = 1
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        ground_truth_polygons = puzzle.get_ground_truth_puzzle()


        response = {
            "AfterEnableCollision": {
                "springs": [
                    {
                        "firstPieceId": "7",
                        "firstPieceVertex": 1,
                        "secondPieceId": "9",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 10.142101287841797
                    },
                    {
                        "firstPieceId": "7",
                        "firstPieceVertex": 2,
                        "secondPieceId": "9",
                        "secondPieceVertex": 3,
                        "snapshotedLength": 11.260101318359375
                    },
                    {
                        "firstPieceId": "7",
                        "firstPieceVertex": 0,
                        "secondPieceId": "8",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 20.635299682617188
                    },
                    {
                        "firstPieceId": "7",
                        "firstPieceVertex": 1,
                        "secondPieceId": "8",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 20.327173233032227
                    },
                    {
                        "firstPieceId": "8",
                        "firstPieceVertex": 1,
                        "secondPieceId": "9",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 15.948013305664063
                    },
                    {
                        "firstPieceId": "8",
                        "firstPieceVertex": 2,
                        "secondPieceId": "9",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 14.22866153717041
                    },
                    {
                        "firstPieceId": "6",
                        "firstPieceVertex": 1,
                        "secondPieceId": "9",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 13.986743927001953
                    },
                    {
                        "firstPieceId": "6",
                        "firstPieceVertex": 2,
                        "secondPieceId": "9",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 15.092012405395508
                    },
                    {
                        "firstPieceId": "0",
                        "firstPieceVertex": 2,
                        "secondPieceId": "8",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 7.531733989715576
                    },
                    {
                        "firstPieceId": "0",
                        "firstPieceVertex": 3,
                        "secondPieceId": "8",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 12.917973518371582
                    },
                    {
                        "firstPieceId": "5",
                        "firstPieceVertex": 2,
                        "secondPieceId": "6",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 15.013673782348633
                    },
                    {
                        "firstPieceId": "5",
                        "firstPieceVertex": 3,
                        "secondPieceId": "6",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 14.896913528442383
                    },
                    {
                        "firstPieceId": "4",
                        "firstPieceVertex": 1,
                        "secondPieceId": "6",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 9.381514549255371
                    },
                    {
                        "firstPieceId": "4",
                        "firstPieceVertex": 2,
                        "secondPieceId": "6",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 11.278538703918457
                    },
                    {
                        "firstPieceId": "5",
                        "firstPieceVertex": 3,
                        "secondPieceId": "0",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 17.220252990722656
                    },
                    {
                        "firstPieceId": "5",
                        "firstPieceVertex": 0,
                        "secondPieceId": "0",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 17.102039337158203
                    },
                    {
                        "firstPieceId": "0",
                        "firstPieceVertex": 0,
                        "secondPieceId": "1",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 11.324124336242676
                    },
                    {
                        "firstPieceId": "0",
                        "firstPieceVertex": 1,
                        "secondPieceId": "1",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 11.957756996154785
                    },
                    {
                        "firstPieceId": "3",
                        "firstPieceVertex": 1,
                        "secondPieceId": "5",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 11.744946479797363
                    },
                    {
                        "firstPieceId": "3",
                        "firstPieceVertex": 2,
                        "secondPieceId": "5",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 10.237936973571777
                    },
                    {
                        "firstPieceId": "2",
                        "firstPieceVertex": 1,
                        "secondPieceId": "5",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 21.767284393310547
                    },
                    {
                        "firstPieceId": "2",
                        "firstPieceVertex": 2,
                        "secondPieceId": "5",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 21.589750289916992
                    },
                    {
                        "firstPieceId": "3",
                        "firstPieceVertex": 0,
                        "secondPieceId": "4",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 10.96021556854248
                    },
                    {
                        "firstPieceId": "3",
                        "firstPieceVertex": 1,
                        "secondPieceId": "4",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 8.148117065429688
                    },
                    {
                        "firstPieceId": "3",
                        "firstPieceVertex": 2,
                        "secondPieceId": "2",
                        "secondPieceVertex": 1,
                        "snapshotedLength": 19.059406280517578
                    },
                    {
                        "firstPieceId": "3",
                        "firstPieceVertex": 0,
                        "secondPieceId": "2",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 14.149581909179688
                    },
                    {
                        "firstPieceId": "1",
                        "firstPieceVertex": 1,
                        "secondPieceId": "2",
                        "secondPieceVertex": 0,
                        "snapshotedLength": 12.62522029876709
                    },
                    {
                        "firstPieceId": "1",
                        "firstPieceVertex": 2,
                        "secondPieceId": "2",
                        "secondPieceVertex": 2,
                        "snapshotedLength": 18.883333206176758
                    }
                ],
                "sumSpringsLength": 386.0
            },
            "piecesBeforeEnableCollision": [
                {
                    "coordinates": [
                        [
                            1930.1241455078125,
                            478.7597351074219
                        ],
                        [
                            1529.546630859375,
                            245.06185913085938
                        ],
                        [
                            -16.576766967773438,
                            682.7735595703125
                        ],
                        [
                            678.8386840820313,
                            1548.4256591796875
                        ]
                    ],
                    "pieceId": "0"
                },
                {
                    "coordinates": [
                        [
                            1936.2601318359375,
                            488.2793273925781
                        ],
                        [
                            1865.0911865234375,
                            -451.6658630371094
                        ],
                        [
                            1521.1409912109375,
                            236.55889892578125
                        ]
                    ],
                    "pieceId": "1"
                },
                {
                    "coordinates": [
                        [
                            1872.827392578125,
                            -441.6885070800781
                        ],
                        [
                            1479.560791015625,
                            126.71660614013672
                        ],
                        [
                            1503.2862548828125,
                            230.41151428222656
                        ]
                    ],
                    "pieceId": "2"
                },
                {
                    "coordinates": [
                        [
                            1885.993896484375,
                            -436.5062561035156
                        ],
                        [
                            739.084228515625,
                            11.081694602966309
                        ],
                        [
                            1469.1905517578125,
                            110.7234878540039
                        ]
                    ],
                    "pieceId": "3"
                },
                {
                    "coordinates": [
                        [
                            1875.2860107421875,
                            -438.84466552734375
                        ],
                        [
                            -260.4713439941406,
                            -4.7607421875
                        ],
                        [
                            740.8103637695313,
                            3.1185147762298584
                        ]
                    ],
                    "pieceId": "4"
                },
                {
                    "coordinates": [
                        [
                            1513.0748291015625,
                            249.65475463867188
                        ],
                        [
                            1460.519775390625,
                            116.1689682006836
                        ],
                        [
                            742.9752197265625,
                            0.0
                        ],
                        [
                            0.0,
                            678.110107421875
                        ]
                    ],
                    "pieceId": "5"
                },
                {
                    "coordinates": [
                        [
                            732.6068725585938,
                            10.858534812927246
                        ],
                        [
                            -264.0743103027344,
                            -13.422011375427246
                        ],
                        [
                            5.653380870819092,
                            664.3275756835938
                        ]
                    ],
                    "pieceId": "6"
                },
                {
                    "coordinates": [
                        [
                            670.642822265625,
                            1545.0858154296875
                        ],
                        [
                            7.158278942108154,
                            936.2391967773438
                        ],
                        [
                            -379.63482666015625,
                            1472.7401123046875
                        ]
                    ],
                    "pieceId": "7"
                },
                {
                    "coordinates": [
                        [
                            685.2988891601563,
                            1559.6121826171875
                        ],
                        [
                            -12.493132591247559,
                            689.1021118164063
                        ],
                        [
                            -4.0378570556640625,
                            919.2733154296875
                        ]
                    ],
                    "pieceId": "8"
                },
                {
                    "coordinates": [
                        [
                            -2.586364507675171,
                            933.4277954101563
                        ],
                        [
                            -4.985809326171875,
                            675.0316162109375
                        ],
                        [
                            -262.9203796386719,
                            -27.36091423034668
                        ],
                        [
                            -370.9144287109375,
                            1479.865966796875
                        ]
                    ],
                    "pieceId": "9"
                }
            ],
            "piecesFinalCoords": [
                {
                    "coordinates": [
                        [
                            1930.1241455078125,
                            478.7597351074219
                        ],
                        [
                            1529.546630859375,
                            245.06185913085938
                        ],
                        [
                            -16.576766967773438,
                            682.7735595703125
                        ],
                        [
                            678.8386840820313,
                            1548.4256591796875
                        ]
                    ],
                    "pieceId": "0"
                },
                {
                    "coordinates": [
                        [
                            1936.2601318359375,
                            488.2793273925781
                        ],
                        [
                            1865.0911865234375,
                            -451.6658630371094
                        ],
                        [
                            1521.1409912109375,
                            236.55889892578125
                        ]
                    ],
                    "pieceId": "1"
                },
                {
                    "coordinates": [
                        [
                            1872.827392578125,
                            -441.6885070800781
                        ],
                        [
                            1479.560791015625,
                            126.71660614013672
                        ],
                        [
                            1503.2862548828125,
                            230.41151428222656
                        ]
                    ],
                    "pieceId": "2"
                },
                {
                    "coordinates": [
                        [
                            1885.993896484375,
                            -436.5062561035156
                        ],
                        [
                            739.084228515625,
                            11.081694602966309
                        ],
                        [
                            1469.1905517578125,
                            110.7234878540039
                        ]
                    ],
                    "pieceId": "3"
                },
                {
                    "coordinates": [
                        [
                            1875.2860107421875,
                            -438.84466552734375
                        ],
                        [
                            -260.4713439941406,
                            -4.7607421875
                        ],
                        [
                            740.8103637695313,
                            3.1185147762298584
                        ]
                    ],
                    "pieceId": "4"
                },
                {
                    "coordinates": [
                        [
                            1513.0748291015625,
                            249.65475463867188
                        ],
                        [
                            1460.519775390625,
                            116.1689682006836
                        ],
                        [
                            742.9752197265625,
                            0.0
                        ],
                        [
                            0.0,
                            678.110107421875
                        ]
                    ],
                    "pieceId": "5"
                },
                {
                    "coordinates": [
                        [
                            732.6068725585938,
                            10.858534812927246
                        ],
                        [
                            -264.0743103027344,
                            -13.422011375427246
                        ],
                        [
                            5.653380870819092,
                            664.3275756835938
                        ]
                    ],
                    "pieceId": "6"
                },
                {
                    "coordinates": [
                        [
                            670.642822265625,
                            1545.0858154296875
                        ],
                        [
                            7.158278942108154,
                            936.2391967773438
                        ],
                        [
                            -379.63482666015625,
                            1472.7401123046875
                        ]
                    ],
                    "pieceId": "7"
                },
                {
                    "coordinates": [
                        [
                            685.2988891601563,
                            1559.6121826171875
                        ],
                        [
                            -12.493132591247559,
                            689.1021118164063
                        ],
                        [
                            -4.0378570556640625,
                            919.2733154296875
                        ]
                    ],
                    "pieceId": "8"
                },
                {
                    "coordinates": [
                        [
                            -2.586364507675171,
                            933.4277954101563
                        ],
                        [
                            -4.985809326171875,
                            675.0316162109375
                        ],
                        [
                            -262.9203796386719,
                            -27.36091423034668
                        ],
                        [
                            -370.9144287109375,
                            1479.865966796875
                        ]
                    ],
                    "pieceId": "9"
                }
            ],
            "piecesFinalTransformation": [
                {
                    "pieceId": "0",
                    "rotationRadians": -2.657514810562134,
                    "translateVectorX": 928.5106201171875,
                    "translateVectorY": 804.6798095703125
                },
                {
                    "pieceId": "1",
                    "rotationRadians": -18.95050621032715,
                    "translateVectorX": 1774.1640625,
                    "translateVectorY": 91.05681610107422
                },
                {
                    "pieceId": "2",
                    "rotationRadians": -0.8310062289237976,
                    "translateVectorX": 1618.556884765625,
                    "translateVectorY": -28.186796188354492
                },
                {
                    "pieceId": "3",
                    "rotationRadians": 3.585374593734741,
                    "translateVectorX": 1364.755615234375,
                    "translateVectorY": -104.90035247802734
                },
                {
                    "pieceId": "4",
                    "rotationRadians": -9.907032012939453,
                    "translateVectorX": 785.2077026367188,
                    "translateVectorY": -146.82960510253906
                },
                {
                    "pieceId": "5",
                    "rotationRadians": 0.0,
                    "translateVectorX": 0.0,
                    "translateVectorY": 0.0
                },
                {
                    "pieceId": "6",
                    "rotationRadians": -2.453127861022949,
                    "translateVectorX": 158.06198120117188,
                    "translateVectorY": 220.5886688232422
                },
                {
                    "pieceId": "7",
                    "rotationRadians": 1.8316062688827515,
                    "translateVectorX": 99.38811492919922,
                    "translateVectorY": 1318.021728515625
                },
                {
                    "pieceId": "8",
                    "rotationRadians": 6.320694923400879,
                    "translateVectorX": 222.9232635498047,
                    "translateVectorY": 1055.995849609375
                },
                {
                    "pieceId": "9",
                    "rotationRadians": -43.570457458496094,
                    "translateVectorX": -198.01901245117188,
                    "translateVectorY": 764.249755859375
                }
            ]
        }

        
        solution_polygons = [Polygon(piece_json["coordinates"]) for piece_json in response["piecesFinalCoords"]]
        evaluator = Qpos(ground_truth_polygons)
        overlapping_score = evaluator.evaluate(solution_polygons)

        assert abs(overlapping_score-1) < 1e-3
        

    def test_19DBPAST2staged(self):
        db = "0-30"
        puzzle_num = "19DBPAST2staged"
        puzzle_noise_level = 0 
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        ground_truth_polygons = puzzle.get_ground_truth_puzzle()
        ground_truth_polygons = ground_truth_polygons#[:num_pieces_observed]

        response = {
        
        
    "AfterEnableCollision": {
        "springs": [
            {
                "firstPieceId": "0",
                "firstPieceVertex": 0,
                "secondPieceId": "1",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.917414665222168
            },
            {
                "firstPieceId": "0",
                "firstPieceVertex": 1,
                "secondPieceId": "1",
                "secondPieceVertex": 3,
                "snapshotedLength": 10.219512939453125
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 2,
                "secondPieceId": "4",
                "secondPieceVertex": 1,
                "snapshotedLength": 9.87955379486084
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 3,
                "secondPieceId": "4",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.234469413757324
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 1,
                "secondPieceId": "2",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.434589385986328
            },
            {
                "firstPieceId": "1",
                "firstPieceVertex": 2,
                "secondPieceId": "2",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.87761116027832
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 1,
                "secondPieceId": "6",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.522393226623535
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 2,
                "secondPieceId": "6",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.229329109191895
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 0,
                "secondPieceId": "3",
                "secondPieceVertex": 0,
                "snapshotedLength": 11.008228302001953
            },
            {
                "firstPieceId": "2",
                "firstPieceVertex": 1,
                "secondPieceId": "3",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.297056198120117
            },
            {
                "firstPieceId": "3",
                "firstPieceVertex": 1,
                "secondPieceId": "10",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.47563362121582
            },
            {
                "firstPieceId": "3",
                "firstPieceVertex": 2,
                "secondPieceId": "10",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.133009910583496
            },
            {
                "firstPieceId": "4",
                "firstPieceVertex": 1,
                "secondPieceId": "5",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.080572128295898
            },
            {
                "firstPieceId": "4",
                "firstPieceVertex": 2,
                "secondPieceId": "5",
                "secondPieceVertex": 3,
                "snapshotedLength": 10.049464225769043
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 2,
                "secondPieceId": "22",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.111474990844727
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 3,
                "secondPieceId": "22",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.023399353027344
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 1,
                "secondPieceId": "18",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.723337173461914
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 2,
                "secondPieceId": "18",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.91222858428955
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 0,
                "secondPieceId": "6",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.961305618286133
            },
            {
                "firstPieceId": "5",
                "firstPieceVertex": 1,
                "secondPieceId": "6",
                "secondPieceVertex": 2,
                "snapshotedLength": 11.05591869354248
            },
            {
                "firstPieceId": "6",
                "firstPieceVertex": 1,
                "secondPieceId": "7",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.9026460647583
            },
            {
                "firstPieceId": "6",
                "firstPieceVertex": 2,
                "secondPieceId": "7",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.11030101776123
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 1,
                "secondPieceId": "11",
                "secondPieceVertex": 0,
                "snapshotedLength": 11.050721168518066
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 2,
                "secondPieceId": "11",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.954449653625488
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 0,
                "secondPieceId": "8",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.805530548095703
            },
            {
                "firstPieceId": "7",
                "firstPieceVertex": 1,
                "secondPieceId": "8",
                "secondPieceVertex": 2,
                "snapshotedLength": 11.578559875488281
            },
            {
                "firstPieceId": "8",
                "firstPieceVertex": 1,
                "secondPieceId": "15",
                "secondPieceVertex": 1,
                "snapshotedLength": 15.260697364807129
            },
            {
                "firstPieceId": "8",
                "firstPieceVertex": 2,
                "secondPieceId": "15",
                "secondPieceVertex": 0,
                "snapshotedLength": 12.472540855407715
            },
            {
                "firstPieceId": "8",
                "firstPieceVertex": 0,
                "secondPieceId": "9",
                "secondPieceVertex": 0,
                "snapshotedLength": 13.62034797668457
            },
            {
                "firstPieceId": "8",
                "firstPieceVertex": 1,
                "secondPieceId": "9",
                "secondPieceVertex": 2,
                "snapshotedLength": 15.865697860717773
            },
            {
                "firstPieceId": "9",
                "firstPieceVertex": 1,
                "secondPieceId": "23",
                "secondPieceVertex": 3,
                "snapshotedLength": 10.785911560058594
            },
            {
                "firstPieceId": "9",
                "firstPieceVertex": 2,
                "secondPieceId": "23",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.540759086608887
            },
            {
                "firstPieceId": "9",
                "firstPieceVertex": 0,
                "secondPieceId": "10",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.374635696411133
            },
            {
                "firstPieceId": "9",
                "firstPieceVertex": 1,
                "secondPieceId": "10",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.522747039794922
            },
            {
                "firstPieceId": "10",
                "firstPieceVertex": 1,
                "secondPieceId": "16",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.860681533813477
            },
            {
                "firstPieceId": "10",
                "firstPieceVertex": 2,
                "secondPieceId": "16",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.082367897033691
            },
            {
                "firstPieceId": "11",
                "firstPieceVertex": 1,
                "secondPieceId": "18",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.508530616760254
            },
            {
                "firstPieceId": "11",
                "firstPieceVertex": 2,
                "secondPieceId": "18",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.498061180114746
            },
            {
                "firstPieceId": "11",
                "firstPieceVertex": 0,
                "secondPieceId": "12",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.915160179138184
            },
            {
                "firstPieceId": "11",
                "firstPieceVertex": 1,
                "secondPieceId": "12",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.116662979125977
            },
            {
                "firstPieceId": "12",
                "firstPieceVertex": 1,
                "secondPieceId": "21",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.204345703125
            },
            {
                "firstPieceId": "12",
                "firstPieceVertex": 2,
                "secondPieceId": "21",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.053685188293457
            },
            {
                "firstPieceId": "12",
                "firstPieceVertex": 0,
                "secondPieceId": "13",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.738227844238281
            },
            {
                "firstPieceId": "12",
                "firstPieceVertex": 1,
                "secondPieceId": "13",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.077652931213379
            },
            {
                "firstPieceId": "13",
                "firstPieceVertex": 1,
                "secondPieceId": "24",
                "secondPieceVertex": 1,
                "snapshotedLength": 9.837160110473633
            },
            {
                "firstPieceId": "13",
                "firstPieceVertex": 2,
                "secondPieceId": "24",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.277090072631836
            },
            {
                "firstPieceId": "13",
                "firstPieceVertex": 0,
                "secondPieceId": "14",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.339057922363281
            },
            {
                "firstPieceId": "13",
                "firstPieceVertex": 1,
                "secondPieceId": "14",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.025172233581543
            },
            {
                "firstPieceId": "14",
                "firstPieceVertex": 1,
                "secondPieceId": "25",
                "secondPieceVertex": 1,
                "snapshotedLength": 9.665310859680176
            },
            {
                "firstPieceId": "14",
                "firstPieceVertex": 2,
                "secondPieceId": "25",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.793017387390137
            },
            {
                "firstPieceId": "14",
                "firstPieceVertex": 0,
                "secondPieceId": "15",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.165597915649414
            },
            {
                "firstPieceId": "14",
                "firstPieceVertex": 1,
                "secondPieceId": "15",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.1922607421875
            },
            {
                "firstPieceId": "15",
                "firstPieceVertex": 1,
                "secondPieceId": "26",
                "secondPieceVertex": 1,
                "snapshotedLength": 9.982022285461426
            },
            {
                "firstPieceId": "15",
                "firstPieceVertex": 2,
                "secondPieceId": "26",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.001755714416504
            },
            {
                "firstPieceId": "16",
                "firstPieceVertex": 1,
                "secondPieceId": "23",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.910200119018555
            },
            {
                "firstPieceId": "16",
                "firstPieceVertex": 2,
                "secondPieceId": "23",
                "secondPieceVertex": 3,
                "snapshotedLength": 9.884443283081055
            },
            {
                "firstPieceId": "16",
                "firstPieceVertex": 0,
                "secondPieceId": "17",
                "secondPieceVertex": 0,
                "snapshotedLength": 11.357844352722168
            },
            {
                "firstPieceId": "16",
                "firstPieceVertex": 1,
                "secondPieceId": "17",
                "secondPieceVertex": 2,
                "snapshotedLength": 7.934224605560303
            },
            {
                "firstPieceId": "17",
                "firstPieceVertex": 1,
                "secondPieceId": "23",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.984820365905762
            },
            {
                "firstPieceId": "17",
                "firstPieceVertex": 2,
                "secondPieceId": "23",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.272586822509766
            },
            {
                "firstPieceId": "18",
                "firstPieceVertex": 1,
                "secondPieceId": "19",
                "secondPieceVertex": 0,
                "snapshotedLength": 11.634832382202148
            },
            {
                "firstPieceId": "18",
                "firstPieceVertex": 2,
                "secondPieceId": "19",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.025787353515625
            },
            {
                "firstPieceId": "19",
                "firstPieceVertex": 1,
                "secondPieceId": "22",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.230944633483887
            },
            {
                "firstPieceId": "19",
                "firstPieceVertex": 2,
                "secondPieceId": "22",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.15886402130127
            },
            {
                "firstPieceId": "19",
                "firstPieceVertex": 0,
                "secondPieceId": "20",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.328317642211914
            },
            {
                "firstPieceId": "19",
                "firstPieceVertex": 1,
                "secondPieceId": "20",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.41045093536377
            },
            {
                "firstPieceId": "20",
                "firstPieceVertex": 1,
                "secondPieceId": "22",
                "secondPieceVertex": 1,
                "snapshotedLength": 10.079397201538086
            },
            {
                "firstPieceId": "20",
                "firstPieceVertex": 2,
                "secondPieceId": "22",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.554826736450195
            },
            {
                "firstPieceId": "20",
                "firstPieceVertex": 0,
                "secondPieceId": "21",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.65949821472168
            },
            {
                "firstPieceId": "20",
                "firstPieceVertex": 1,
                "secondPieceId": "21",
                "secondPieceVertex": 2,
                "snapshotedLength": 10.138458251953125
            },
            {
                "firstPieceId": "21",
                "firstPieceVertex": 1,
                "secondPieceId": "24",
                "secondPieceVertex": 0,
                "snapshotedLength": 11.15848445892334
            },
            {
                "firstPieceId": "21",
                "firstPieceVertex": 2,
                "secondPieceId": "24",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.11844253540039
            },
            {
                "firstPieceId": "24",
                "firstPieceVertex": 1,
                "secondPieceId": "25",
                "secondPieceVertex": 0,
                "snapshotedLength": 10.897817611694336
            },
            {
                "firstPieceId": "24",
                "firstPieceVertex": 2,
                "secondPieceId": "25",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.654745101928711
            },
            {
                "firstPieceId": "25",
                "firstPieceVertex": 1,
                "secondPieceId": "26",
                "secondPieceVertex": 0,
                "snapshotedLength": 9.987682342529297
            },
            {
                "firstPieceId": "25",
                "firstPieceVertex": 2,
                "secondPieceId": "26",
                "secondPieceVertex": 2,
                "snapshotedLength": 9.904173851013184
            }
        ],
        "sumSpringsLength": 751.0
    },
    "piecesBeforeEnableCollision": [
        {
            "coordinates": [
                [
                    -804.8419799804688,
                    5412.80517578125
                ],
                [
                    -91.2513656616211,
                    329.4200744628906
                ],
                [
                    -813.7645263671875,
                    1483.17138671875
                ]
            ],
            "pieceId": "0"
        },
        {
            "coordinates": [
                [
                    -812.1604614257813,
                    5406.1123046875
                ],
                [
                    -224.3003692626953,
                    8873.763671875
                ],
                [
                    -0.8411406874656677,
                    1889.289794921875
                ],
                [
                    -81.99691009521484,
                    325.0808410644531
                ]
            ],
            "pieceId": "1"
        },
        {
            "coordinates": [
                [
                    890.0546875,
                    10374.6767578125
                ],
                [
                    1672.086669921875,
                    12150.6796875
                ],
                [
                    5814.0810546875,
                    7048.21533203125
                ]
            ],
            "pieceId": "10"
        },
        {
            "coordinates": [
                [
                    945.2552490234375,
                    10282.2275390625
                ],
                [
                    1746.2271728515625,
                    5051.85693359375
                ],
                [
                    1680.6048583984375,
                    2556.562255859375
                ]
            ],
            "pieceId": "11"
        },
        {
            "coordinates": [
                [
                    947.5440673828125,
                    10291.875
                ],
                [
                    5452.52197265625,
                    1657.0948486328125
                ],
                [
                    1749.021484375,
                    5061.58251953125
                ]
            ],
            "pieceId": "12"
        },
        {
            "coordinates": [
                [
                    937.8394775390625,
                    10291.064453125
                ],
                [
                    5848.31005859375,
                    2503.560791015625
                ],
                [
                    5459.05078125,
                    1664.77197265625
                ]
            ],
            "pieceId": "13"
        },
        {
            "coordinates": [
                [
                    948.1620483398438,
                    10291.6484375
                ],
                [
                    6710.9599609375,
                    3306.3125
                ],
                [
                    5858.32763671875,
                    2503.953857421875
                ]
            ],
            "pieceId": "14"
        },
        {
            "coordinates": [
                [
                    957.954345703125,
                    10294.3779296875
                ],
                [
                    7649.0322265625,
                    5368.05322265625
                ],
                [
                    6720.771484375,
                    3309.060791015625
                ]
            ],
            "pieceId": "15"
        },
        {
            "coordinates": [
                [
                    1680.92529296875,
                    12155.0517578125
                ],
                [
                    3128.217529296875,
                    12108.70703125
                ],
                [
                    5823.09716796875,
                    7052.728515625
                ]
            ],
            "pieceId": "16"
        },
        {
            "coordinates": [
                [
                    1681.2724609375,
                    12166.408203125
                ],
                [
                    5333.236328125,
                    12752.73828125
                ],
                [
                    3128.4501953125,
                    12116.6376953125
                ]
            ],
            "pieceId": "17"
        },
        {
            "coordinates": [
                [
                    1671.8253173828125,
                    2552.9365234375
                ],
                [
                    1736.356689453125,
                    5048.26123046875
                ],
                [
                    2796.937744140625,
                    2012.67236328125
                ]
            ],
            "pieceId": "18"
        },
        {
            "coordinates": [
                [
                    1725.715576171875,
                    5052.970703125
                ],
                [
                    2390.2529296875,
                    3709.316162109375
                ],
                [
                    2798.284423828125,
                    2021.5968017578125
                ]
            ],
            "pieceId": "19"
        },
        {
            "coordinates": [
                [
                    -219.52818298339844,
                    8881.904296875
                ],
                [
                    872.8179321289063,
                    10367.3125
                ],
                [
                    -8.472442626953125,
                    1897.0450439453125
                ]
            ],
            "pieceId": "2"
        },
        {
            "coordinates": [
                [
                    1731.7332763671875,
                    5060.0986328125
                ],
                [
                    6702.5087890625,
                    -10.572432518005371
                ],
                [
                    2396.3525390625,
                    3716.48388671875
                ]
            ],
            "pieceId": "20"
        },
        {
            "coordinates": [
                [
                    1741.2203369140625,
                    5055.23828125
                ],
                [
                    5458.25732421875,
                    1665.534912109375
                ],
                [
                    6710.119140625,
                    -17.271041870117188
                ]
            ],
            "pieceId": "21"
        },
        {
            "coordinates": [
                [
                    2386.0185546875,
                    3718.627685546875
                ],
                [
                    6692.87060546875,
                    -7.621764659881592
                ],
                [
                    2794.4716796875,
                    2031.011474609375
                ]
            ],
            "pieceId": "22"
        },
        {
            "coordinates": [
                [
                    3137.05615234375,
                    12113.185546875
                ],
                [
                    5342.53466796875,
                    12746.890625
                ],
                [
                    7689.4453125,
                    5370.5078125
                ],
                [
                    5814.45654296875,
                    7047.927734375
                ]
            ],
            "pieceId": "23"
        },
        {
            "coordinates": [
                [
                    5469.28955078125,
                    1663.8602294921875
                ],
                [
                    5858.12158203125,
                    2502.84765625
                ],
                [
                    6718.46533203125,
                    -20.942686080932617
                ]
            ],
            "pieceId": "24"
        },
        {
            "coordinates": [
                [
                    5862.0126953125,
                    2513.027099609375
                ],
                [
                    6714.86083984375,
                    3315.15673828125
                ],
                [
                    6720.29638671875,
                    -11.463164329528809
                ]
            ],
            "pieceId": "25"
        },
        {
            "coordinates": [
                [
                    6724.30029296875,
                    3318.420166015625
                ],
                [
                    7653.1787109375,
                    5377.13427734375
                ],
                [
                    6729.646484375,
                    -8.20159912109375
                ]
            ],
            "pieceId": "26"
        },
        {
            "coordinates": [
                [
                    -209.09117126464844,
                    8885.404296875
                ],
                [
                    1678.0394287109375,
                    12142.0625
                ],
                [
                    880.033447265625,
                    10373.17578125
                ]
            ],
            "pieceId": "3"
        },
        {
            "coordinates": [
                [
                    -72.23892211914063,
                    328.1631164550781
                ],
                [
                    -9.901046752929688,
                    1893.236083984375
                ],
                [
                    6689.8056640625,
                    3.051757574081421
                ]
            ],
            "pieceId": "4"
        },
        {
            "coordinates": [
                [
                    0.0,
                    1891.342041015625
                ],
                [
                    1662.177978515625,
                    2551.725341796875
                ],
                [
                    2791.92724609375,
                    2021.224853515625
                ],
                [
                    6699.38037109375,
                    0.0
                ]
            ],
            "pieceId": "5"
        },
        {
            "coordinates": [
                [
                    -0.8640288710594177,
                    1902.269287109375
                ],
                [
                    864.8204345703125,
                    10374.1484375
                ],
                [
                    1668.9814453125,
                    2543.012451171875
                ]
            ],
            "pieceId": "6"
        },
        {
            "coordinates": [
                [
                    866.5504150390625,
                    10383.8994140625
                ],
                [
                    956.1519165039063,
                    10280.3876953125
                ],
                [
                    1671.375244140625,
                    2552.83349609375
                ]
            ],
            "pieceId": "7"
        },
        {
            "coordinates": [
                [
                    876.3884887695313,
                    10388.3681640625
                ],
                [
                    7664.29296875,
                    5368.06103515625
                ],
                [
                    966.5965576171875,
                    10285.384765625
                ]
            ],
            "pieceId": "8"
        },
        {
            "coordinates": [
                [
                    889.596923828125,
                    10385.0439453125
                ],
                [
                    5804.181640625,
                    7044.64892578125
                ],
                [
                    7680.15625,
                    5368.32958984375
                ]
            ],
            "pieceId": "9"
        }
    ],
    "piecesFinalCoords": [
        {
            "coordinates": [
                [
                    -804.8419799804688,
                    5412.80517578125
                ],
                [
                    -91.2513656616211,
                    329.4200744628906
                ],
                [
                    -813.7645263671875,
                    1483.17138671875
                ]
            ],
            "pieceId": "0"
        },
        {
            "coordinates": [
                [
                    -812.1604614257813,
                    5406.1123046875
                ],
                [
                    -224.3003692626953,
                    8873.763671875
                ],
                [
                    -0.8411406874656677,
                    1889.289794921875
                ],
                [
                    -81.99691009521484,
                    325.0808410644531
                ]
            ],
            "pieceId": "1"
        },
        {
            "coordinates": [
                [
                    890.0546875,
                    10374.6767578125
                ],
                [
                    1672.086669921875,
                    12150.6796875
                ],
                [
                    5814.0810546875,
                    7048.21533203125
                ]
            ],
            "pieceId": "10"
        },
        {
            "coordinates": [
                [
                    945.2552490234375,
                    10282.2275390625
                ],
                [
                    1746.2271728515625,
                    5051.85693359375
                ],
                [
                    1680.6048583984375,
                    2556.562255859375
                ]
            ],
            "pieceId": "11"
        },
        {
            "coordinates": [
                [
                    947.5440673828125,
                    10291.875
                ],
                [
                    5452.52197265625,
                    1657.0948486328125
                ],
                [
                    1749.021484375,
                    5061.58251953125
                ]
            ],
            "pieceId": "12"
        },
        {
            "coordinates": [
                [
                    937.8394775390625,
                    10291.064453125
                ],
                [
                    5848.31005859375,
                    2503.560791015625
                ],
                [
                    5459.05078125,
                    1664.77197265625
                ]
            ],
            "pieceId": "13"
        },
        {
            "coordinates": [
                [
                    948.1620483398438,
                    10291.6484375
                ],
                [
                    6710.9599609375,
                    3306.3125
                ],
                [
                    5858.32763671875,
                    2503.953857421875
                ]
            ],
            "pieceId": "14"
        },
        {
            "coordinates": [
                [
                    957.954345703125,
                    10294.3779296875
                ],
                [
                    7649.0322265625,
                    5368.05322265625
                ],
                [
                    6720.771484375,
                    3309.060791015625
                ]
            ],
            "pieceId": "15"
        },
        {
            "coordinates": [
                [
                    1680.92529296875,
                    12155.0517578125
                ],
                [
                    3128.217529296875,
                    12108.70703125
                ],
                [
                    5823.09716796875,
                    7052.728515625
                ]
            ],
            "pieceId": "16"
        },
        {
            "coordinates": [
                [
                    1681.2724609375,
                    12166.408203125
                ],
                [
                    5333.236328125,
                    12752.73828125
                ],
                [
                    3128.4501953125,
                    12116.6376953125
                ]
            ],
            "pieceId": "17"
        },
        {
            "coordinates": [
                [
                    1671.8253173828125,
                    2552.9365234375
                ],
                [
                    1736.356689453125,
                    5048.26123046875
                ],
                [
                    2796.937744140625,
                    2012.67236328125
                ]
            ],
            "pieceId": "18"
        },
        {
            "coordinates": [
                [
                    1725.715576171875,
                    5052.970703125
                ],
                [
                    2390.2529296875,
                    3709.316162109375
                ],
                [
                    2798.284423828125,
                    2021.5968017578125
                ]
            ],
            "pieceId": "19"
        },
        {
            "coordinates": [
                [
                    -219.52818298339844,
                    8881.904296875
                ],
                [
                    872.8179321289063,
                    10367.3125
                ],
                [
                    -8.472442626953125,
                    1897.0450439453125
                ]
            ],
            "pieceId": "2"
        },
        {
            "coordinates": [
                [
                    1731.7332763671875,
                    5060.0986328125
                ],
                [
                    6702.5087890625,
                    -10.572432518005371
                ],
                [
                    2396.3525390625,
                    3716.48388671875
                ]
            ],
            "pieceId": "20"
        },
        {
            "coordinates": [
                [
                    1741.2203369140625,
                    5055.23828125
                ],
                [
                    5458.25732421875,
                    1665.534912109375
                ],
                [
                    6710.119140625,
                    -17.271041870117188
                ]
            ],
            "pieceId": "21"
        },
        {
            "coordinates": [
                [
                    2386.0185546875,
                    3718.627685546875
                ],
                [
                    6692.87060546875,
                    -7.621764659881592
                ],
                [
                    2794.4716796875,
                    2031.011474609375
                ]
            ],
            "pieceId": "22"
        },
        {
            "coordinates": [
                [
                    3137.05615234375,
                    12113.185546875
                ],
                [
                    5342.53466796875,
                    12746.890625
                ],
                [
                    7689.4453125,
                    5370.5078125
                ],
                [
                    5814.45654296875,
                    7047.927734375
                ]
            ],
            "pieceId": "23"
        },
        {
            "coordinates": [
                [
                    5469.28955078125,
                    1663.8602294921875
                ],
                [
                    5858.12158203125,
                    2502.84765625
                ],
                [
                    6718.46533203125,
                    -20.942686080932617
                ]
            ],
            "pieceId": "24"
        },
        {
            "coordinates": [
                [
                    5862.0126953125,
                    2513.027099609375
                ],
                [
                    6714.86083984375,
                    3315.15673828125
                ],
                [
                    6720.29638671875,
                    -11.463164329528809
                ]
            ],
            "pieceId": "25"
        },
        {
            "coordinates": [
                [
                    6724.30029296875,
                    3318.420166015625
                ],
                [
                    7653.1787109375,
                    5377.13427734375
                ],
                [
                    6729.646484375,
                    -8.20159912109375
                ]
            ],
            "pieceId": "26"
        },
        {
            "coordinates": [
                [
                    -209.09117126464844,
                    8885.404296875
                ],
                [
                    1678.0394287109375,
                    12142.0625
                ],
                [
                    880.033447265625,
                    10373.17578125
                ]
            ],
            "pieceId": "3"
        },
        {
            "coordinates": [
                [
                    -72.23892211914063,
                    328.1631164550781
                ],
                [
                    -9.901046752929688,
                    1893.236083984375
                ],
                [
                    6689.8056640625,
                    3.051757574081421
                ]
            ],
            "pieceId": "4"
        },
        {
            "coordinates": [
                [
                    0.0,
                    1891.342041015625
                ],
                [
                    1662.177978515625,
                    2551.725341796875
                ],
                [
                    2791.92724609375,
                    2021.224853515625
                ],
                [
                    6699.38037109375,
                    0.0
                ]
            ],
            "pieceId": "5"
        },
        {
            "coordinates": [
                [
                    -0.8640288710594177,
                    1902.269287109375
                ],
                [
                    864.8204345703125,
                    10374.1484375
                ],
                [
                    1668.9814453125,
                    2543.012451171875
                ]
            ],
            "pieceId": "6"
        },
        {
            "coordinates": [
                [
                    866.5504150390625,
                    10383.8994140625
                ],
                [
                    956.1519165039063,
                    10280.3876953125
                ],
                [
                    1671.375244140625,
                    2552.83349609375
                ]
            ],
            "pieceId": "7"
        },
        {
            "coordinates": [
                [
                    876.3884887695313,
                    10388.3681640625
                ],
                [
                    7664.29296875,
                    5368.06103515625
                ],
                [
                    966.5965576171875,
                    10285.384765625
                ]
            ],
            "pieceId": "8"
        },
        {
            "coordinates": [
                [
                    889.596923828125,
                    10385.0439453125
                ],
                [
                    5804.181640625,
                    7044.64892578125
                ],
                [
                    7680.15625,
                    5368.32958984375
                ]
            ],
            "pieceId": "9"
        }
    ],
    "piecesFinalTransformation": [
        {
            "pieceId": "0",
            "rotationRadians": -12.581486701965332,
            "translateVectorX": -569.9539184570313,
            "translateVectorY": 2408.46435546875
        },
        {
            "pieceId": "1",
            "rotationRadians": -25.144596099853516,
            "translateVectorX": -334.3105163574219,
            "translateVectorY": 4701.38916015625
        },
        {
            "pieceId": "10",
            "rotationRadians": 31.413475036621094,
            "translateVectorX": 2792.073974609375,
            "translateVectorY": 9857.8583984375
        },
        {
            "pieceId": "11",
            "rotationRadians": -0.009098979644477367,
            "translateVectorX": 1457.363037109375,
            "translateVectorY": 5963.54833984375
        },
        {
            "pieceId": "12",
            "rotationRadians": -0.009002288803458214,
            "translateVectorX": 2716.36181640625,
            "translateVectorY": 5670.18310546875
        },
        {
            "pieceId": "13",
            "rotationRadians": -0.007121407892554998,
            "translateVectorX": 4081.7333984375,
            "translateVectorY": 4819.79736328125
        },
        {
            "pieceId": "14",
            "rotationRadians": -0.007160348352044821,
            "translateVectorX": 4505.8154296875,
            "translateVectorY": 5367.3056640625
        },
        {
            "pieceId": "15",
            "rotationRadians": -0.007157361600548029,
            "translateVectorX": 5109.2529296875,
            "translateVectorY": 6323.8310546875
        },
        {
            "pieceId": "16",
            "rotationRadians": 31.413509368896484,
            "translateVectorX": 3544.07861328125,
            "translateVectorY": 10438.8291015625
        },
        {
            "pieceId": "17",
            "rotationRadians": 31.411142349243164,
            "translateVectorX": 3380.987060546875,
            "translateVectorY": 12345.259765625
        },
        {
            "pieceId": "18",
            "rotationRadians": 6.274524211883545,
            "translateVectorX": 2068.37255859375,
            "translateVectorY": 3204.6240234375
        },
        {
            "pieceId": "19",
            "rotationRadians": -0.0047096069902181625,
            "translateVectorX": 2304.752197265625,
            "translateVectorY": 3594.629150390625
        },
        {
            "pieceId": "2",
            "rotationRadians": -25.146371841430664,
            "translateVectorX": 214.93910217285156,
            "translateVectorY": 7048.75537109375
        },
        {
            "pieceId": "20",
            "rotationRadians": -0.004647381603717804,
            "translateVectorX": 3610.19873046875,
            "translateVectorY": 2922.002685546875
        },
        {
            "pieceId": "21",
            "rotationRadians": -0.005017527379095554,
            "translateVectorX": 4636.53173828125,
            "translateVectorY": 2234.500732421875
        },
        {
            "pieceId": "22",
            "rotationRadians": -0.004460354335606098,
            "translateVectorX": 3957.786376953125,
            "translateVectorY": 1914.0052490234375
        },
        {
            "pieceId": "23",
            "rotationRadians": 31.41005516052246,
            "translateVectorX": 5424.27587890625,
            "translateVectorY": 9659.0576171875
        },
        {
            "pieceId": "24",
            "rotationRadians": 12.559757232666016,
            "translateVectorX": 6015.29296875,
            "translateVectorY": 1381.9217529296875
        },
        {
            "pieceId": "25",
            "rotationRadians": 12.558940887451172,
            "translateVectorX": 6432.39013671875,
            "translateVectorY": 1938.907470703125
        },
        {
            "pieceId": "26",
            "rotationRadians": 6.275728702545166,
            "translateVectorX": 7035.708984375,
            "translateVectorY": 2895.7841796875
        },
        {
            "pieceId": "3",
            "rotationRadians": -18.861019134521484,
            "translateVectorX": 782.9932861328125,
            "translateVectorY": 10466.8798828125
        },
        {
            "pieceId": "4",
            "rotationRadians": 0.00017287067021243274,
            "translateVectorX": 2202.556396484375,
            "translateVectorY": 741.483642578125
        },
        {
            "pieceId": "5",
            "rotationRadians": 0.0,
            "translateVectorX": 0.0,
            "translateVectorY": 0.0
        },
        {
            "pieceId": "6",
            "rotationRadians": -25.144529342651367,
            "translateVectorX": 844.3126220703125,
            "translateVectorY": 4939.8095703125
        },
        {
            "pieceId": "7",
            "rotationRadians": -18.86125946044922,
            "translateVectorX": 1164.69189453125,
            "translateVectorY": 7739.0400390625
        },
        {
            "pieceId": "8",
            "rotationRadians": 6.277372360229492,
            "translateVectorX": 3169.092041015625,
            "translateVectorY": 8680.6044921875
        },
        {
            "pieceId": "9",
            "rotationRadians": 31.410642623901367,
            "translateVectorX": 4791.31298828125,
            "translateVectorY": 7599.33984375
        }
    ]
}

        

        # scale =1/3 
        # solution_polygons = []
        # solution_ids = []

        # for piece_json in response["piecesFinalCoords"]:#[:num_pieces_observed]:
        #     solution_polygons.append(Polygon([(p[0]*scale, p[1]*scale) for p in piece_json["coordinates"]]))
        #     solution_ids.append(int(piece_json["pieceId"]))


        # solution_polygons_aranged_by_id_ = [solution_polygons[id_] for id_ in solution_ids]
        # solution_polygons = solution_polygons_aranged_by_id_

        evaluator = Qpos(ground_truth_polygons,response)
        overlapping_score = evaluator.evaluate()

        print(overlapping_score)

        _,axs = plt.subplots(1,3)
        self.plot(evaluator.ground_truth_polygons,axs[0])
        self.plot(evaluator.translated_solution_polygons,axs[1])
        self.plot(evaluator.ground_truth_polygons,axs[2])
        self.plot(evaluator.translated_solution_polygons,axs[2],seed=8)

        plt.show()

if __name__ == "__main__":
    unittest.main()