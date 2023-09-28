import unittest 
import numpy as np
import matplotlib.pyplot as plt
from src.puzzle import Puzzle
from src.feature_extraction.extrapolator.stable_diffusion import SDExtrapolatorExtractor,SDOriginalExtractor,NormalizeSDOriginalExtractor,NormalizeSDExtrapolatorExtractor
from src.pairwise_matchers.stable_diffusion import DotProductExtraToOriginalMatcher

class TestStableDiffusionExtrapolators(unittest.TestCase):

    def _load_chosen_pieces(self,piece_ii,piece_jj,db = 1,puzzle_num = 19,puzzle_noise_level = 0):
        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()
        chosen_pieces = [bag_of_pieces[piece_ii],bag_of_pieces[piece_jj]]
        
        for piece in chosen_pieces:
            piece.load_extrapolated_image()
            piece.load_stable_diffusion_original_image()

        return chosen_pieces
    
    def test_score_no_preprocessing(self,piece_ii = 5,edge_ii = 1, piece_jj = 6,edge_jj = 0):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        chosen_pieces = self._load_chosen_pieces(piece_ii,piece_jj,
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
        edge_jj_original_img = chosen_pieces[1].features[original_extractor_name][edge_jj]
        score = pictorial_matcher._score_pair(edge_ii_extra_img,edge_jj_original_img)

        fig, axs = plt.subplots(2,1)
        fig.suptitle(f"Score: {score}")
        
        axs[0].set_title(f"P_{piece_jj}_E_{edge_jj} Original")
        axs[0].imshow(edge_jj_original_img)
        axs[1].set_title(f"P_{piece_ii}_E_{edge_ii} Extrapolated")
        axs[1].imshow(edge_ii_extra_img) 

        plt.show()

        return score

    def test_score_no_preprocessing_expected_high(self):
        min_excpected_score = 0.5
        score = self.test_score_no_preprocessing(piece_ii = 5,edge_ii = 1, piece_jj = 6,edge_jj = 0)
        assert score > min_excpected_score
        score = self.test_score_no_preprocessing(piece_ii = 5,edge_ii = 2,piece_jj = 3,edge_jj = 1)
        assert score > min_excpected_score

    def test_score_no_preprocessing_expected_low(self):
        max_excpected_score = 0.5
        score = self.test_score_no_preprocessing(piece_ii = 5,edge_ii = 0, piece_jj = 9,edge_jj = 1)
        assert score < max_excpected_score
        score = self.test_score_no_preprocessing(piece_ii = 7,edge_ii = 0,piece_jj = 6,edge_jj = 1)
        assert score < max_excpected_score

    def test_normalized_image_score_a_pair(self,piece_ii = 5,edge_ii = 2,
                                           piece_jj = 3,edge_jj = 1,
                                           sample_height=5):
        assert 1==0
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0

        chosen_pieces = self._load_chosen_pieces(piece_ii,piece_jj,
                                                 db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level)
        

        extrapolation_extractor = SDExtrapolatorExtractor(chosen_pieces)
        extrapolation_extractor.run()
        extrapolation_extractor_name = extrapolation_extractor.__class__.__name__

        original_extractor = SDOriginalExtractor(chosen_pieces)
        original_extractor.run()
        original_extractor_name = original_extractor.__class__.__name__

        pictorial_matcher = DotProductExtraToOriginalMatcher(chosen_pieces,
                                                             extrapolation_extractor_name,
                                                             original_extractor_name)

        edge_ii_img = chosen_pieces[0].features[extrapolation_extractor_name][edge_ii]
        edge_jj_img = chosen_pieces[1].features[extrapolation_extractor_name][edge_jj]
        score = pictorial_matcher._score_pair(edge_ii_img,edge_jj_img)

        fig, axs = plt.subplots(2,1)
        fig.suptitle(f"Score: {score}")
        
        axs[0].set_title(f"P_{piece_jj}_E_{edge_jj} Original")
        axs[0].imshow(edge_jj_img.astype(np.int))
        axs[1].set_title(f"P_{piece_ii}_E_{edge_ii} Extrapolated")
        axs[1].imshow(edge_ii_img.astype(np.int)) 

        plt.show()

    
    def test_normalized_image_pair_best_buddies(self,piece_ii = 1,edge_ii = 1,
                                           piece_jj =5,edge_jj = 2,
                                           sample_height=5):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()
        chosen_pieces = [bag_of_pieces[piece_ii],bag_of_pieces[piece_jj]]
        
        for piece in chosen_pieces:
            piece.load_extrapolated_image()
            piece.load_stable_diffusion_original_image()

        extrapolation_extractor = NormalizeSDExtrapolatorExtractor(chosen_pieces,extrapolation_height=sample_height)
        extrapolation_extractor.run()

        original_extractor = NormalizeSDOriginalExtractor(chosen_pieces,sampling_height=sample_height)
        original_extractor.run()

        pictorial_matcher = DotProductExtraToOriginalMatcher(chosen_pieces,
                                                             extrapolation_extractor.__class__.__name__,
                                                             original_extractor.__class__.__name__)

        pictorial_matcher.pairwise()

        edge_ii_img_extra_same = chosen_pieces[0].features[extrapolation_extractor.__class__.__name__][edge_ii]["same"]
        edge_ii_img_flipped = chosen_pieces[0].features[original_extractor.__class__.__name__][edge_ii]["flipped"]
        edge_jj_img_extra_same = chosen_pieces[1].features[extrapolation_extractor.__class__.__name__][edge_jj]["same"]
        edge_jj_img_flipped = chosen_pieces[1].features[original_extractor.__class__.__name__][edge_jj]["flipped"]
        
        

        fig, axs = plt.subplots(2,2)
        fig.suptitle(f"Score: {pictorial_matcher.get_score(piece_ii,edge_ii,piece_jj,edge_jj)}")
        
        '''VERIFY THIS PLOTTING...'''
        axs[0,0].set_title(f"P_{piece_jj}_E_{edge_jj} Original (FLIPPED)")
        axs[0,0].imshow(edge_jj_img_flipped.astype(np.int))
        axs[0,1].set_title(f"P_{piece_ii}_E_{edge_ii} Extrapolated (SAME)")
        axs[0,1].imshow(edge_ii_img_extra_same.astype(np.int)) 
        axs[1,0].set_title(f"P_{piece_ii}_E_{edge_ii} Original (FLIPPED)")
        axs[1,0].imshow(edge_ii_img_flipped.astype(np.int)) 
        axs[1,1].set_title(f"P_{piece_jj}_E_{edge_jj} Extrapolated (SAME)")
        axs[1,1].imshow(edge_jj_img_extra_same.astype(np.int))

        plt.show()



if __name__ == "__main__":
    unittest.main()