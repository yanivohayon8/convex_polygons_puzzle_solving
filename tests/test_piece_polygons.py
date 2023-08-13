import unittest
# from src.piece import move_and_rotate_polygons
from src.piece import Piece
from src.piece import overlapping_area,semi_dice_coef_overlapping,compute_iou
from matplotlib.patches import Polygon as MatplotlibPolygon
import matplotlib.pyplot as plt
import numpy as np
from shapely import Polygon
from shapely import affinity


class TestPieceAttributes(unittest.TestCase):

    def test_inner_angle(self):
        # piece zero in puzzle Inv9084 puzzle 1
        angles = [70.78026064882025, 87.72737855452097, 67.56571608921074, 133.92664470744808]
        


class TestTwoPolygonsAlign(unittest.TestCase):
    
    def _plot(self,ax,polygon1_coords,polygon2_coords):
        #fig, ax = plt.subplots()
        # Convert polygon coordinates to Matplotlib polygons
        polygon1 = MatplotlibPolygon(polygon1_coords, edgecolor='blue', facecolor='none', linewidth=2)
        polygon2 = MatplotlibPolygon(polygon2_coords, edgecolor='red', facecolor='none', linewidth=2)

        # Add polygons to the axis
        ax.add_patch(polygon1)
        ax.add_patch(polygon2)

        # Set axis limits
        x_coords = [coord[0] for coord in polygon1_coords + polygon2_coords]
        y_coords = [coord[1] for coord in polygon1_coords + polygon2_coords]
        ax.set_xlim(min(x_coords) - 1, max(x_coords) + 1)
        ax.set_ylim(min(y_coords) - 1, max(y_coords) + 1)

        # Set axis labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        #ax.set_title('Two Polygons')

        # Display the plot
        #
        #plt.waitforbuttonpress()

    
    def test_hardcoded(self):
        polygon_8 = [(0.0,0.0),
                    (1012.0741665619662,500.5796613721416),
                    (894.3125757357866,263.5534858178564)]
        piece_8 = Piece(6,polygon_8)
        polygon_9 = [(967.0356002382177,255.9119595492084),
                    (738.532991218126,122.36138943672267),
                    (0.0,0.0),
                    (1259.6811080818297,863.2661759857438)]
        piece_9 = Piece(9,polygon_9)
        edge8_vertices = [1, 2]
        edge9_vertices = [1,0]
        # edge8_vertices = [1, 2]
        # edge9_vertices = [0,1]

        fig, ax = plt.subplots(2,2)

        ax[0,0].set_title("Start")
        xs_0_0 = [polygon_8[vert_i][0] for vert_i in  edge8_vertices]
        xs_0_0 += [polygon_9[vert_i][0] for vert_i in edge9_vertices]
        ys_0_0 = [polygon_8[vert_i][1] for vert_i in  edge8_vertices]
        ys_0_0 += [polygon_9[vert_i][1] for vert_i in edge9_vertices]
        ax[0,0].scatter(xs_0_0,ys_0_0)
        self._plot(ax[0,0],polygon_8,polygon_9)
        ax[0,0].grid()

        edge8_vertex_1_i = edge8_vertices[0]
        p_8_set_vertex_8_1 =  piece_8.move_coords(polygon_8,polygon_8[edge8_vertex_1_i])
        p_9_set_vertex_8_1 = piece_9.move_coords(polygon_9,polygon_8[edge8_vertex_1_i])
        ax[0,1].set_title("Move pieces: vertex of piece8 is in origin")
        xs_0_1 = [p_8_set_vertex_8_1[vert_i][0] for vert_i in  edge8_vertices]
        xs_0_1 += [p_9_set_vertex_8_1[vert_i][0] for vert_i in edge9_vertices]
        ys_0_1 = [p_8_set_vertex_8_1[vert_i][1] for vert_i in  edge8_vertices]
        ys_0_1 += [p_9_set_vertex_8_1[vert_i][1] for vert_i in edge9_vertices]
        ax[0,1].scatter(xs_0_1,ys_0_1)
        self._plot(ax[0,1],p_8_set_vertex_8_1,p_9_set_vertex_8_1)
        ax[0,1].grid()

        edge9_vertex_1_i = edge9_vertices[0]
        p_9_set_vertex_9_1 = piece_9.move_coords(p_9_set_vertex_8_1,p_9_set_vertex_8_1[edge9_vertex_1_i])
        ax[1,0].set_title("Move pieces 9 (2) to origin")
        xs_1_0 = [p_8_set_vertex_8_1[vert_i][0] for vert_i in  edge8_vertices]
        xs_1_0 += [p_9_set_vertex_9_1[vert_i][0] for vert_i in edge9_vertices]
        ys_1_0 = [p_8_set_vertex_8_1[vert_i][1] for vert_i in  edge8_vertices]
        ys_1_0 += [p_9_set_vertex_9_1[vert_i][1] for vert_i in edge9_vertices]
        ax[1,0].scatter(xs_1_0,ys_1_0)
        self._plot(ax[1,0],p_8_set_vertex_8_1,p_9_set_vertex_9_1)
        ax[1,0].grid()

        p_8_v_2 = np.array(p_8_set_vertex_8_1[edge8_vertices[1]])
        p_9_v_2 = np.array(p_9_set_vertex_9_1[edge9_vertices[1]])
        cos_angle = p_8_v_2.dot(p_9_v_2)/(np.linalg.norm(p_8_v_2)*np.linalg.norm(p_9_v_2))
        angle = np.degrees(np.arccos(cos_angle))

        origin = (0,0)
        is_right = (p_8_v_2[0] - origin[0])*(p_9_v_2[1] - origin[0]) - (p_8_v_2[1] - origin[1])*(p_9_v_2[0] - origin[0]) > 0
        if is_right:
            angle *= -1
        
        p_9_polygon = Polygon(p_9_set_vertex_9_1)
        p_9_polygon = affinity.rotate(p_9_polygon,angle,origin=p_9_set_vertex_9_1[edge9_vertices[0]])
        p_9_rotated = list(p_9_polygon.exterior.coords)

        


        ax[1,1].set_title("Rotate Piece 2 to align piece 1")
        xs_1_1 = [p_8_set_vertex_8_1[vert_i][0] for vert_i in  edge8_vertices]
        xs_1_1 += [p_9_rotated[vert_i][0] for vert_i in edge9_vertices]
        ys_1_1 = [p_8_set_vertex_8_1[vert_i][1] for vert_i in  edge8_vertices]
        ys_1_1 += [p_9_rotated[vert_i][1] for vert_i in edge9_vertices]
        ax[1,1].scatter(xs_1_1,ys_1_1)
        self._plot(ax[1,1],p_8_set_vertex_8_1,p_9_rotated)
        ax[1,1].grid()

        # plt.grid()
        plt.show()

    def test_Inv9084_8_9(self):
        polygon_8 = [(0.0,0.0),
                    (1012.0741665619662,500.5796613721416),
                    (894.3125757357866,263.5534858178564)]
        piece_8 = Piece(6,polygon_8)
        polygon_9 = [(967.0356002382177,255.9119595492084),
                    (738.532991218126,122.36138943672267),
                    (0.0,0.0),
                    (1259.6811080818297,863.2661759857438)]
        piece_9 = Piece(9,polygon_9)
        
        # edge8_vertices = [1, 2]
        # edge9_vertices = [1,0]
        # area,poly8,poly9 = piece_8.align_pieces_on_edge_and_compute_overlap_area(piece_9,edge8_vertices,edge9_vertices)
        
        edge8_vertices = [1, 2]
        edge9_vertices = [1,0]
        area,poly8,poly9 = piece_8.align_pieces_on_edge_and_compute_overlap_area(piece_9,edge8_vertices,edge9_vertices)

        ax = plt.subplot()
        self._plot(ax,poly8,poly9)
        xs = [poly8[edge8_vertices[0]][0],poly8[edge8_vertices[1]][0],poly9[edge9_vertices[0]][0],poly9[edge9_vertices[1]][0]]
        ys = [poly8[edge8_vertices[0]][1],poly8[edge8_vertices[1]][1],poly9[edge9_vertices[0]][1],poly9[edge9_vertices[1]][1]]
        ax.scatter(xs,ys)
        ax.grid()
        plt.show()

    def test_Inv9084_6_9(self):

        polygon_6 = [(317.0016030246443,972.6080337150197),
                    (747.3753572848327,42.81779674124118),
                    (0.0,0.0)]
        piece_6 = Piece(6,polygon_6)
        polygon_9 = [(967.0356002382177,255.9119595492084),
                    (738.532991218126,122.36138943672267),
                    (0.0,0.0),
                    (1259.6811080818297,863.2661759857438)]
        piece_9 = Piece(9,polygon_9)
        edge6_vertices = [1, 2] # [1,2]
        edge9_vertices = [2, 1]#[2, 1]

        # overlap_area = move_and_rotate_polygons(polygon_6,edge6_vertices,polygon_9,edge9_vertices)
        area,poly6,poly9 = piece_6.align_pieces_on_edge_and_compute_overlap_area(piece_9,edge6_vertices,edge9_vertices)

        ax = plt.subplot()
        self._plot(ax,poly6,poly9)
        xs = [poly6[edge6_vertices[0]][0],poly6[edge6_vertices[1]][0],poly9[edge9_vertices[0]][0],poly9[edge9_vertices[1]][0]]
        ys = [poly6[edge6_vertices[0]][1],poly6[edge6_vertices[1]][1],poly9[edge9_vertices[0]][1],poly9[edge9_vertices[1]][1]]
        ax.scatter(xs,ys)
        ax.grid()
        plt.show()

class TestPolygonsOverlap(unittest.TestCase):

    def test_toy_example(self):
        poly1 = Polygon([(0,0),(2,0),(2,2),(0,2)])
        poly2 = Polygon([(0,1),(2,1),(2,0)])

        polys = [poly1,poly2]
        print(overlapping_area(polys))

    def test_toy_example_2(self):
        polygons = [
            [(0, 0), (0, 4), (4, 4), (4, 0)],   # Square with area 16
            [(3, 3), (3, 7), (7, 7), (7, 3)],   # Square with area 16
            [(5, 5), (5, 9), (9, 9), (9, 5)],   # Square with area 16
            [(6, 6), (6, 10), (10, 10), (10, 6)] # Square with area 16
        ]

        area = overlapping_area(polygons) 
        assert area == 4 
    
class TestSemiDiceCoeffient(unittest.TestCase):

    def test_toy_example(self):
        poly1 = Polygon([(0,0),(2,0),(2,2),(0,2)])
        poly2 = Polygon([(0,1),(2,1),(2,0)])

        polys = [poly1,poly2]
        print(semi_dice_coef_overlapping(polys))

    def test_toy_example_2(self):
        polygons = [
            [(0, 0), (0, 4), (4, 4), (4, 0)],   # Square with area 16
            [(3, 3), (3, 7), (7, 7), (7, 3)],   # Square with area 16
            [(5, 5), (5, 9), (9, 9), (9, 5)],   # Square with area 16
            [(6, 6), (6, 10), (10, 10), (10, 6)] # Square with area 16
        ]

        area = semi_dice_coef_overlapping(polygons) 
        print(area)
    
class TestIoU(unittest.TestCase):

    def test_toy_example_2(self):
        polygons = [
            [(0, 0), (0, 4), (4, 4), (4, 0)],   # Square with area 16
            [(3, 3), (3, 7), (7, 7), (7, 3)],   # Square with area 16
            [(5, 5), (5, 9), (9, 9), (9, 5)],   # Square with area 16
            [(6, 6), (6, 10), (10, 10), (10, 6)] # Square with area 16
        ]

        iou = compute_iou(polygons) 
        assert iou == 4/64

if __name__ == "__main__":
    unittest.main()