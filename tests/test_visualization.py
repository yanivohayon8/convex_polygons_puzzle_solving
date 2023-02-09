import unittest
import numpy as np
import cv2 
import matplotlib.pyplot as plt


class TestOpencv(unittest.TestCase):


    def test_draw_line(self):
        # Create a black image
        img = np.zeros((512,512,3), np.uint8)
        # Draw a diagonal blue line with thickness of 5 px
        cv2.line(img,(0,0),(511,511),(255,0,0),5)
        cv2.namedWindow("Test")
        cv2.imshow("Test",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def test_draw_polygon(self):
        # Create a black image
        img = np.zeros((512,512,3), np.uint8)
        # Draw a diagonal blue line with thickness of 5 px
        pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(0,255,255),)
        cv2.fillPoly(img,[pts],(0,255,255))
        cv2.namedWindow("Test")
        cv2.imshow("Test",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def test_simple_video(self):
        frameSize = (500, 500)
        out = cv2.VideoWriter('data/output_video.avi',cv2.VideoWriter_fourcc(*'DIVX'), 60, frameSize)
        for i in range(0,255):
            img = np.ones((500, 500, 3), dtype=np.uint8)*i
            out.write(img)

        out.release()

    def test_interactive_video(self):
        img = np.zeros((512,512,3), np.uint8)
        cv2.namedWindow("Test")
        cv2.imshow("Test",img)

        # Draw a diagonal blue line with thickness of 5 px
        pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(0,255,255),)
        cv2.fillPoly(img,[pts],(0,255,255))
        cv2.imshow("Test",img)

        for i in range(5):
            img = np.zeros((512,512,3), np.uint8)
            pts = pts + 40
            cv2.polylines(img,[pts],True,(0,255,255),)
            cv2.fillPoly(img,[pts],(0,255,255))
            cv2.imshow("Test",img)
            cv2.waitKey(0)


        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def test_plot_img(self):
        #img = cv2.imread("data\\ofir\\Pseudo-Sappho_MAN_Napoli_Inv9084\\Puzzle1\\0\\ground_truth.jpg")
        img = cv2.imread("data\\ofir\\Pseudo-Sappho_MAN_Napoli_Inv9084\\Puzzle1\\0\\0.png")
        
        w,h,c = img.shape

        # Set screen resolution
        resolution = (1920, 1080)

        # # Create window
        cv2.namedWindow("Output")
        cv2.resizeWindow("Output", resolution[0], resolution[1])

        # new_w = w#int(w*1.5)
        # new_h = h#int(h*1.5)

        # img = cv2.resize(img, (new_w, new_h))
        # img = cv2.copyMakeBorder( img,
        #  int((1080-new_h)/2), int((1080-new_h)/2),
        #   int((1920-new_w)/2), int((1920-new_h)/2), 0)

        cv2.imshow("Output",img)

        if cv2.waitKey(0) == ord('q'):
            cv2.destroyAllWindows()
        
        #plt.imshow(img)
        #plt.close()
        

if __name__ == "__main__":
    unittest.main()