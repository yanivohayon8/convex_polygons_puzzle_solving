import unittest
import cv2
from src.feature_extraction import image_process 
import matplotlib.pyplot as plt

images_folder = "data/poc_10_pictorial_compatibility/db-1-puzzle-19-noise-0_v2/"

class TestFlipImage(unittest.TestCase):
    
    def test_0_1_axes(self,image_name="db-1-puzzle-19-P-2-E-2_original"):
        img = cv2.imread(images_folder+"/"+image_name+".png")
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        flipped = image_process.filp_image(img)

        fig, axs = plt.subplots(1,2)
        axs[0].imshow(img)
        axs[0].set_title("img")
        axs[1].imshow(flipped)
        axs[1].set_title("flipped")

        plt.show()





if __name__ == "__main__":
    unittest.main()