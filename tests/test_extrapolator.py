import unittest 
from src.feature_extraction.extrapolator.lama_masking import mask_line
from PIL import Image
from PIL import ImageDraw
from shapely import Polygon,Point
import matplotlib.pyplot as plt
import cv2
import numpy as np
from src.puzzle import Puzzle
from src.feature_extraction.extrapolator.stable_diffusion import StableDiffusionExtrapolationExtractor
from src.feature_extraction.pictorial import find_rotation_angle,padd_image_before_translate,trans_image

# class TestStableDiffusionExtractor(unittest.TestCase):

#     def test_edge_extrapolated(self):
#         db = 1
#         puzzle_num = 19
#         puzzle_noise_level = 0
#         puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
#         puzzle.load()
#         bag_of_pieces = puzzle.get_bag_of_pieces()

#         # PARAMS
#         piece_index = 0
#         edge_index = 3
#         sampling_height = 30 # TO BE DELETE?

#         chosen_piece = bag_of_pieces[piece_index]
#         chosen_piece.load_extrapolated_image()
#         chosen_piece.extrapolated_img = cv2.cvtColor(chosen_piece.extrapolated_img,cv2.COLOR_BGR2RGB)
#         feature_extractor_extrapolator = StableDiffusionExtrapolationExtractor([chosen_piece],sampling_height=sampling_height)
#         feature_extractor_extrapolator.run()

#         edge_extra_image_ = chosen_piece.features[feature_extractor_extrapolator.__class__.__name__][edge_index]["original"]

#         ax = plt.subplot()

#         ax.set_title("Extrapolated")
#         ax.imshow(edge_extra_image_)

#         plt.show()





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

        piece4_coords = [(0.0,0.0),(627.1196899414062,606.4771728515625),(832.7311401367188,665.748779296875),(1624.2766723632812,758.9954223632812)]
        piece4_coords_ = [(int(coord[0]),int(coord[1])) for coord in piece4_coords+[piece4_coords[0]]]

        image = cv2.imread(f"{directory}/extrapolated/DB-{db}-puzzle-{puzzle_num}-noise-{puzzle_noise_level}-{piece_name}_mask.png")
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        width = 10
        debug_masked_images = []
        edges_pixels = []

        for prev_coord,next_coord in zip(piece4_coords_[:-1],piece4_coords_[1:]):
            masked_image,edge_pixels = mask_line(image,prev_coord,next_coord,width)
            debug_masked_images.append(masked_image)
            edges_pixels.append(edge_pixels)

        width_extrapolation = 10
        is_show_all_edges = False#True

        if is_show_all_edges:

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

            fig2, axs_line_pixels = plt.subplots(2,2)
            axs_flatten = axs_line_pixels.flatten()

            for i,edge_pixels_ in enumerate(edges_pixels):
                num_pad = width_extrapolation - edge_pixels_.shape[0]%width_extrapolation
                edge_padded = np.pad(edge_pixels_,((0,num_pad),(0,0)),constant_values=0)
                # edge_img = edge_padded.reshape(width_extrapolation,-1,3)
                edge_img = edge_padded.reshape(-1,width_extrapolation,3)
                axs_flatten[i].imshow(edge_img)
            
            plt.show()
        else:
            jj = 1 
            fig3, axs_zoomed = plt.subplots(1,2)
            axs_zoomed[0].imshow(debug_masked_images[jj])
            
            num_pad = width_extrapolation - edges_pixels[jj].shape[0]%width_extrapolation
            edge_padded = np.pad(edges_pixels[jj],((0,num_pad),(0,0)),constant_values=0)
            edge_img = edge_padded.reshape(-1,width_extrapolation,3)
            axs_zoomed[1].imshow(edge_img)
            
            
            
            plt.show()






if __name__ == "__main__":
    unittest.main()