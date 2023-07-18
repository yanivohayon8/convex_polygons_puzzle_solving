from shapely import Polygon
import numpy as np
import cv2


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
    
    def align_pieces_origin_coords_and_compute_overlap_area(self,self_edge_vertices:list, polygon_other_coords:list, edge_other_vertices:list,angle_sign=1):
        self_vertex_1_i = self_edge_vertices[0]
        self_vertex_1 = self.original_coordinates[self_vertex_1_i]

        # make self_vertex_1 the origin 
        self_coord_moved = [(ver[0]-self_vertex_1[0],ver[1]-self_vertex_1[1]) for ver in self.original_coordinates]
        other_coord_moved = [(ver[0]-self_vertex_1[0],ver[1]-self_vertex_1[1]) for ver in polygon_other_coords]

        # set the edge self_edge_vertices aligned with the axis
        self_vertex_2 = self_coord_moved[self_edge_vertices[1]]
        y = self_vertex_2[1]
        x = self_vertex_2[0]
        angle_align_with_axis = np.degrees(np.arctan2(y,x))
        print("angle_align_with_axis",angle_align_with_axis)
        #if y<0:
        if angle_align_with_axis<0:
            angle_align_with_axis = 360 - angle_align_with_axis
        # angle_align_with_axis*=-1
        # angle_align_with_axis = 0

        align_axis_rot = np.array([
            [np.cos(angle_align_with_axis),-np.sin(angle_align_with_axis)],
            [np.sin(angle_align_with_axis),np.cos(angle_align_with_axis)],
        ])

        self_coord_moved = [np.dot(align_axis_rot, np.array(coord).T).tolist() for coord in self_coord_moved]
        other_coord_moved = [np.dot(align_axis_rot, np.array(coord).T).tolist() for coord in other_coord_moved]

        # move the first vertex of other polygon on first vertex of self polygon
        other_vertex_1_i = edge_other_vertices[0]
        other_vertex_1 = other_coord_moved[other_vertex_1_i]
        other_coord_on_self = [(ver[0]-other_vertex_1[0],ver[1]-other_vertex_1[1]) for ver in other_coord_moved]

        # compute the angle between them
        self_vertex_2 = np.array(self_coord_moved[self_edge_vertices[1]])
        other_vertex_2 = np.array(other_coord_on_self[edge_other_vertices[1]])
        # cos_angle = self_vertex_2.dot(other_vertex_2)/(np.linalg.norm(self_vertex_2)*np.linalg.norm(other_vertex_2))
        # angle = np.degrees(np.arccos(cos_angle))

        # angle = 90-angle
        # angle *= -1

        angle = np.degrees(np.arctan2(other_vertex_2[1],other_vertex_2[0]))
        # angle = 360-angle
        angle*=-1

        # angle = 0######

        # rotate
        rotation_matrix = np.array([
            [np.cos(angle),-np.sin(angle)],
            [np.sin(angle),np.cos(angle)],
        ])

        other_rotated = [np.dot(rotation_matrix, np.array(coord).T).tolist() for coord in other_coord_on_self]
        other_polygon = Polygon(other_rotated)
        self_polygon = Polygon(self_coord_moved)

        return other_polygon.intersection(self_polygon).area,self_polygon,other_polygon

    
    # def align_pieces_origin_coords_and_compute_overlap_area(self,self_edge_vertices, polygon_other_coords, edge_other_vertices):
    #     polygon1 = Polygon(self.original_coordinates)
    #     # polygon2 = Polygon(polygon_other_coords)

    #     # Extract the coordinates of the vertices that lie on the edges
    #     edge1_coords = [self.original_coordinates[vertex_index] for vertex_index in self_edge_vertices]
    #     edge2_coords = [polygon_other_coords[vertex_index] for vertex_index in edge_other_vertices]

    #     # Calculate translation vector to move the second polygon
    #     translation_vector = np.array(edge1_coords[0]) - np.array(edge2_coords[0])

    #     # Move the second polygon
    #     moved_polygon2_coords = [(x + translation_vector[0], y + translation_vector[1]) for x, y in polygon_other_coords]

    #     # Calculate the angle between the edges
    #     angle1 = np.arctan2(edge1_coords[1][1] - edge1_coords[0][1], edge1_coords[1][0] - edge1_coords[0][0])
    #     angle2 = np.arctan2(edge2_coords[1][1] - edge2_coords[0][1], edge2_coords[1][0] - edge2_coords[0][0])
    #     rotation_angle = angle1 - angle2

    #     # Rotate the second polygon
    #     rotation_matrix = np.array([[np.cos(rotation_angle), -np.sin(rotation_angle)],
    #                                 [np.sin(rotation_angle), np.cos(rotation_angle)]])
    #     rotated_polygon2_coords = [np.dot(rotation_matrix, np.array(coord).T).tolist() for coord in moved_polygon2_coords]

    #     # Create the rotated polygon
    #     rotated_polygon2 = Polygon(rotated_polygon2_coords)

    #     # Calculate the area of overlap between the two polygons
    #     overlap_area = polygon1.intersection(rotated_polygon2).area

    #     return overlap_area,polygon1,rotated_polygon2    