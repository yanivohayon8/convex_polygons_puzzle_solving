import unittest 
import numpy as np
import matplotlib.pyplot as plt
from src.puzzle import Puzzle
from src.feature_extraction import image_process 
from src.feature_extraction.extrapolator.stable_diffusion import SDExtrapolatorExtractor,SDOriginalExtractor
from src.pairwise_matchers.stable_diffusion import DotProductExtraToOriginalMatcher

class TestFunction_score_pair(unittest.TestCase):

    def _load_chosen_pieces_pair(self,piece_ii,piece_jj,db = 1,puzzle_num = 19,puzzle_noise_level = 0):
        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()
        chosen_pieces = [bag_of_pieces[piece_ii],bag_of_pieces[piece_jj]]
        
        for piece in chosen_pieces:
            piece.load_extrapolated_image()
            piece.load_stable_diffusion_original_image()

        return chosen_pieces
    
    ''' WITHOUT preprocessing '''

    def test_score_no_preprocessing(self,piece_ii = 5,edge_ii = 2,
                                     piece_jj = 3,edge_jj = 1,is_plot=True):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        chosen_pieces = self._load_chosen_pieces_pair(piece_ii,piece_jj,
                                                 db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level)    

        extrapolation_extractor = SDExtrapolatorExtractor(chosen_pieces)
        extrapolator_extractor_name = extrapolation_extractor.__class__.__name__
        extrapolation_extractor.run()

        original_extractor = SDOriginalExtractor(chosen_pieces)
        original_extractor_name = original_extractor.__class__.__name__
        original_extractor.run()

        pictorial_matcher = DotProductExtraToOriginalMatcher(chosen_pieces,
                                                             extrapolator_extractor_name,
                                                             original_extractor_name)

        edge_ii_extra_img = chosen_pieces[0].features[extrapolator_extractor_name][edge_ii]
        edge_ii_original_img = chosen_pieces[0].features[original_extractor_name][edge_ii]
        edge_jj_extra_img = chosen_pieces[1].features[extrapolator_extractor_name][edge_jj]
        edge_jj_original_img = chosen_pieces[1].features[original_extractor_name][edge_jj]

        ''' Becaues of the background based cropping the feature extraction the images height might not be unified'''

        if edge_ii_extra_img.shape[0] > edge_jj_original_img.shape[0]:
            edge_ii_extra_img = edge_ii_extra_img[:edge_jj_original_img.shape[0]]
        elif edge_jj_original_img.shape[0] > edge_ii_extra_img.shape[0]:
            diff = edge_jj_original_img.shape[0] - edge_ii_extra_img.shape[0]
            edge_jj_original_img = edge_jj_original_img[diff:diff+edge_ii_extra_img.shape[0]]

        score_left = pictorial_matcher._score_pair(edge_ii_extra_img,edge_jj_original_img)

        if edge_jj_extra_img.shape[0] > edge_ii_original_img.shape[0]:
            edge_jj_extra_img = edge_jj_extra_img[:edge_ii_original_img.shape[0]]
        elif edge_ii_original_img.shape[0] > edge_jj_extra_img.shape[0]:
            diff = edge_ii_original_img.shape[0] - edge_jj_extra_img.shape[0]
            edge_ii_original_img = edge_ii_original_img[diff:diff+edge_jj_extra_img.shape[0]]

        score_right = pictorial_matcher._score_pair(edge_jj_extra_img,edge_ii_original_img)

        if is_plot:
            fig, axs = plt.subplots(2,2)
            fig.suptitle(f"Left col score: {score_left}; Right col score: {score_right}")
            
            axs[0,0].set_title(f"P_{piece_jj}_E_{edge_jj} Original")
            axs[0,0].imshow(edge_jj_original_img)
            axs[1,0].set_title(f"P_{piece_ii}_E_{edge_ii} Extrapolated")
            axs[1,0].imshow(edge_ii_extra_img) 
            axs[0,1].set_title(f"P_{piece_ii}_E_{edge_ii} Original")
            axs[0,1].imshow(edge_ii_original_img)
            axs[1,1].set_title(f"P_{piece_jj}_E_{edge_jj} Extrapolated")
            axs[1,1].imshow(edge_jj_extra_img) 

            plt.show()

        return score_left,score_right

    def test_score_no_preprocessing_expected_high(self):
        min_excpected_score = 0.5
        score = self.test_score_no_preprocessing(piece_ii = 5,edge_ii = 1, piece_jj = 6,edge_jj = 0)
        assert score > min_excpected_score
        score = self.test_score_no_preprocessing(piece_ii = 5,edge_ii = 2,piece_jj = 3,edge_jj = 1)
        assert score > min_excpected_score

    def test_score_no_preprocessing_expected_low(self,max_excpected_score = 0.25):
        score1,score2  = self.test_score_no_preprocessing(piece_ii = 5,edge_ii = 0, piece_jj = 9,edge_jj = 1,is_plot=False)
        score = (score1+score2)/2
        assert score < max_excpected_score

        score1,score2 = self.test_score_no_preprocessing(piece_ii = 7,edge_ii = 0,piece_jj = 6,edge_jj = 1,is_plot=False)
        score = (score1+score2)/2
        assert score < max_excpected_score

    ''' WITH preprocessing '''

    def test_score_preprocessing(self,piece_ii = 5,edge_ii = 2,
                                        piece_jj = 3,edge_jj = 1,is_plot=True):
        
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0

        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()
        
        for piece in bag_of_pieces:
            piece.load_extrapolated_image()
            piece.load_stable_diffusion_original_image()

        chosen_pieces = [bag_of_pieces[piece_ii],bag_of_pieces[piece_jj]]

        original_extractor = SDOriginalExtractor(bag_of_pieces)
        original_extractor.run()
        orig_extractor_name = original_extractor.__class__.__name__
        recipe_original = image_process.RecipeFlipCropSubMean()
        original_images = [piece.features[orig_extractor_name][edge] for piece in bag_of_pieces for edge in range(piece.get_num_coords())]
        original_channels_mean = recipe_original.compute_channels_mean(original_images)
        original_img_ii = recipe_original.process(chosen_pieces[0].features[orig_extractor_name][edge_ii],
                                                  original_channels_mean)
        original_img_jj = recipe_original.process(chosen_pieces[1].features[orig_extractor_name][edge_jj],
                                                  original_channels_mean)

        extrapolation_extractor = SDExtrapolatorExtractor(bag_of_pieces)
        extrapolation_extractor.run()
        extra_extractor_name = extrapolation_extractor.__class__.__name__
        recipe_extra = image_process.RecipeFlipCropSubMean(axes_flipped=())
        extra_img_ii = recipe_extra.process(chosen_pieces[0].features[extra_extractor_name][edge_ii],
                                            original_channels_mean)
        extra_img_jj = recipe_extra.process(chosen_pieces[1].features[extra_extractor_name][edge_jj],
                                            original_channels_mean)

        pictorial_matcher = DotProductExtraToOriginalMatcher(bag_of_pieces,extra_extractor_name,orig_extractor_name) # None because it does not matter.
        score_left = pictorial_matcher._score_pair(extra_img_ii,original_img_jj)
        score_right = pictorial_matcher._score_pair(extra_img_jj,original_img_ii)

        if is_plot:
            fig, axs = plt.subplots(2,2)
            fig.suptitle(f"Left col score: {score_left}; Right col score: {score_right}\nThe images plotted before the processing")
            
            axs[0,0].set_title(f"P_{piece_jj}_E_{edge_jj} Original")
            axs[0,0].imshow(chosen_pieces[1].features[orig_extractor_name][edge_jj].astype(np.int))
            axs[1,0].set_title(f"P_{piece_ii}_E_{edge_ii} Extrapolated")
            axs[1,0].imshow(chosen_pieces[0].features[extra_extractor_name][edge_ii].astype(np.int)) 
            axs[0,1].set_title(f"P_{piece_ii}_E_{edge_ii} Original")
            axs[0,1].imshow(chosen_pieces[0].features[orig_extractor_name][edge_ii].astype(np.int))
            axs[1,1].set_title(f"P_{piece_jj}_E_{edge_jj} Extrapolated")
            axs[1,1].imshow(chosen_pieces[1].features[extra_extractor_name][edge_jj].astype(np.int)) 

            plt.show()

        return score_left,score_left
    
    def test_score_preprocessing_expected_high(self,min_excpected_score = 0.2):
        score1,score2 = self.test_score_preprocessing(piece_ii = 5,edge_ii = 1, piece_jj = 6,edge_jj = 0,is_plot=False)
        score = (score1+score2)/2
        assert score > min_excpected_score

        score1,score2 = self.test_score_preprocessing(piece_ii = 5,edge_ii = 2,piece_jj = 3,edge_jj = 1,is_plot=False)
        score = (score1+score2)/2
        assert score > min_excpected_score

    def test_score_preprocessing_expected_low(self,max_excpected_score = 0.25):
        score1,score2 = self.test_score_preprocessing(piece_ii = 5,edge_ii = 0, piece_jj = 9,edge_jj = 1,is_plot=False)
        score = (score1+score2)/2
        assert score < max_excpected_score

        score1,score2 = self.test_score_preprocessing(piece_ii = 7,edge_ii = 0,piece_jj = 6,edge_jj = 1,is_plot=False)
        score = (score1+score2)/2
        assert score < max_excpected_score

    ''' preprocessing_vs_preprocessing '''

    def test_no_preprocessing_vs_preprocessing(self,piece_ii = 5,edge_ii = 2,
                                                    piece_jj = 6,edge_jj = 0):
        
        preproc_score_left,preproc_score_right = self.test_score_preprocessing(piece_ii=piece_ii,piece_jj=piece_jj,edge_ii=edge_ii,edge_jj=edge_jj,is_plot=False)
        avg_preproc = (preproc_score_left+preproc_score_right)/2
        no_preproc_score_left,no_preproc_score_right = self.test_score_no_preprocessing(piece_ii=piece_ii,piece_jj=piece_jj,edge_ii=edge_ii,edge_jj=edge_jj,is_plot=False)
        avg_no_preproc = (no_preproc_score_left+no_preproc_score_right)/2

        print("Left Column:")
        print(f"\tP_{piece_jj}_E_{edge_jj} Original vs P_{piece_ii}_E_{edge_ii} Extrapolated:")
        print(f"\tpreprocessing vs NON-preprocessing:")
        print(f"\t{preproc_score_left} vs {no_preproc_score_left}")
        print("Right Column:")
        print(f"\tP_{piece_ii}_E_{edge_ii} Original vs P_{piece_jj}_E_{edge_jj} Extrapolated:")
        print(f"\tpreprocessing vs NON-preprocessing:")
        print(f"\t{preproc_score_right} vs {no_preproc_score_right}")
        print(f"Avg prerprocess:")
        print(f"\tpreprocessing vs NON-preprocessing:")
        print(f"\t{avg_preproc} vs {avg_no_preproc}")

        winner = "preprocessing"
        loser = "NON-preprossing"

        if avg_preproc < avg_no_preproc:
            tmp = winner
            winner = loser
            loser = tmp
        print(f"CONCLUSION: {winner} > {loser}")


    

    # def test_normalized_image_pair_best_buddies(self,piece_ii = 1,edge_ii = 1,
    #                                        piece_jj =5,edge_jj = 2,
    #                                        sample_height=5):
    #     db = 1
    #     puzzle_num = 19
    #     puzzle_noise_level = 0
    #     puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
    #     puzzle.load()
    #     bag_of_pieces = puzzle.get_bag_of_pieces()
    #     chosen_pieces = [bag_of_pieces[piece_ii],bag_of_pieces[piece_jj]]
        
    #     for piece in chosen_pieces:
    #         piece.load_extrapolated_image()
    #         piece.load_stable_diffusion_original_image()

    #     extrapolation_extractor = NormalizeSDExtrapolatorExtractor(chosen_pieces,extrapolation_height=sample_height)
    #     extrapolation_extractor.run()

    #     original_extractor = NormalizeSDOriginalExtractor(chosen_pieces,sampling_height=sample_height)
    #     original_extractor.run()

    #     pictorial_matcher = DotProductExtraToOriginalMatcher(chosen_pieces,
    #                                                          extrapolation_extractor.__class__.__name__,
    #                                                          original_extractor.__class__.__name__)

    #     pictorial_matcher.pairwise()

    #     edge_ii_img_extra_same = chosen_pieces[0].features[extrapolation_extractor.__class__.__name__][edge_ii]["same"]
    #     edge_ii_img_flipped = chosen_pieces[0].features[original_extractor.__class__.__name__][edge_ii]["flipped"]
    #     edge_jj_img_extra_same = chosen_pieces[1].features[extrapolation_extractor.__class__.__name__][edge_jj]["same"]
    #     edge_jj_img_flipped = chosen_pieces[1].features[original_extractor.__class__.__name__][edge_jj]["flipped"]
        
        

    #     fig, axs = plt.subplots(2,2)
    #     fig.suptitle(f"Score: {pictorial_matcher.get_score(piece_ii,edge_ii,piece_jj,edge_jj)}")
        
    #     '''VERIFY THIS PLOTTING...'''
    #     axs[0,0].set_title(f"P_{piece_jj}_E_{edge_jj} Original (FLIPPED)")
    #     axs[0,0].imshow(edge_jj_img_flipped.astype(np.int))
    #     axs[0,1].set_title(f"P_{piece_ii}_E_{edge_ii} Extrapolated (SAME)")
    #     axs[0,1].imshow(edge_ii_img_extra_same.astype(np.int)) 
    #     axs[1,0].set_title(f"P_{piece_ii}_E_{edge_ii} Original (FLIPPED)")
    #     axs[1,0].imshow(edge_ii_img_flipped.astype(np.int)) 
    #     axs[1,1].set_title(f"P_{piece_jj}_E_{edge_jj} Extrapolated (SAME)")
    #     axs[1,1].imshow(edge_jj_img_extra_same.astype(np.int))

    #     plt.show()



if __name__ == "__main__":
    unittest.main()