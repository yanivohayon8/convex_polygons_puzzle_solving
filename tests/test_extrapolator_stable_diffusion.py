import unittest
from src.feature_extraction.extrapolator.stable_diffusion import SDExtrapolatorExtractor,SDOriginalExtractor,NormalizeSDExtrapolatorExtractor,NormalizeSDOriginalExtractor
from src.feature_extraction.pictorial import find_rotation_angle,padd_image_before_translate,trans_image
import numpy as np
from src.puzzle import Puzzle
import matplotlib.pyplot as plt
import cv2


class TestStableDiffusionExtractor(unittest.TestCase):

    def test_edge_extrapolated(self,piece_index = 0,edge_index = 3):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()

        chosen_piece = bag_of_pieces[piece_index]
        chosen_piece.load_extrapolated_image()
        # chosen_piece.extrapolated_img = cv2.cvtColor(chosen_piece.extrapolated_img,cv2.COLOR_BGR2RGB)
        extrapolation_height = chosen_piece.extrapolation_details.height#//2 # rule of thumb because there is a miss match between the extrapolated height to the json
        feature_extractor_extrapolator = SDExtrapolatorExtractor([chosen_piece],
                                                                               extrapolation_height=extrapolation_height)
        feature_extractor_extrapolator.run()
        edge_extra_image_ = chosen_piece.features[feature_extractor_extrapolator.__class__.__name__][edge_index]["same"]

        ax = plt.subplot()
        ax.set_title("Extrapolated")
        ax.imshow(edge_extra_image_)

        plt.show()
    
    def test_edge_original(self,piece_index = 0,edge_index = 3):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()

        chosen_piece = bag_of_pieces[piece_index]
        chosen_piece.load_stable_diffusion_original_image()
        # chosen_piece.stable_diffusion_original_img = cv2.cvtColor(chosen_piece.stable_diffusion_original_img,cv2.COLOR_BGR2RGB)
        extrapolation_height = chosen_piece.extrapolation_details.height//2# rule of thumb because there is a miss match between the extrapolated height to the json
        feature_extractor_extrapolator = SDOriginalExtractor([chosen_piece],sampling_height=extrapolation_height)
        feature_extractor_extrapolator.run()
        edge_image_ = chosen_piece.features[feature_extractor_extrapolator.__class__.__name__][edge_index]["same"]

        ax = plt.subplot()
        ax.set_title("same")
        ax.imshow(edge_image_)

        plt.show()
    
    def test_normalized_edge_extrapolated(self,piece_index = 0,edge_index = 3):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()

        chosen_piece = bag_of_pieces[piece_index]
        chosen_piece.load_extrapolated_image()
        # chosen_piece.extrapolated_img = cv2.cvtColor(chosen_piece.extrapolated_img,cv2.COLOR_BGR2RGB)
        extrapolation_height = chosen_piece.extrapolation_details.height#//2 # rule of thumb because there is a miss match between the extrapolated height to the json
        feature_extractor_extrapolator = NormalizeSDExtrapolatorExtractor([chosen_piece],
                                                                               extrapolation_height=extrapolation_height)
        feature_extractor_extrapolator.run()
        edge_extra_image_ = chosen_piece.features[feature_extractor_extrapolator.__class__.__name__][edge_index]["same"]

        ax = plt.subplot()
        ax.set_title("Extrapolated")
        ax.imshow(edge_extra_image_)

        plt.show()
    
    def test_normalized_edge_original(self,piece_index = 0,edge_index = 3):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()

        chosen_piece = bag_of_pieces[piece_index]
        chosen_piece.load_stable_diffusion_original_image()
        # chosen_piece.stable_diffusion_original_img = cv2.cvtColor(chosen_piece.stable_diffusion_original_img,cv2.COLOR_BGR2RGB)
        extrapolation_height = chosen_piece.extrapolation_details.height//2# rule of thumb because there is a miss match between the extrapolated height to the json
        feature_extractor_extrapolator = NormalizeSDOriginalExtractor([chosen_piece],sampling_height=extrapolation_height)
        feature_extractor_extrapolator.run()
        edge_image_ = chosen_piece.features[feature_extractor_extrapolator.__class__.__name__][edge_index]["same"]

        ax = plt.subplot()
        ax.set_title("same")
        ax.imshow(edge_image_)

        plt.show()


class TestPocStableDiffusion(unittest.TestCase):

    def test_load_extrapolation_image(self,piece_index=4):
        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 0
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        puzzle.load()

        bag_of_pieces = puzzle.get_bag_of_pieces()
        piece = bag_of_pieces[piece_index]
        coords = piece.raw_coordinates
        shifted_coords = piece.extrapolation_details.match_piece_to_img(coords)
        piece.load_extrapolated_image()
        plt.imshow(piece.extrapolated_img)
        plt.fill(
                shifted_coords[:, 0],
                shifted_coords[:, 1],
                alpha=0.5,
                color='orange')
        plt.show()

    def test_load_original_image(self,piece_index=5):
        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 0
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()

        piece = bag_of_pieces[piece_index]
        coords = piece.raw_coordinates
        shifted_coords = piece.extrapolation_details.match_piece_to_img(coords)
        piece.load_stable_diffusion_original_image()
        # piece.stable_diffusion_original_img = cv2.cvtColor(piece.stable_diffusion_original_img,cv2.COLOR_BGR2RGB)

        plt.imshow(piece.stable_diffusion_original_img)
        plt.fill(
                shifted_coords[:, 0],
                shifted_coords[:, 1],
                alpha=0.5,
                color='orange')
        plt.show()

    def test_translate_piece_on_extrapolated_edge(self,piece_index=5,edge_index=1):
        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 0
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()

        piece = bag_of_pieces[piece_index]
        coords = piece.raw_coordinates
        shifted_coords = piece.extrapolation_details.match_piece_to_img(coords)
        piece.load_extrapolated_image()
        # piece.extrapolated_img = cv2.cvtColor(piece.extrapolated_img,cv2.COLOR_BGR2RGB)

        next_edge_index = (edge_index+1)%len(shifted_coords)
        angle = find_rotation_angle(shifted_coords,edge_index,next_edge_index)
        edge_row = shifted_coords[edge_index][1]
        edge_col = shifted_coords[edge_index][0]
        next_edge_row = shifted_coords[next_edge_index][1]
        next_edge_col = shifted_coords[next_edge_index][0]
        edge_width = int(np.sqrt((edge_col-next_edge_col)**2 + (edge_row-next_edge_row)**2)) #abs(curr_col-next_col)
        padded_image = padd_image_before_translate(piece.extrapolated_img,edge_width)
        translated_img = trans_image(padded_image,edge_col,edge_row,angle,edge_row,edge_col)

        # cropped_img = translated_img[:30,:edge_width]

        non_background_indices = np.argwhere(np.any(translated_img != [0,0,0],axis=2))
        min_row,min_col = np.min(non_background_indices,axis=0)
        
        # max_row,max_col = np.max(non_background_indices,axis=0)
        # cropped_img = translated_img[min_row:max_row,min_col:max_col]
        
        max_row = piece.extrapolation_details.height#//2 # rule of thumb because there is a miss match between the extrapolated height to the json
        cropped_img = translated_img[:max_row,min_col:min_col+edge_width]

        
        # fig, axs = plt.subplots(2,2)
        # axs[0,0].imshow(piece.extrapolated_img)
        # axs[0,0].set_title("original")
        # axs[0,1].imshow(padded_image)
        # axs[0,1].set_title("padded")
        # axs[1,0].imshow(translated_img)
        # axs[1,0].set_title("translated")
        # axs[1,1].imshow(cropped_img)
        # axs[1,1].set_title("cropped")
        
        
        axs2 = plt.subplot()
        axs2.imshow(cropped_img)
        axs2.set_title("cropped")
        
        fig, axs = plt.subplots(1,2)
        axs[0].imshow(piece.extrapolated_img)
        axs[0].set_title("original")
        axs[1].imshow(translated_img)
        axs[1].set_title("translated")

        plt.show()
        
    def test_translate_piece_on_original_edge(self,piece_index=5,edge_index=1):
        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 0
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()

        piece = bag_of_pieces[piece_index]
        coords = piece.raw_coordinates
        shifted_coords = piece.extrapolation_details.match_piece_to_img(coords)
        piece.load_stable_diffusion_original_image()
        # piece.stable_diffusion_original_img = cv2.cvtColor(piece.stable_diffusion_original_img,cv2.COLOR_BGR2RGB)

        next_edge_index = (edge_index+1)%len(shifted_coords)
        angle = find_rotation_angle(shifted_coords,edge_index,next_edge_index)
        edge_row = shifted_coords[edge_index][1]
        edge_col = shifted_coords[edge_index][0]
        next_edge_row = shifted_coords[next_edge_index][1]
        next_edge_col = shifted_coords[next_edge_index][0]
        edge_width = int(np.sqrt((edge_col-next_edge_col)**2 + (edge_row-next_edge_row)**2)) #abs(curr_col-next_col)

        height_sampling = piece.extrapolation_details.height#//3
        translated_img = trans_image(piece.stable_diffusion_original_img,edge_col,edge_row,angle,edge_row-height_sampling,edge_col)

        non_background_indices = np.argwhere(np.any(translated_img != [0,0,0],axis=2))
        min_row,min_col = np.min(non_background_indices,axis=0)
        cropped_img = translated_img[:height_sampling,min_col:min_col+edge_width]

        axs2 = plt.subplot()
        axs2.imshow(cropped_img)
        axs2.set_title("cropped")
        
        fig, axs = plt.subplots(1,2)
        axs[0].imshow(piece.stable_diffusion_original_img)
        axs[0].set_title("original")
        axs[1].imshow(translated_img)
        axs[1].set_title("translated")

        plt.show()

if __name__ == "__main__":
    unittest.main()