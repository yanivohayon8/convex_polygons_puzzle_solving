from shapely import Polygon
import numpy as np
import cv2
from shapely import affinity
from shapely.ops import unary_union #cascaded_union
from functools import reduce

class Piece():

    def __init__(self,id:str,coordinates:list,img_path=None) -> None:
        self.id = id
        self.polygon = Polygon(coordinates)
        self.coordinates = coordinates
        self.original_coordinates = coordinates # before ccw in puzzle._preprocess
        self.img_path = img_path
        self.img = None
        self.features = {}
        self.ccw_edge2origin_edge = {}

    def load_image(self):
        self.img = cv2.imread(self.img_path)
        self.img = self.img[...,::-1] # BGR to RGB

    def get_coords(self):
        '''
            Get the coordinates of the piece where its center of mass is the origin of the axis.
            This is because we read it from the piece.csv file...
        '''
        return list(self.polygon.exterior.coords)#[:-1]
    
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
