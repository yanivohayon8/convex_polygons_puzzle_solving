import unittest 
import numpy as np
import matplotlib.pyplot as plt
from src.recipes.puzzle import loadRegularPuzzle
from src.recipes import factory as recipes_factory
from src.feature_extraction.extrapolator.stable_diffusion import extract_and_normalize_original_mean
from src.feature_extraction import extract_features
from src.pairwise_matchers.stable_diffusion import DotProductExtraToOriginalMatcher
from src.pairwise_matchers import geometric as geo_pairwiser
from src.mating_graphs.matching_graph import MatchingGraphWrapper
from src.mating_graphs.drawer import MatchingGraphDrawer
from src.pairwise_matchers import pairwise_pieces



class TestFunction_score_pair(unittest.TestCase):

    
    ''' WITHOUT preprocessing '''

    def test_score_no_preprocessing(self,puzzle_noise_level = 0,piece_ii = 5,edge_ii = 2,
                                     piece_jj = 3,edge_jj = 1,is_plot=True):
        db = 1
        puzzle_num = 19
        bag_of_pieces = recipes_factory.create("loadRegularPuzzle",
                                                db=db,puzzle_num=puzzle_num,noise_level=puzzle_noise_level).cook()

        extra_feature = "SDExtrapolatorExtractor"
        original_feature = "SDOriginalExtractor"

        features = [original_feature,extra_feature]
        extract_features(bag_of_pieces,features)

        chosen_pieces = [bag_of_pieces[piece_ii],bag_of_pieces[piece_jj]]

        pictorial_matcher = DotProductExtraToOriginalMatcher(bag_of_pieces,
                                                             extra_feature,
                                                             original_feature)

        edge_ii_extra_img = chosen_pieces[0].features[extra_feature][edge_ii]
        edge_ii_original_img = chosen_pieces[0].features[original_feature][edge_ii]
        edge_jj_extra_img = chosen_pieces[1].features[extra_feature][edge_jj]
        edge_jj_original_img = chosen_pieces[1].features[original_feature][edge_jj]

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

    def test_score_no_preprocessing_expected_high(self,puzzle_noise_level = 0):
        min_excpected_score = 0.5
        score_left,score_right = self.test_score_no_preprocessing(puzzle_noise_level=puzzle_noise_level,piece_ii = 5,edge_ii = 1, piece_jj = 6,edge_jj = 0)
        assert (score_left+score_right)/2 > min_excpected_score
        score_left,score_right = self.test_score_no_preprocessing(puzzle_noise_level=puzzle_noise_level,piece_ii = 5,edge_ii = 2,piece_jj = 3,edge_jj = 1)
        assert (score_left+score_right)/2 > min_excpected_score

    def test_score_no_preprocessing_expected_low(self,puzzle_noise_level=0,
                                                 max_excpected_score = 0.25):
        score1,score2  = self.test_score_no_preprocessing(puzzle_noise_level=puzzle_noise_level,
                                                          piece_ii = 5,edge_ii = 0, piece_jj = 9,edge_jj = 1,is_plot=False)
        score = (score1+score2)/2
        assert score < max_excpected_score

        score1,score2 = self.test_score_no_preprocessing(puzzle_noise_level=puzzle_noise_level,
                                                         piece_ii = 7,edge_ii = 0,piece_jj = 6,edge_jj = 1,is_plot=False)
        score = (score1+score2)/2
        assert score < max_excpected_score

    ''' WITH preprocessing '''

    def test_score_preprocessing(self,puzzle_noise_level = 0,piece_ii = 5,edge_ii = 1,
                                        piece_jj = 6,edge_jj = 0,is_plot=True):
        
        db = 1
        puzzle_num = 19
        bag_of_pieces = recipes_factory.create("loadRegularPuzzle",
                                                db=db,puzzle_num=puzzle_num,noise_level=puzzle_noise_level).cook()


        orig_extractor_name = "NormalizeSDOriginalExtractor"
        extra_extractor_name = "NormalizeSDExtrapolatorExtractor"
        non_normed_origin_feature = "SDOriginalExtractor"
        non_normed_extra_feature = "SDExtrapolatorExtractor"

        extract_features(bag_of_pieces,[non_normed_origin_feature,non_normed_extra_feature])
        extract_and_normalize_original_mean(bag_of_pieces)
        
        original_img_ii = bag_of_pieces[piece_ii].features[orig_extractor_name][edge_ii]
        original_img_jj = bag_of_pieces[piece_jj].features[orig_extractor_name][edge_jj]
        extra_img_ii = bag_of_pieces[piece_ii].features[extra_extractor_name][edge_ii]
        extra_img_jj = bag_of_pieces[piece_jj].features[extra_extractor_name][edge_jj]
        non_normed_original_img_ii = bag_of_pieces[piece_ii].features[non_normed_origin_feature][edge_ii]
        non_normed_original_img_jj = bag_of_pieces[piece_jj].features[non_normed_origin_feature][edge_jj]
        non_normed_extra_img_ii = bag_of_pieces[piece_ii].features[non_normed_extra_feature][edge_ii]
        non_normed_extra_img_jj = bag_of_pieces[piece_jj].features[non_normed_extra_feature][edge_jj]

        pictorial_matcher = DotProductExtraToOriginalMatcher(bag_of_pieces,extra_extractor_name,orig_extractor_name) 
        score_left = pictorial_matcher._score_pair(extra_img_ii,original_img_jj)
        score_right = pictorial_matcher._score_pair(extra_img_jj,original_img_ii)

        if is_plot:
            fig, axs = plt.subplots(2,2)
            fig.suptitle(f"Left col score: {score_left}; Right col score: {score_right}\nThe images plotted before the processing")
            
            axs[0,0].set_title(f"P_{piece_jj}_E_{edge_jj} Original")
            axs[0,0].imshow(non_normed_original_img_jj.astype(np.int))
            axs[1,0].set_title(f"P_{piece_ii}_E_{edge_ii} Extrapolated")
            axs[1,0].imshow(non_normed_extra_img_ii.astype(np.int)) 
            axs[0,1].set_title(f"P_{piece_ii}_E_{edge_ii} Original")
            axs[0,1].imshow(non_normed_original_img_ii.astype(np.int))
            axs[1,1].set_title(f"P_{piece_jj}_E_{edge_jj} Extrapolated")
            axs[1,1].imshow(non_normed_extra_img_jj.astype(np.int)) 

            plt.show()

        return score_left,score_left
    
    def test_score_preprocessing_expected_high(self,puzzle_noise_level=0,
                                               min_excpected_score = 0.2):
        score1,score2 = self.test_score_preprocessing(puzzle_noise_level=puzzle_noise_level,
                                                      piece_ii = 5,edge_ii = 1, piece_jj = 6,edge_jj = 0,is_plot=False)
        score = (score1+score2)/2
        assert score > min_excpected_score

        score1,score2 = self.test_score_preprocessing(puzzle_noise_level=puzzle_noise_level,
                                                      piece_ii = 5,edge_ii = 2,piece_jj = 3,edge_jj = 1,is_plot=False)
        score = (score1+score2)/2
        assert score > min_excpected_score

    def test_score_preprocessing_expected_low(self,puzzle_noise_level=0,
                                              max_excpected_score = 0.25):
        score1,score2 = self.test_score_preprocessing(puzzle_noise_level=puzzle_noise_level,
                                                      piece_ii = 5,edge_ii = 0, piece_jj = 9,edge_jj = 1,is_plot=False)
        score = (score1+score2)/2
        assert score < max_excpected_score

        score1,score2 = self.test_score_preprocessing(puzzle_noise_level=puzzle_noise_level,
                                                      piece_ii = 7,edge_ii = 0,piece_jj = 6,edge_jj = 1,is_plot=False)
        score = (score1+score2)/2
        assert score < max_excpected_score

    ''' preprocessing_vs_preprocessing '''

    def test_no_preprocessing_vs_preprocessing(self,puzzle_noise_level=1,
                                               piece_ii = 5,edge_ii =1,
                                                    piece_jj = 6,edge_jj = 0):
        
        preproc_score_left,preproc_score_right = self.test_score_preprocessing(puzzle_noise_level=puzzle_noise_level,
                                                                               piece_ii=piece_ii,piece_jj=piece_jj,edge_ii=edge_ii,edge_jj=edge_jj,is_plot=False)
        avg_preproc = (preproc_score_left+preproc_score_right)/2
        no_preproc_score_left,no_preproc_score_right = self.test_score_no_preprocessing(puzzle_noise_level=puzzle_noise_level,
                                                                                        piece_ii=piece_ii,piece_jj=piece_jj,edge_ii=edge_ii,edge_jj=edge_jj,is_plot=False)
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


class TestHistogram(unittest.TestCase):
    
        
    def test_comp_histogram(self,db=1,puzzle_num=19,puzzle_noise_level=1):
        puzzle_recipe = recipes_factory.create("loadRegularPuzzle",
                                                db=db,puzzle_num=puzzle_num,noise_level=puzzle_noise_level)
        bag_of_pieces = puzzle_recipe.cook()
        
        extract_features(bag_of_pieces,["EdgeLengthExtractor"])
        extract_and_normalize_original_mean(bag_of_pieces)

        geometric_matcher = "EdgeMatcher"
        pictorial_matcher = "DotProductExtraToOriginalMatcher"
        matchers_keys = [geometric_matcher,pictorial_matcher]
        matchers = pairwise_pieces(bag_of_pieces,matchers_keys,
                        feature_extrapolator="NormalizeSDExtrapolatorExtractor",
                        feature_original="NormalizeSDOriginalExtractor",
                        confidence_interval=puzzle_recipe.puzzle.matings_max_difference+1e-3)

        potential_matings = matchers[geometric_matcher].get_pairwise_as_list()
        tn_matings = []
        fp_matings = []

        for mating in potential_matings:
            if puzzle_recipe.puzzle.is_ground_truth_mating(mating):
                tn_matings.append(mating)
            else:
                fp_matings.append(mating)

        tn_scores = [matchers[pictorial_matcher].get_score(mating.piece_1,mating.edge_1,mating.piece_2,mating.edge_2) for mating in tn_matings]
        fp_scores = [matchers[pictorial_matcher].get_score(mating.piece_1,mating.edge_1,mating.piece_2,mating.edge_2) for mating in fp_matings]

        ax = plt.subplot()
        ax.scatter(fp_scores,[0]*len(fp_scores),color="red")
        ax.scatter(tn_scores,[0]*len(tn_scores),color="blue")
        ax.set_title("Find the right threshold for comp filter")
        # ax.set_xlim(-1,1)

        # plt.show()
        return ax

    def _draw_adjacency_graph(self,db=1,puzzle_num=19,puzzle_noise_level=1):
        gd_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=0)
        gd_graph_wrapper = gd_puzzle_recipe.cook()

        noisy_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                     puzzle_noise_level=puzzle_noise_level)
        noisy_graph_wrapper = noisy_puzzle_recipe.cook()

        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer.init()

        fig, axs = plt.subplots(1,2)
        fig.suptitle(f"db_{db}_puzzle_{puzzle_num}_noise_level_{puzzle_noise_level}")

        drawer.draw_adjacency_graph(noisy_graph_wrapper.adjacency_graph,
                                    ax=axs[0])
        axs[0].set_title("Unfiltered")
        drawer.draw_adjacency_graph(noisy_graph_wrapper.filtered_adjacency_graph,
                                    ax=axs[1])
        axs[1].set_title("Filtered")

        # plt.show()
        return fig, axs


    def test_plot_as_params(self,db=1,puzzle_num=19,puzzle_noise_level=0):
        ax = self.test_comp_histogram(db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level)

        gd_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=0)
        gd_graph_wrapper = gd_puzzle_recipe.cook()

        noisy_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                     puzzle_noise_level=puzzle_noise_level)
        noisy_graph_wrapper = noisy_puzzle_recipe.cook()
        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer.init()

        fig, axs_adj = plt.subplots(1,2)
        fig.suptitle(f"db_{db}_puzzle_{puzzle_num}_noise_level_{puzzle_noise_level}")
        drawer.draw_adjacency_graph(noisy_graph_wrapper.adjacency_graph,ax=axs_adj[0])
        axs_adj[0].set_title("Unfiltered")
        drawer.draw_adjacency_graph(noisy_graph_wrapper.filtered_adjacency_graph,ax=axs_adj[1])
        axs_adj[1].set_title("Filtered")
        
        fig3,ax_matching = plt.subplots(1,1)
        # Because we you use the normalized dot product
        min_edge_weight = -1
        max_edge_weight = 1
        drawer.draw_graph_filtered_matching(noisy_graph_wrapper,ax=ax_matching,min_edge_weight=min_edge_weight,max_edge_weight=max_edge_weight)

        plt.show()

    def test_db_1_puzzle_19_noise_0(self):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        self.test_plot_as_params(db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level)
    
    def test_db_1_puzzle_19_noise_1(self):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 1
        self.test_plot_as_params(db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level)
    
    def test_db_1_puzzle_19_noise_2(self):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 2
        self.test_plot_as_params(db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level)
    
    def test_db_1_puzzle_20_noise_0(self):
        db = 1
        puzzle_num = 20
        puzzle_noise_level = 0
        self.test_plot_as_params(db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level)
    
    def test_db_1_puzzle_20_noise_1(self):
        db = 1
        puzzle_num = 20
        puzzle_noise_level = 1
        self.test_plot_as_params(db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level)
    
    def test_db_1_puzzle_20_noise_2(self):
        db = 1
        puzzle_num = 20
        puzzle_noise_level = 2
        self.test_plot_as_params(db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level)




if __name__ == "__main__":
    unittest.main()