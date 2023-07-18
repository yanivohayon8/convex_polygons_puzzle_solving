import unittest
# from src.piece import move_and_rotate_polygons
from src.piece import Piece
from matplotlib.patches import Polygon as MatplotlibPolygon
import matplotlib.pyplot as plt



class TestTwoPolygonsAlign(unittest.TestCase):
    
    def _plot(self,polygon1_coords,polygon2_coords):
        fig, ax = plt.subplots()
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
        ax.set_title('Two Polygons')

        # Display the plot
        plt.grid()
        plt.show()
        #plt.waitforbuttonpress()

    def test_two_pieces_overlap_Inv9084_1(self):

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
        edge9_vertices = [1, 2]#[2, 1]

        # overlap_area = move_and_rotate_polygons(polygon_6,edge6_vertices,polygon_9,edge9_vertices)
        angle_sign = -1
        overlap_area,polygon_1,polygon_2 = piece_6.align_pieces_origin_coords_and_compute_overlap_area(edge6_vertices,piece_9.original_coordinates,edge9_vertices,angle_sign=angle_sign)
        print(overlap_area)
        self._plot(list(polygon_1.exterior.coords),list(polygon_2.exterior.coords))

    def test_two_pieces_overlap_Inv9084_2(self):
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
        edge9_vertices = [0, 1]#[0, 1]

        # overlap_area = move_and_rotate_polygons(polygon_6,edge6_vertices,polygon_9,edge9_vertices)
        angle_sign = 1
        overlap_area,polygon_8,polygon_9 = piece_8.align_pieces_origin_coords_and_compute_overlap_area(edge8_vertices,
                                                                                                       piece_9.original_coordinates,
                                                                                                       edge9_vertices,angle_sign=angle_sign)
        print(overlap_area)

        polygon1_coords = list(polygon_8.exterior.coords)
        polygon2_coords = list(polygon_9.exterior.coords)
        self._plot(polygon1_coords,polygon2_coords)

        


    


if __name__ == "__main__":
    unittest.main()