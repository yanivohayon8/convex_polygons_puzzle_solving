import unittest 
from src.feature_extraction.extrapolator.lama_masking import mask_line
from PIL import Image
from PIL import ImageDraw
from shapely import Polygon,Point
import matplotlib.pyplot as plt
import cv2

class TestPOC(unittest.TestCase):
    
    def test_convert_rgba_to_rgb(self):
        db = "1"
        puzzle_num = "13"
        puzzle_noise_level = 0
        directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        piece_name = "4"
        input_image_path = f"{directory}/images/{piece_name}.png"
        output_rgb_image_path = f"{directory}/rgb/{piece_name}.png"
        convert_rgba_to_rgb(input_image_path,output_rgb_image_path)
        # output_mask_path = f"{directory}/masks/{piece_name}_mask.png"

    def test_draw_white_lines(self):
        db = "1"
        puzzle_num = "13"
        puzzle_noise_level = 0
        directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        piece_name = "4"
        input_image_path = f"{directory}/images/{piece_name}.png"

        piece_image = Image.open(input_image_path)
        mask_image = Image.new("RGB",piece_image.size,0)

        piece4_coords = [(0.0,0.0),(627.1196899414062,606.4771728515625),(832.7311401367188,665.748779296875),(1624.2766723632812,758.9954223632812)]
        piece4_coords_ = piece4_coords+[piece4_coords[0]]
        drawer = ImageDraw.Draw(mask_image)
        drawer.line(piece4_coords_,fill=(255,255,255),width=10)

        # fig, axs = plt.subplots(1,2)
        # axs[0].imshow(mask_image)
        # axs[0].set_title("Only draw lines")
        # plt.show()
        mask_image.save(f"{directory}/rgb/{piece_name}_mask.png")


    def test_extrapolated_edges(self):
        db = "1"
        puzzle_num = "13"
        puzzle_noise_level = 0
        directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        piece_name = "4"

        # mask_image = Image.open(f"{directory}/rgb/{piece_name}_mask.png")
        # mask_pixels = mask_image.load()

        piece4_coords = [(0.0,0.0),(627.1196899414062,606.4771728515625),(832.7311401367188,665.748779296875),(1624.2766723632812,758.9954223632812)]
        piece4_coords_ = [(int(coord[0]),int(coord[1])) for coord in piece4_coords+[piece4_coords[0]]]

        image = cv2.imread(f"{directory}/extrapolated/{piece_name}_mask.png")
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        width = 10
        debug_masked_images = []
        edges_content = []
        
        for prev_coord,next_coord in zip(piece4_coords_[:-1],piece4_coords_[1:]):
            masked_image,line_pixels = mask_line(image,prev_coord,next_coord,width)
            debug_masked_images.append(masked_image)
        
        fig, axs_masked_images = plt.subplots(2,2)

        axs_masked_images[0,0].imshow(debug_masked_images[0])
        axs_masked_images[0,0].axis("off")
        axs_masked_images[0,1].imshow(debug_masked_images[1])
        axs_masked_images[0,1].axis("off")
        axs_masked_images[1,0].imshow(debug_masked_images[2])
        axs_masked_images[1,0].axis("off")
        axs_masked_images[1,1].imshow(debug_masked_images[3])
        axs_masked_images[1,1].axis("off")
        
        plt.show()



if __name__ == "__main__":
    unittest.main()