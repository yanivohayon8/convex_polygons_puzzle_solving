import numpy as np
from functools import reduce
from shapely import affinity
from src import shared_variables

def least_square_rigid_motion_svd(points:np.array,ground_truth:np.array,points_weights:np.array):
    '''
        implementation of https://vincentqin.gitee.io/blogresource-3/slam-common-issues-ICP/svd_rot.pdf
    '''
    assert points.shape == ground_truth.shape
    assert points.shape[0] == points_weights.shape[0]

    points_centroid = np.average(points,axis=0,weights=points_weights)
    ground_truth_centroid = np.average(ground_truth,axis=0,weights=points_weights)

    centered_points = points-points_centroid
    centered_ground_truth = ground_truth - ground_truth_centroid

    X = centered_points.T # 2xN
    Y = centered_ground_truth.T # 2xN
    W = np.diag(points_weights)
    S = X@W@Y.T

    U,sigma, V = np.linalg.svd(S)

    diag_d = np.identity(X.shape[0])
    diag_d[-1,-1] = np.linalg.det(V@U.T)

    R = V@diag_d@U.T
    t = ground_truth_centroid - R@points_centroid.T

    return R,t



class AreaOverlappingEvaluator():

    def __init__(self,ground_truth_polygons:list) -> None:
        '''
        solution_coordinates - list of shapely polygons
        ground_truth_coordinates - list of shapely polygons
        '''
        # solution_polygons = solution_polygons
        self.ground_truth_polygons = ground_truth_polygons
        self.weights = []
        self.R = None
        self.t = None
    
    def _compute_weights(self):
        total_area = reduce(lambda acc,polygon: acc+polygon.area,self.ground_truth_polygons,0)
        self.weights = np.array([polygon.area/(total_area+1e-5) for polygon in self.ground_truth_polygons for _ in list(polygon.exterior.coords)])

    def _compute_transformation(self,solution_polygons):
        if len(self.weights)==0:
            raise ("Call _compute_weights first")
        
        solution_points = np.array([coord for polygon in solution_polygons for coord in list(polygon.exterior.coords)])
        ground_truth_points = np.array([coord for polygon in self.ground_truth_polygons for coord in list(polygon.exterior.coords)])
        self.R,self.t = least_square_rigid_motion_svd(solution_points,ground_truth_points,self.weights)
        return self.R,self.t

    def _transform_solution_polygons(self,solution_polygons):
        self.transfomed_polygons_solution = []
        transformation_params = [self.R[0,0],self.R[0,1],self.R[1,0],self.R[1,1],self.t[0],self.t[1]]

        for polygon in solution_polygons:
            self.transfomed_polygons_solution.append(affinity.affine_transform(polygon,transformation_params))
        
        return self.transfomed_polygons_solution
    
    def _score(self):
        score_sum = 0

        for poly_index in range(len(self.transfomed_polygons_solution)):                                
            solution_poly = self.transfomed_polygons_solution[poly_index]
            ground_truth_poly = self.ground_truth_polygons[poly_index]
            intersection_area = solution_poly.intersection(ground_truth_poly).area
            score_sum += intersection_area/(solution_poly.area+1e-5)
        
        return score_sum # score_num/len()

    def evaluate(self,solution_polygons,excluded_pieces=[]):
        bag_of_pieces = shared_variables.puzzle.bag_of_pieces
        self.ground_truth_polygons = [polygon for piece,polygon in zip(bag_of_pieces,self.ground_truth_polygons) if piece.id not in excluded_pieces]

        self._compute_weights()
        self._compute_transformation(solution_polygons)
        self._transform_solution_polygons(solution_polygons)
        return self._score()


        
    

