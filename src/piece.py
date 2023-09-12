from shapely import Polygon
import numpy as np
import cv2
from shapely import affinity
from shapely.ops import unary_union #cascaded_union
from functools import reduce

class Piece():

    def __init__(self,id:str,coordinates:list,img_path=None,extrapolated_img_path=None) -> None:
        self.id = id
        self.polygon = Polygon(coordinates)
        self.coordinates = coordinates
        self.original_coordinates = coordinates # before ccw in puzzle._preprocess
        self.features = {}
        self.ccw_edge2origin_edge = {}
        self.img_path = img_path
        self.img = None
        self.extrapolated_img_path = extrapolated_img_path
        self.extrapolated_img = None
        self.stable_diffusion_original_img_path = ""
        self.stable_diffusion_original_img = None
        self.raw_coordinates = None # Coordinates Ofir computed without any of my postprocessing. For extrating the stabe diffustion extrapolation pictorial content
        self.extrapolation_details = None # instance of StableDiffusionExtrapolationDetails

    def load_image(self):
        self.img = cv2.imread(self.img_path)
        self.img = self.img[...,::-1] # BGR to RGB

    def load_extrapolated_image(self):
        self.extrapolated_img = cv2.imread(self.extrapolated_img_path)
        self.extrapolated_img = cv2.cvtColor(self.extrapolated_img,cv2.COLOR_BGR2RGB)
        # self.extrapolated_img = cv2.cvtColor(self.extrapolated_img,cv2.COLOR_BGR2LAB)
        # self.extrapolated_img = cv2.cvtColor(self.extrapolated_img,cv2.COLOR_BGR2HSV)

    def load_stable_diffusion_original_image(self):
        self.stable_diffusion_original_img = cv2.imread(self.stable_diffusion_original_img_path)
        self.stable_diffusion_original_img = cv2.cvtColor(self.stable_diffusion_original_img,cv2.COLOR_BGR2RGB)

    def get_coords(self):
        '''
            Get the coordinates of the piece where its center of mass is the origin of the axis.
            This is because we read it from the piece.csv file...
        '''
        return list(self.polygon.exterior.coords)#[:-1]
    
    def get_num_coords(self):
        return len(list(self.polygon.exterior.coords)[:-1])

    def get_vertices_indices(self,edge_index):
        return edge_index,(edge_index+1)%len(self.original_coordinates)
    
    def get_origin_index(self, edge_index):
        '''Before counter clockwise sort'''
        return self.ccw_edge2origin_edge[edge_index]
    
    def align_pieces_on_edge_and_compute_overlap_area(self,other_piece,self_edge_vertices_indecies:list, 
                                                      other_edge_vertices_indecies:list):
        
        self_vertex_1_i = self_edge_vertices_indecies[0]

        # move self piece such that the first vertex of the input edge is in the origin
        translate_vector = self.original_coordinates[self_vertex_1_i]
        self_coords_moved =  [(coord[0]-translate_vector[0],coord[1]-translate_vector[1]) for coord in self.original_coordinates]
        other_coords_moved = [(coord[0]-translate_vector[0],coord[1]-translate_vector[1]) for coord in other_piece.original_coordinates]
        
        # move the other piece so the first vertex is in the origin
        other_vertex_1_i = other_edge_vertices_indecies[0]
        translate_vector = other_coords_moved[other_vertex_1_i]
        other_coords_moved = [(coord[0]-translate_vector[0],coord[1]-translate_vector[1]) for coord in other_coords_moved]
        
        # rotate the other polygon so the edges are aligned
        self_vertex_2 = np.array(self_coords_moved[self_edge_vertices_indecies[1]])
        other_vertex_2 = np.array(other_coords_moved[other_edge_vertices_indecies[1]])
        cos_angle = self_vertex_2.dot(other_vertex_2)/(np.linalg.norm(self_vertex_2)*np.linalg.norm(other_vertex_2))
        angle = np.degrees(np.arccos(cos_angle))

        origin = (0,0)
        is_right = (self_vertex_2[0] - origin[0])*(other_vertex_2[1] - origin[0]) - (self_vertex_2[1] - origin[1])*(other_vertex_2[0] - origin[0]) > 0
        
        if is_right:
            angle *= -1
        
        other_polygon = Polygon(other_coords_moved)
        other_polygon = affinity.rotate(other_polygon,angle,origin=other_coords_moved[other_edge_vertices_indecies[0]])
        
        self_polygon = Polygon(self_coords_moved)
        area = other_polygon.intersection(self_polygon).area
        return area, list(self_polygon.exterior.coords),list(other_polygon.exterior.coords)


    def get_inner_angle(self,edge_index_1,edge_index_2):
        if edge_index_1 == 0 and edge_index_2 == self.get_num_coords()-1 or \
            edge_index_2 == 0 and edge_index_1 == self.get_num_coords()-1:
            return self.features["angles"][0]

        vertex_index = max(edge_index_1,edge_index_2)
        return self.features["angles"][vertex_index]
    

    def _push_polygon_outwards(self,polygon:Polygon, distance:int):
        # Find the center of the polygon
        center = polygon.centroid
        
        # Create a list to store the new vertices
        new_vertices = []
        
        # Iterate through the old vertices and push them outwards
        for vertex in polygon.exterior.coords:
            # Calculate the vector from the center to the vertex
            vector = np.array(vertex) - np.array(center.coords[0])
            
            # Normalize the vector
            norm_vector = vector / np.linalg.norm(vector)
            
            # Calculate the new vertex position
            new_vertex = np.array(vertex) + distance * norm_vector
            
            new_vertices.append(new_vertex)
        
        # Create a new polygon from the updated vertices
        new_polygon = Polygon(new_vertices)
        
        return new_polygon

    def push_original_coordinates(self,distance:int)->Polygon:
        return self._push_polygon_outwards(Polygon(self.coordinates),distance)

def overlapping_area(polygons:list):
    '''
        polygons: list of lists of tuples
    '''
    # Convert the list of polygons to Shapely Polygon objects
    shapely_polygons = [Polygon(poly) for poly in polygons]

    # Calculate the overlapping area by taking the union of all polygons
    overlapping_polygon = unary_union(shapely_polygons) #cascaded_union(shapely_polygons)

    # Return the area of the overlapping polygon
    return overlapping_polygon.area


def compute_iou(polygons):
    polygons = [Polygon(p) for p in polygons]
    
    # The reduce may fail ....
    intersection = reduce(lambda x, y: x.intersection(y), polygons)
    union = reduce(lambda x, y: x.union(y), polygons)
    
    iou = intersection.area / union.area
    return iou

def semi_dice_coef_overlapping(polygons:list):
    shapely_polygons = [Polygon(poly) for poly in polygons]
    dice_sum = 0

    for i in range(len(shapely_polygons)):
        other_polygons = [shapely_polygons[j] for j in range(len(shapely_polygons)) if i!=j]    
        other_union = unary_union(other_polygons)
        curr_intersect_with_other = shapely_polygons[i].intersection(other_union)
        dice_sum+= curr_intersect_with_other.area/shapely_polygons[i].area

    return dice_sum




class StableDiffusionExtrapolationDetails():
    '''
        Details from the extrapolation_details.json 
        from the stable diffusion extrapolation
    '''
    def __init__(self,x_offset,y_offset,scale_factor,height,should_denormalize=True) -> None:
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.scale_factor = scale_factor
        self.height = height
        self.should_denormalize= should_denormalize
    
    def match_piece_to_img(self,coords:np.array):
        shifted_coords = np.copy(coords)

        if self.scale_factor != 1.0:
            for i, vertice in enumerate(coords):
                shifted_coords[i][0] = vertice[0] * self.scale_factor
                shifted_coords[i][1] = vertice[1] * self.scale_factor
        
        if self.should_denormalize:
            denormalization_value = np.min(shifted_coords, axis=0)
        else:
            denormalization_value = np.array([0, 0])
        shifted_coords[:, 0] = shifted_coords[:, 0] - denormalization_value[0] + self.x_offset
        shifted_coords[:, 1] = shifted_coords[:, 1] - denormalization_value[1] + self.y_offset

        return shifted_coords