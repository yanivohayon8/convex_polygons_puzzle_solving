import numpy as np
from functools import reduce
from shapely import affinity,MultiPolygon,Polygon
from src import shared_variables
from src.physics.restore_assembly_img import center_of_mass

def least_square_rigid_motion_svd(points:np.array,ground_truth:np.array,points_weights:np.array):
    '''
        implementation of https://igl.ethz.ch/projects/ARAP/svd_rot.pdf
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
    V = V.T

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
        
        fixed_point = MultiPolygon(solution_polygons).centroid #solution_polygons[0].centroid

        for polygon in solution_polygons:
            self.transfomed_polygons_solution.append(affinity.affine_transform(polygon,transformation_params))
        
            # # polygon_transformed = affinity.rotate(polygon,np.arccos(self.R[0,0]),use_radians=True)
            # polygon_transformed = affinity.rotate(polygon,np.arccos(self.R[0,0]),use_radians=True,origin=fixed_point)
            # polygon_transformed = affinity.translate(polygon_transformed,self.t[0],self.t[1])
            # self.transfomed_polygons_solution.append(polygon_transformed)
        
        return self.transfomed_polygons_solution
    
    def _score(self):
        score_sum = 0

        total_area= sum(map(lambda p: p.area,self.transfomed_polygons_solution))
        raise("The total area shold include also the excluded points")

        for poly_index in range(len(self.transfomed_polygons_solution)):                                
            solution_poly = self.transfomed_polygons_solution[poly_index]
            ground_truth_poly = self.ground_truth_polygons[poly_index]
            intersection_area = solution_poly.intersection(ground_truth_poly).area
            
            # Actually we could just divide the intersection area with sum_area, but to avoid dividing small numbers by large numbers, 
            # I wrote piece_weight explicitly
            piece_weight = solution_poly.area/(total_area+1e-5)
            score_sum += piece_weight * intersection_area/(solution_poly.area+1e-5) 
        
        return score_sum # score_num/len()

    def evaluate(self,solution_polygons,excluded_pieces=[]):

        if len(excluded_pieces) != 0:
            bag_of_pieces = shared_variables.puzzle.bag_of_pieces
            self.ground_truth_polygons = [polygon for piece,polygon in zip(bag_of_pieces,self.ground_truth_polygons) if piece.id not in excluded_pieces]

        self._compute_weights()
        self._compute_transformation(solution_polygons)
        self._transform_solution_polygons(solution_polygons)
        return self._score()


        
    

def registration_only_one_piece(solution_polygons,ground_truth_polygons,excluded_pieces=[]):

    if len(excluded_pieces) != 0:
        bag_of_pieces = shared_variables.puzzle.bag_of_pieces
        ground_truth_polygons = [polygon for piece,polygon in zip(bag_of_pieces,ground_truth_polygons) if piece.id not in excluded_pieces]

    
    pieces_areas = list(map(lambda p: p.area,ground_truth_polygons))
    largest_piece_index = pieces_areas.index(max(pieces_areas))
    solution_largest_polygon = solution_polygons[largest_piece_index]
    ground_truth_largest_polygon = ground_truth_polygons[largest_piece_index]

    ground_truth_coords = np.array(solution_largest_polygon.exterior.coords)
    ground_truth_truth_coords = np.array(ground_truth_largest_polygon.exterior.coords)

    R,_ = least_square_rigid_motion_svd(ground_truth_coords,ground_truth_truth_coords,np.ones(ground_truth_coords.shape[0]))
    t = ground_truth_largest_polygon.centroid - solution_largest_polygon.centroid
        
    translated_polygons = [affinity.translate(polygon,t.x,t.y) for polygon in solution_polygons]
    center_of_all = MultiPolygon(translated_polygons).centroid
    angle = np.arccos(R[0,0])
    rotated_polygons = [affinity.rotate(polygon,-angle,use_radians=True,origin=center_of_all) for polygon in translated_polygons]

    q_pos = 0

    return q_pos,translated_polygons,rotated_polygons
    

    # for solution_poly,ground_truth_poly in zip(solution_polygons,ground_truth_polygons):                                

    #     transformed_solution_poly    
    #     intersection_area = solution_poly.intersection(ground_truth_poly).area
        
    #     # Actually we could just divide the intersection area with sum_area, but to avoid dividing small numbers by large numbers, 
    #     # I wrote piece_weight explicitly
    #     piece_weight = solution_poly.area/(total_area+1e-5)
    #     score_sum += piece_weight * intersection_area/(solution_poly.area+1e-5) 



class Qpos():

    def __init__(self,ground_truth_polygons:list,simulation_response,solution_scale=1/3) -> None:
        # solution_scale - refer in fix_dataset project...
        
        self.ground_truth_polygons = ground_truth_polygons
        self.total_gd_area = sum(map(lambda p: p.area,self.ground_truth_polygons))

        self.simulation_response = simulation_response

        self.solution_polygons = []
        self.solution_ids = []

        for piece_json in self.simulation_response["piecesFinalCoords"]:#[:num_pieces_observed]:
            self.solution_polygons.append(Polygon([(p[0]*solution_scale, p[1]*solution_scale) for p in piece_json["coordinates"]]))
            self.solution_ids.append(int(piece_json["pieceId"]))
        # if len(excluded_pieces) != 0:
        #     bag_of_pieces = shared_variables.puzzle.bag_of_pieces
        #     self.ground_truth_polygons = [polygon for piece,polygon in zip(bag_of_pieces,self.ground_truth_polygons) if piece.id not in excluded_pieces]


        # because the bag of pieces is sorted by the ids 
        self.solution_polygons = [p for _,p in sorted(zip(self.solution_ids,self.solution_polygons))]
        self.solution_ids = sorted(self.solution_ids)

        self.anchored_piece_index = None
        self.anchored_piece_id = None
        
        for i,piece_json in enumerate(self.simulation_response["piecesFinalTransformation"]):
            if piece_json["translateVectorX"] == 0 and piece_json["translateVectorY"] == 0 and piece_json["rotationRadians"] ==0:
                self.anchored_piece_index = i
                self.anchored_piece_id = piece_json["pieceId"]
                break

        


    def evaluate_based_pivot(self,pivot_piece_index=3):
        '''
            solution_polygons - list of polygons
        '''
        # center_of_solution = MultiPolygon(solution_polygons).centroid
        
        # dont change pivot_piece_index=0
        # This probabliy because of a bug, but setting this variable to 0 works 
        # TODO: debug it later
        
        solution_pivot_polygon = self.solution_polygons[pivot_piece_index]
        ground_truth_pivot_polygon = self.ground_truth_polygons[pivot_piece_index]
        solution_coords = np.array(solution_pivot_polygon.exterior.coords)[:-1]
        ground_truth_truth_coords = np.array(ground_truth_pivot_polygon.exterior.coords)[:-1]
        weights = np.ones(solution_coords.shape[0])
        R,t = least_square_rigid_motion_svd(solution_coords,ground_truth_truth_coords,weights)

        


        # # self.translated_solution_polygons = [affinity.rotate(polygon,-trans["rotationRadians"],use_radians=True,origin=center_of_mass(polygon)) for trans, polygon in zip(self.simulation_response["piecesFinalTransformation"] ,self.solution_polygons)] 
        # self.translated_solution_polygons = []
        # anchored_piece_mass_x = None
        # anchored_piece_mass_y = None

        # # TODO: ....
        # # anchored_piece_mass_x,anchored_piece_mass_y = center_of_mass(self.solution_polygons[self.anchored_piece_index])
        # # anchored_piece_mass_x*=1/3
        # # anchored_piece_mass_y*=1/3

        # for trans, polygon in zip(self.simulation_response["piecesFinalTransformation"] ,self.solution_polygons):
        #     # trans_poly = affinity.rotate(polygon,-trans["rotationRadians"],use_radians=True,origin="centroid")
        #     trans_poly = affinity.rotate(polygon,-trans["rotationRadians"],use_radians=True,origin=center_of_mass(polygon))
        #     # tx = trans["translateVectorX"]
        #     # tx*=1/3
        #     # ty = trans["translateVectorY"]
        #     # ty*=1/3

        #     # # if trans["pieceId"] != self.anchored_piece_id:
        #     # #     tx -= anchored_piece_mass_x
        #     # #     ty -= anchored_piece_mass_y

        #     # trans_poly = affinity.translate(trans_poly,tx,ty)
        #     self.translated_solution_polygons.append(trans_poly)

         

        angle = np.arccos(R[0,0])
        pivot_center = center_of_mass(self.solution_polygons[pivot_piece_index])
        self.translated_solution_polygons = [affinity.rotate(polygon,-angle,use_radians=True,origin=pivot_center) for polygon in self.solution_polygons]
        # self.translated_solution_polygons = [polygon for polygon in self.solution_polygons]

        tx = ground_truth_pivot_polygon.centroid.x-self.translated_solution_polygons[pivot_piece_index].centroid.x
        ty = ground_truth_pivot_polygon.centroid.y-self.translated_solution_polygons[pivot_piece_index].centroid.y
        self.translated_solution_polygons = [affinity.translate(polygon,tx,ty) for polygon in self.translated_solution_polygons]

        score_sum = 0

        for solution_poly,poly_id in zip(self.translated_solution_polygons,self.solution_ids):
            ground_truth_poly = self.ground_truth_polygons[poly_id]
            intersection_area = solution_poly.intersection(ground_truth_poly).area
                
            # Actually we could just divide the intersection area with sum_area, but to avoid dividing small numbers by large numbers, 
            # I wrote piece_weight explicitly
            piece_weight = solution_poly.area/(self.total_gd_area+1e-5)
            score_sum += piece_weight * intersection_area/(solution_poly.area+1e-5) 
        
        return score_sum # score_num/len()



    def evaluate(self):
        # sometimes changing the pivot bring the desired resutls 
        best_score = -9999999999
        best_translated_solution_polygons = None

        for i in range(len(self.solution_ids)):

            try:
                score = self.evaluate_based_pivot(pivot_piece_index=i)
            except Exception as e:
                score = 0
                self.translated_solution_polygons = None

            if best_score < score:
                best_score = score
                best_translated_solution_polygons = self.translated_solution_polygons

        self.translated_solution_polygons = best_translated_solution_polygons

        return best_score
