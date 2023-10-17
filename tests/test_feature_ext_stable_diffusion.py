import unittest
from src.feature_extraction.extrapolator.stable_diffusion import SDExtrapolatorExtractor,SDOriginalExtractor,NormalizeSDOriginalExtractor,NormalizeSDExtrapolatorExtractor
from src.feature_extraction.extrapolator.stable_diffusion import extract_and_normalize_original_mean
from src.feature_extraction.pictorial import find_rotation_angle,padd_image_before_translate,trans_image
import numpy as np
from src.recipes.puzzle import loadRegularPuzzle
import matplotlib.pyplot as plt
import cv2
from src.feature_extraction import factory


db_1_num_19_noise_0_channels_means = np.array([[154.42034955, 145.18238508, 138.50948254]],dtype=np.double)


class TestPocStableDiffusion(unittest.TestCase):

    def test_load_extrapolation_image(self,piece_index=6):
        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 2
        bag_of_pieces = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level).cook()

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

    def test_load_original_image(self,piece_index=0):
        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 0
        bag_of_pieces = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level).cook()


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

    def test_translate_piece_on_extrapolated_edge(self,
                                                  piece_index=2,
                                                  edge_index=0):
        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 0
        bag_of_pieces = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level).cook()


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
        
    def test_translate_piece_on_original_edge(self,
                                              piece_index=2,
                                              edge_index=0):
        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 0
        bag_of_pieces = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level).cook()

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


class TestSDExtrapolatorExtractor(unittest.TestCase):

    def _test_edge_extrapolated(self,piece_index = 5,edge_index = 2):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        bag_of_pieces = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level).cook()

        chosen_piece = bag_of_pieces[piece_index]
        chosen_piece.load_extrapolated_image()
        feature_extractor_extrapolator = SDExtrapolatorExtractor([chosen_piece])
        feature_extractor_extrapolator.run()
        feature_name = feature_extractor_extrapolator.__class__.__name__
        edge_extra_image_ = chosen_piece.features[feature_name][edge_index]

        fig,axs = plt.subplots(1,2)
        axs[0].set_title("extrapolated_img")
        axs[0].imshow(chosen_piece.extrapolated_img)
        axs[1].set_title(f"P_{piece_index}_E_{edge_index} Extrapolated")
        axs[1].imshow(edge_extra_image_)

        plt.show()
    
    def test_edge_as_param(self,piece_index = 5,edge_index = 2):
        '''
            Change the parameter values according to your wishes
        '''
        self._test_edge_extrapolated(piece_index=piece_index,edge_index=edge_index)

    def test_P_2_E_2(self):
        print("An example where the extrapolation is not good, so there are background holes")
        print("The extrapolation eroded the left side")
        print("There is no need for cropping to keep the edges aligned...")
        self._test_edge_extrapolated(piece_index=2,edge_index=2)
    
    def test_P_2_E_0(self):
        print("An example where the extrapolation is not good, so there are background holes")
        print("The extrapolation eroded the right side")
        print("There is no need for cropping to keep the edges aligned...")
        self._test_edge_extrapolated(piece_index=2,edge_index=0)


class TestSDOriginalExtractor(unittest.TestCase):
    
    def _test_edge_original(self,piece_index = 5,edge_index = 2):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        bag_of_pieces = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level).cook()

        chosen_piece = bag_of_pieces[piece_index]
        chosen_piece.load_stable_diffusion_original_image()
        feature_extractor_extrapolator = SDOriginalExtractor([chosen_piece])
        feature_extractor_extrapolator.run()
        feature_name = feature_extractor_extrapolator.__class__.__name__
        edge_extra_image_ = chosen_piece.features[feature_name][edge_index]

        fig,axs = plt.subplots(1,2)
        axs[0].set_title("stable_diffusion_original_img")
        axs[0].imshow(chosen_piece.stable_diffusion_original_img)
        axs[1].set_title(f"P_{piece_index}_E_{edge_index}")
        axs[1].imshow(edge_extra_image_)

        plt.show()

    def test_edge_as_param(self,piece_index = 5,edge_index = 2):
        self._test_edge_original(piece_index=piece_index,edge_index=edge_index)
    
    def test_P_2_E_2(self):
        self._test_edge_original(piece_index=2,edge_index=2)
    
    def test_P_2_E_0(self):
        self._test_edge_original(piece_index=2,edge_index=0)
    
    def test_save_images(self, db=1,puzzle_num=19,puzzle_noise_level=0,out_folder="data/poc_10_pictorial_compatibility"):
        bag_of_pieces = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level).cook()

        for piece in bag_of_pieces:
            piece.load_extrapolated_image()
            piece.load_stable_diffusion_original_image()

        extrapolation_height = 13 
        feature_extractor_extrapolator = SDExtrapolatorExtractor(bag_of_pieces)
        feature_extractor_extrapolator.run()
        
        feature_extractor_original = SDOriginalExtractor(bag_of_pieces)
        feature_extractor_original.run()


        for piece in bag_of_pieces:
            for edge_index in range(piece.get_num_coords()):
                file_path_prefix = f"{out_folder}/db-{db}-puzzle-{puzzle_num}-P-{piece.id}-E-{edge_index}" 
                
                extrapolated_img = piece.features[feature_extractor_extrapolator.__class__.__name__][edge_index]
                extra_file_path = f"{file_path_prefix}_ext.png"
                cv2.imwrite(extra_file_path,extrapolated_img)

                original_img = piece.features[feature_extractor_original.__class__.__name__][edge_index]
                original_file_path = f"{file_path_prefix}_original.png"
                cv2.imwrite(original_file_path,original_img)
        
        # piece = bag_of_pieces[0]
        # edge_index = 0 
        # extrapolated_img = piece.features[feature_extractor_extrapolator.__class__.__name__][edge_index]["same"]
        # original_img = piece.features[feature_extractor_extrapolator.__class__.__name__][edge_index]["same"]
        
        plt.imshow(original_img)
        plt.show()


class TestNormalizeSDExtrapolatorExtractor(unittest.TestCase):

    def _plot_before_after_preprocessing(self,piece_index = 5,edge_index = 2):
        db = 1 # DONT'T CHANGE THIS (computed hardcoded channels mean)
        puzzle_num = 19 # DONT'T CHANGE THIS
        puzzle_noise_level = 0 # DONT'T CHANGE THIS

        bag_of_pieces = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level).cook()

        for piece in bag_of_pieces:
            piece.load_extrapolated_image()

        chosen_piece = bag_of_pieces[piece_index]
        preprocessing_feature = NormalizeSDExtrapolatorExtractor(bag_of_pieces,
                                                                 channels_mean=db_1_num_19_noise_0_channels_means)
        preprocessing_feature.run()
        feature_name = preprocessing_feature.__class__.__name__
        preprocess_image = chosen_piece.features[feature_name][edge_index]

        non_preprocessing_feature = SDExtrapolatorExtractor(bag_of_pieces)
        non_preprocessing_feature.run()
        non_preprocess_image = chosen_piece.features[non_preprocessing_feature.__class__.__name__][edge_index]

        fig,axs = plt.subplots(1,3)
        axs[0].set_title("extrapolated_img")
        axs[0].imshow(chosen_piece.extrapolated_img)
        axs[1].set_title(f"P_{piece_index}_E_{edge_index} (NON preprocessed)")
        axs[1].imshow(non_preprocess_image)
        axs[2].set_title(f"P_{piece_index}_E_{edge_index} (preprocessed)")
        axs[2].imshow(preprocess_image)

        plt.show()

    def test_P_2_E_2(self):
        self._plot_before_after_preprocessing(piece_index=2,edge_index=2)
    
    def test_P_0_E_1(self):
        self._plot_before_after_preprocessing(piece_index=0,edge_index=1)

class TestNormalizeSDOriginalExtractor(unittest.TestCase):

    def _plot_before_after_preprocessing(self,piece_index = 5,edge_index = 2):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        bag_of_pieces = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level).cook()

        for piece in bag_of_pieces:
            piece.load_stable_diffusion_original_image()

        chosen_piece = bag_of_pieces[piece_index]
        preprocessing_feature = NormalizeSDOriginalExtractor(bag_of_pieces)
        preprocessing_feature.run()
        feature_name = preprocessing_feature.__class__.__name__
        preprocess_image = chosen_piece.features[feature_name][edge_index]

        non_preprocessing_feature = SDOriginalExtractor(bag_of_pieces)
        non_preprocessing_feature.run()
        non_preprocess_image = chosen_piece.features[non_preprocessing_feature.__class__.__name__][edge_index]


        fig,axs = plt.subplots(1,3)
        axs[0].set_title("stable_diffusion_original_img")
        axs[0].imshow(chosen_piece.stable_diffusion_original_img)
        axs[1].set_title(f"P_{piece_index}_E_{edge_index} (NON preprocessed)")
        axs[1].imshow(non_preprocess_image)
        axs[2].set_title(f"P_{piece_index}_E_{edge_index} (preprocessed)")
        axs[2].imshow(preprocess_image)

        plt.show()

    def test_P_2_E_2(self):
        self._plot_before_after_preprocessing(piece_index=2,edge_index=2)
    
    def test_P_0_E_1(self):
        self._plot_before_after_preprocessing(piece_index=0,edge_index=1)


class TestLoadFromFactory(unittest.TestCase):

    def _load_feature(self,feature,piece_index=0,edge_index=0,**kwargs):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        bag_of_pieces = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level).cook()

        extractor = factory.create(feature,pieces=bag_of_pieces,**kwargs)
        extractor.run()
        feature_name = extractor.__class__.__name__
        chosen_piece = bag_of_pieces[piece_index]
        edge_image = chosen_piece.features[feature_name][edge_index]

        ax = plt.subplot()
        ax.set_title(feature_name)
        ax.imshow(edge_image)

        plt.show()

    def test_SDExtrapolatorExtractor(self,piece_index=0,edge_index=0):
        self._load_feature("SDExtrapolatorExtractor",
                           piece_index=piece_index,edge_index=edge_index)

    def test_SDOriginalExtractor(self,piece_index=0,edge_index=0):
        self._load_feature("SDOriginalExtractor",
                           piece_index=piece_index,edge_index=edge_index)
        
    def test_NormalizeSDOriginalExtractor(self,piece_index=0,edge_index=0):
        self._load_feature("NormalizeSDOriginalExtractor",
                           piece_index=piece_index,edge_index=edge_index)
    
    def test_NormalizeSDExtrapolatorExtractor(self,piece_index=0,edge_index=0):
        self._load_feature("NormalizeSDExtrapolatorExtractor",
                           piece_index=piece_index,edge_index=edge_index,
                           channels_mean=db_1_num_19_noise_0_channels_means)
    
    def test_load_common_channel(self,piece_index=0,edge_index =0):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        bag_of_pieces = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level).cook()
        extract_and_normalize_original_mean(bag_of_pieces)
        
        origin_image = bag_of_pieces[piece_index].features["NormalizeSDOriginalExtractor"][edge_index]
        extra_image = bag_of_pieces[piece_index].features["NormalizeSDExtrapolatorExtractor"][edge_index]

        fig,axs = plt.subplots(1,2)
        axs[0].set_title("NormalizeSDOriginalExtractor")
        axs[0].imshow(origin_image)
        axs[1].set_title("NormalizeSDExtrapolatorExtractor")
        axs[1].imshow(extra_image)

        plt.show()
        

        
if __name__ == "__main__":
    unittest.main()