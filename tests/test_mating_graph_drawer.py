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


    def test_draw_adjacency(self):
        db = "1"
        puzzle_num = "19"
        
        gd_puzzle_recipe = recipes_factory.create("loadRegularPuzzle",
                                                db=db,puzzle_num=puzzle_num,noise_level=0)
        gd_puzzle_recipe.cook()
        gd_recipe = recipes_factory.create("SD1Pairwise",puzzle=gd_puzzle_recipe.puzzle)
        gd_graph_wrapper = gd_recipe.cook()

        noise_level = 1
        noisy_puzzle_recipe = recipes_factory.create("loadRegularPuzzle",
                                                db=db,puzzle_num=puzzle_num,noise_level=noise_level)
        noisy_puzzle_recipe.cook()
        noisy_recipe = recipes_factory.create("SD1Pairwise",puzzle=noisy_puzzle_recipe.puzzle)
        noisy_graph_wrapper = noisy_recipe.cook()

        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer.init()

        fig, axs = plt.subplots(1,2)

        drawer.draw_adjacency_graph(noisy_graph_wrapper,ax=axs[0])
        axs[0].set_title("Noised")
        drawer.draw_adjacency_graph(gd_graph_wrapper,ax=axs[1])
        axs[1].set_title("Noiseless")

        plt.show()

    def test_draw_ground_truth(self):
        db = "1"
        puzzle_num = 19
        gd_noise_level = 0
        
        gd_puzzle_recipe = recipes_factory.create("loadRegularPuzzle",
                                                db=db,puzzle_num=puzzle_num,noise_level=gd_noise_level)
        gd_puzzle_recipe.cook()
        gd_recipe = recipes_factory.create("SD1Pairwise",puzzle=gd_puzzle_recipe.puzzle)
        gd_graph_wrapper = gd_recipe.cook()

        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer._draw_ground_truth_adjacency()
        plt.show()
    
    
    def test_draw_matching(self):
        db = "1"
        puzzle_num = "19"
        gd_noise_level = 0
        
        gd_puzzle_recipe = recipes_factory.create("loadRegularPuzzle",
                                                db=db,puzzle_num=puzzle_num,noise_level=gd_noise_level)
        gd_puzzle_recipe.cook()
        gd_recipe = recipes_factory.create("SD1Pairwise",puzzle=gd_puzzle_recipe.puzzle)
        gd_graph_wrapper = gd_recipe.cook()

        noise_level = 1
        noisy_puzzle_recipe = recipes_factory.create("loadRegularPuzzle",
                                                db=db,puzzle_num=puzzle_num,noise_level=noise_level)
        noisy_puzzle_recipe.cook()
        noisy_recipe = recipes_factory.create("SD1Pairwise",puzzle=noisy_puzzle_recipe.puzzle)
        noisy_graph_wrapper = noisy_recipe.cook()

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