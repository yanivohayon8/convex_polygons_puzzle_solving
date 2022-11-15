import unittest
from src.visualizers import cv2_wrapper 
import cv2
import numpy as np

class TestFrame(unittest.TestCase):

    def test_simple_square(self):
        frame = cv2_wrapper.Frame(size=(1080,1920,3))
        square_length = 200
        simple_square = np.array([
            (0,0),(square_length,0),(square_length,square_length),(0,square_length)
        ])

        frame.draw_polygons([simple_square],[(255,0,0)])
        frame.show()
        frame.wait()
        frame.destroy()

    def test_showimg(self):
        frame = cv2_wrapper.Frame(size=(2880,1620,3))

        img_path = "..\data\ofir\Pseudo-Sappho_MAN_Napoli_Inv9084\Puzzle1\0\0.png"
        img = cv2.imread(img_path,cv2.COLOR_BGR2RGB)



if __name__ == "__main__":
    unittest.main()