import unittest
import numpy as np
import cv2 

class TestVisuallization(unittest.TestCase):


    def test_draw_line(self):
        # Create a black image
        img = np.zeros((512,512,3), np.uint8)
        # Draw a diagonal blue line with thickness of 5 px
        cv2.line(img,(0,0),(511,511),(255,0,0),5)
        cv2.namedWindow("Test")
        cv2.imshow("Test",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    unittest.main()