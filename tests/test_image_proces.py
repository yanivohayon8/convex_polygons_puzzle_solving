import unittest
import cv2
from src.feature_extraction import image_process 
import matplotlib.pyplot as plt

images_folder = "data/poc_10_pictorial_compatibility/db-1-puzzle-19-noise-0_v2/"

class TestFunctions(unittest.TestCase):
    
    def _load_rgb_image(self,image_path):
        img = cv2.imread(image_path)
        return cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    def test_flip_0_1_axes(self,image_name="db-1-puzzle-19-P-2-E-2_original"):
        image_path = images_folder+"/"+image_name+".png"
        img = self._load_rgb_image(image_path)
        flipped = image_process.filp_image(img)

        fig, axs = plt.subplots(1,2)
        axs[0].imshow(img)
        axs[0].set_title("img")
        axs[1].imshow(flipped)
        axs[1].set_title("flipped")

        plt.show()

    def test_flip_none(self,image_name="db-1-puzzle-19-P-2-E-2_original"):
        image_path = images_folder+"/"+image_name+".png"
        img = self._load_rgb_image(image_path)
        flipped = image_process.filp_image(img,axes=())

        fig, axs = plt.subplots(1,2)
        axs[0].imshow(img)
        axs[0].set_title("img")
        axs[1].imshow(flipped)
        axs[1].set_title("flipped (should not flipped)")

        plt.show()

    def test_get_non_zero_pixels(self,image_name="db-1-puzzle-19-P-2-E-2_original"):
        image_path = images_folder+"/"+image_name+".png"
        img = self._load_rgb_image(image_path)
        x_non_zero,y_non_zero = image_process.get_non_zero_pixels(img)
        img_marked = img.copy()
        img_marked[x_non_zero,y_non_zero] = 255

        fig, axs = plt.subplots(1,2)
        axs[0].imshow(img)
        axs[0].set_title("img")
        axs[1].imshow(img_marked)
        axs[1].set_title("marked non background image")

        plt.show()

# edge2extrapolate_images_plot[second_plot_edge][x_non_zero,y_non_zero] = mark_color


if __name__ == "__main__":
    unittest.main()