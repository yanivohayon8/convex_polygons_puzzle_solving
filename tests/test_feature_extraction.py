import unittest 
import cv2
from src.piece import Piece
import matplotlib.pyplot as plt
from src.feature_extraction.pictorial import slice_image,rotate_and_crop,trans_image
import numpy as np
from src.feature_extraction import geometric as geo_extractor 
from src.puzzle import Puzzle
from src.feature_extraction.extrapolator.lama_masking import LamaEdgeExtrapolator,reshape_line_to_image


class TestLamaExtrapolation(unittest.TestCase):


    def test_toy_example(self):
        pieces = [
            Piece("0",
                  [
                      (279.26156414925936,0.0),
                        (0.0,400.418000125509),
                        (325.5645334835908,1962.0680983081097),
                        (1260.6015084925616,1329.154326230219)
                      ])
        ]

        pieces[0].extrapolated_img_path = '../ConvexDrawingDataset/DB1/Puzzle19/noise_0\\extrapolated\\rgb-0_mask.png'
        pieces[0].load_extrapolated_image()

        feature_extractor = LamaEdgeExtrapolator(pieces)
        feature_extractor.run()
        assert len(pieces[0].features["edges_extrapolated_lama"]) == 4

        axs_zoomed = plt.subplot()
        jj = 2
        width_extrapolation = 10
        edge_pixels = pieces[0].features["edges_extrapolated_lama"][jj]
        edge_img = reshape_line_to_image(edge_pixels,width_extrapolation)
        axs_zoomed.imshow(edge_img)
        plt.show()


    def test_edge_vs_edge_display(self):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()
        piece_ii = 8
        edge_ii = 0
        piece_jj = 7
        edge_jj = 2
        pieces = [bag_of_pieces[piece_ii],bag_of_pieces[piece_jj]]

        for piece in pieces:
            piece.load_extrapolated_image()

        feature_extractor = LamaEdgeExtrapolator(pieces)
        feature_extractor.run()

        fig,axs = plt.subplots(1,2)
        width_extrapolation = 10 # as preproceessed beforehand
        edges_indices = [edge_ii,edge_jj]
        pieces_indecies = [piece_ii,piece_jj]
        edges_names = [f"P_{pieces_indecies[0]}_E_{edges_indices[0]}",f"P_{pieces_indecies[1]}_E_{edges_indices[1]}"]

        for k in range(2):
            edge_pixels = pieces[k].features["edges_extrapolated_lama"][edges_indices[k]]
            edge_img = reshape_line_to_image(edge_pixels,width_extrapolation) 
            axs[k].imshow(edge_img)
            axs[k].set_title(edges_names[k])

        plt.show()
        edge_ii_length = pieces[0].features["edges_extrapolated_lama"][edges_indices[0]].shape[0]
        edge_jj_length = pieces[1].features["edges_extrapolated_lama"][edges_indices[1]].shape[0]
        assert abs(edge_ii_length -  edge_jj_length) < width_extrapolation, f"{edges_names[0]} length is {edge_ii_length} and {edges_names[1]} length is {edge_jj_length}. The diffrence is too big "











class TestGeometric(unittest.TestCase):


    def test_edge_length(self):
        pieces = [
            Piece("0",[(-847.4256148049196,409.07035256641507),(-390.6580493044287,580.180048490992),(1039.668350940752,-119.88084521481937),(198.41531316859664,-869.3695558425879)])
        ]

        length_extractor = geo_extractor.EdgeLengthExtractor(pieces)
        length_extractor.run()
        print(pieces[0].features["edges_length"])
    
    def test_angle(self):
        pieces = [
            Piece("0",[(-847.4256148049196,409.07035256641507),(-390.6580493044287,580.180048490992),(1039.668350940752,-119.88084521481937),(198.41531316859664,-869.3695558425879)])
        ]

        angles_extractor = geo_extractor.AngleLengthExtractor(pieces)
        angles_extractor.run()

        print(pieces[0].features["angles"])
    



if __name__ == "__main__":
    unittest.main()