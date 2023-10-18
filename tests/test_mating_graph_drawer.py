import unittest
from src.recipes.puzzle import loadRegularPuzzle
from src.recipes import factory as recipes_factory
from src.mating_graphs.matching_graph import MatchingGraphWrapper
from src.mating_graphs.drawer import MatchingGraphDrawer
import matplotlib.pyplot as plt
from src.pairwise_matchers.stable_diffusion import DotProductExtraToOriginalMatcher
from src.pairwise_matchers.geometric import EdgeMatcher
from src.feature_extraction import extract_features
# from src.feature_extraction.extrapolator.stable_diffusion import NormalizeSDExtrapolatorExtractor,NormalizeSDOriginalExtractor
# from src.feature_extraction import geometric as geo_extractor 
# from src.pairwise_matchers import geometric as geo_pairwiser

class TestGraphDrawer(unittest.TestCase):


    def test_draw_adjacency(self,noise_level = 1):
        db = "1"
        puzzle_num = "19"
        
        gd_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=0)
        gd_graph_wrapper = gd_puzzle_recipe.cook()

        noisy_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                     puzzle_noise_level=noise_level)
        noisy_graph_wrapper = noisy_puzzle_recipe.cook()

        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer.init()

        fig, axs = plt.subplots(1,2)

        drawer.draw_adjacency_graph(noisy_graph_wrapper.adjacency_graph,ax=axs[0])
        axs[0].set_title("Noised")
        drawer.draw_adjacency_graph(gd_graph_wrapper.adjacency_graph,ax=axs[1])
        axs[1].set_title("Noiseless")

        plt.show()
    
    def test_draw_filtered_adjacency(self,noise_level = 1):
        db = "1"
        puzzle_num = "19"
        
        gd_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=0)
        gd_graph_wrapper = gd_puzzle_recipe.cook()

        noisy_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                     puzzle_noise_level=noise_level)
        noisy_graph_wrapper = noisy_puzzle_recipe.cook()

        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer.init()

        fig, axs = plt.subplots(1,2)
        fig.suptitle(f"db_{db}_puzzle_{puzzle_num}_noise_level_{noise_level}")

        drawer.draw_adjacency_graph(noisy_graph_wrapper.adjacency_graph,
                                    ax=axs[0])
        axs[0].set_title("Unfiltered")
        drawer.draw_adjacency_graph(noisy_graph_wrapper.filtered_adjaceny_graph,
                                    ax=axs[1])
        axs[1].set_title("Filtered")

        plt.show()

    def test_draw_ground_truth(self):
        db = "1"
        puzzle_num = 19
                
        gd_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=0)
        gd_graph_wrapper = gd_puzzle_recipe.cook()

        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer._draw_ground_truth_adjacency()
        plt.show()
    
    
    def test_draw_matching(self,noise_level = 1):
        db = "1"
        puzzle_num = "19"       
        
        gd_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=0)
        gd_graph_wrapper = gd_puzzle_recipe.cook()
        
        noisy_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                     puzzle_noise_level=noise_level)
        noisy_graph_wrapper = noisy_puzzle_recipe.cook()

        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer.init()
        # Because we you use the normalized dot product
        min_edge_weight = -1
        max_edge_weight = 1
        drawer.draw_graph_matching(noisy_graph_wrapper,min_edge_weight=min_edge_weight,max_edge_weight=max_edge_weight)
        drawer.draw_graph_filtered_matching(noisy_graph_wrapper,min_edge_weight=min_edge_weight,max_edge_weight=max_edge_weight)

        plt.show()
        




        
        

if __name__ == "__main__":
    unittest.main()