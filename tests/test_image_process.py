import unittest
import cv2
from src.feature_extraction import image_process 
import matplotlib.pyplot as plt
import glob

from src.feature_extraction.extrapolator.stable_diffusion import SDExtrapolatorExtractor,SDOriginalExtractor
from src.puzzle import Puzzle

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


class TestRecipeFlipCropSubMean(unittest.TestCase):

    def test_toy_example(self,plot_index = 4):
        images = [cv2.imread(file) for file in glob.glob(images_folder+"/*original.png")]
        before_img = images[plot_index]
        recipe = image_process.RecipeFlipCropSubMean()
        channels_mean = recipe.compute_channels_mean(images)
        processed_img = recipe.process(images[plot_index],channels_mean)

        fig, axs = plt.subplots(1,2)
        axs[0].imshow(before_img)
        axs[0].set_title("before processing")
        axs[1].imshow(processed_img)
        axs[1].set_title("after processing")

        plt.show()
    
    def test_SDOriginalExtractor_integration(self,piece_index = 5,edge_index = 2):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()

        [piece.load_stable_diffusion_original_image() for piece in bag_of_pieces]
        feature_extractor_extrapolator = SDOriginalExtractor(bag_of_pieces)
        feature_extractor_extrapolator.run()

        recipe = image_process.RecipeFlipCropSubMean()
        feature_name = feature_extractor_extrapolator.__class__.__name__
        images = [piece.features[feature_name][edge] for piece in bag_of_pieces for edge in range(piece.get_num_coords())]
        channels_mean = recipe.compute_channels_mean(images)
        chosen_piece = bag_of_pieces[piece_index]
        chosen_piece.features[feature_name][edge_index] = recipe.process(chosen_piece.features[feature_name][edge_index],channels_mean)

        plt.imshow(chosen_piece.features[feature_name][edge_index])
        plt.show()





        

if __name__ == "__main__":
    unittest.main()