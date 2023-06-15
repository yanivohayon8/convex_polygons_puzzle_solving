import unittest 
import cv2
from src.piece import Piece
import matplotlib.pyplot as plt
from src.feature_extraction.pictorial import slice_image,rotate_and_crop,trans_image
import numpy as np

class TestPictorialFeatureExtractor(unittest.TestCase):
    
    def test_slice_image_func(self):
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
        center_col = piece.img.shape[1]/2 #216
        center_row = piece.img.shape[0]/2
        angle = 0
        width = piece.img.shape[1]#300
        height = piece.img.shape[0]
        scale = 1

        fig, axs = plt.subplots(1,2)
        pictorial_content = slice_image(piece.img,center_col,center_row,angle,width,height,scale=scale)
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

        curr_index = 1
        next_index = 2

        curr_row = coordinates[curr_index][1]
        curr_col = coordinates[curr_index][0]
        next_row = coordinates[next_index][1]
        next_col = coordinates[next_index][0]

        #plt.imshow(piece.img)
        center_x = int((curr_col+next_col)/2)#piece.img.shape[0]/2 #216
        center_y = int((curr_row+next_row)/2)
        width = int(np.sqrt((curr_col-next_col)**2 + (curr_row-next_row)**2)) #abs(curr_col-next_col)
        #height = abs(next_row-curr_row)
        height_sampling = 500
        
        angle = np.arctan((next_row-curr_row)/(next_col-curr_col))*180/np.pi

        if next_col-curr_col < 0:
            angle +=180

        img_only_rotate_from_center = trans_image(piece.img,center_x,center_y,angle,0,0) # 
        img_only_rotate = trans_image(piece.img,curr_col,curr_row,angle,0,0) # center_x,center_y

        img_rot_and_trans = trans_image(piece.img,curr_col,curr_row,angle,curr_row,curr_col) # this should result as the image is hidding right above the top left corner
        img_height_as_param = trans_image(piece.img,curr_col,curr_row,angle,curr_row-height_sampling,curr_col)
        
        content = img_height_as_param[:height_sampling,:width]

        fig, axs = plt.subplots(2,3)
        axs[0,0].set_title("piece.img")
        axs[0,0].imshow(piece.img)
        axs[0,1].set_title("results")
        axs[0,1].imshow(content)
        axs[0,2].set_title("img_only_rotate_from_center")
        axs[0,2].imshow(img_only_rotate_from_center)
        axs[1,0].set_title("img_only_rotate_from_vertex")
        axs[1,0].imshow(img_only_rotate)
        axs[1,1].set_title("img_rot_and_trans")
        axs[1,1].imshow(img_rot_and_trans)
        axs[1,2].set_title("img_height_as_param")
        axs[1,2].imshow(img_height_as_param)
        
        plt.show()
        pass
    
    def test_crop_then_rotate(self):
        puzzleDirectory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0"
        piece_id = "0"
        img_path = puzzleDirectory+f"/{piece_id}.png"
        image = cv2.imread(img_path,cv2.COLOR_BGR2RGB)


        coordinates = [
            (0,1144),
            (433,1369),
            (1939,845),
            (1191,0)
        ]

        # row1 = 0
        # col1 = 0
        # row2 = image.shape[0]
        # col2 = image.shape[1]
        # angle = 0 #45  # In degrees
        # rotated,cropped_image = rotate_and_crop(image,(row1,col1,col2,row2),angle)

        # # # switch from cartesian to image coordinates
        row1 = 1144
        col1 = 0
        row2 = 1369
        col2 = 433

        #angle = 0 #45  # In degrees
        angle = np.arctan(col2-col1/row2-row1)*180/np.pi
        rotated,cropped_image = rotate_and_crop(image,(col1,row1,col2,row2),angle)

        fig, axs = plt.subplots(2,2)
        axs[0,0].set_title("cropped_image")
        axs[0,0].imshow(cropped_image)
        axs[0,1].set_title("rotated")
        axs[0,1].imshow(rotated)
        axs[1,0].set_title("Original Image")
        axs[1,0].imshow(image)
        plt.show()

        

if __name__ == "__main__":
    unittest.main()