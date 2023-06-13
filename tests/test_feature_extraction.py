import unittest 
import cv2
from src.piece import Piece
import matplotlib.pyplot as plt
from src.feature_extraction.pictorial import slice_image
import numpy as np

class TestPictorialFeatureExtractor(unittest.TestCase):
    
    def test_sample_whole_image(self):
        puzzleDirectory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0"
        piece_id = "0"
        img_path = puzzleDirectory+f"/{piece_id}.png"
        coordinates = [
            (0.0,1144.617911756789),
            (433.1002195373303,1369.8862015073328),
            (1939.6970145840846,845.5681099625981),
            (1191.439977412138,0.0)
        ]

        piece = Piece(piece_id,None,img_path)
        piece.load_image()

        #plt.imshow(piece.img)
        center_x = piece.img.shape[0]/2 #216
        center_y = piece.img.shape[1]/2
        angle = 0
        width = piece.img.shape[0]#300
        height = piece.img.shape[1]
        scale = 1

        fig, axs = plt.subplots(1,2)
        pictorial_content = slice_image(piece.img,center_x,center_y,angle,width,height,scale=scale)
        axs[0].imshow(pictorial_content)
        axs[1].imshow(piece.img)
        plt.show()


    def test_sample_edge(self):
        puzzleDirectory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0"
        piece_id = "0"
        img_path = puzzleDirectory+f"/{piece_id}.png"
        coordinates = [
            (0,1144),
            (433,1369),
            (1939,845),
            (1191,0)
        ]

        piece = Piece(piece_id,coordinates,img_path)
        piece.load_image()

        curr_coord_x = coordinates[0][0]
        curr_coord_y = coordinates[0][1]
        next_coord_x = coordinates[1][0]
        next_coord_y = coordinates[1][1]

        #plt.imshow(piece.img)
        center_x = 500#int((curr_coord_x+next_coord_x)/2)#piece.img.shape[0]/2 #216
        center_y = 500#int((curr_coord_y+next_coord_y)/2)
        width = 400
        
        # vector_x = next_coord_x-curr_coord_x
        # vector_y = next_coord_y-curr_coord_y
        height = 600#int(np.sqrt(vector_x**2+vector_y**2))

        angle = 0#np.arctan2(vector_y,vector_x) * 180/np.pi

        fig, axs = plt.subplots(1,2)
        pictorial_content = slice_image(piece.img,center_x,center_y,angle,
                                        width,height)
        axs[0].imshow(pictorial_content)
        axs[1].imshow(piece.img)
        plt.show()
        raise("Not working")
        pass


if __name__ == "__main__":
    unittest.main()