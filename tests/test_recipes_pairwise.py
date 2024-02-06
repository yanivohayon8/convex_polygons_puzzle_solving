import unittest
from src.recipes.puzzle import loadRegularPuzzle
from src.recipes import factory as recipes_factory
from src.recipes import pairwise as pairwise_recipes
from src.mating_graphs.drawer import MatchingGraphDrawer
import matplotlib.pyplot as plt


class TestGeometricPairwise(unittest.TestCase):

    def test_toy_example(self):
        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 0
        puzzle_recipe = recipes_factory.create("loadRegularPuzzle",
                                                db=db,puzzle_num=puzzle_num,noise_level=puzzle_noise_level)
        puzzle_recipe.cook()
        recipe = pairwise_recipes.GeometricPairwise(puzzle_recipe.puzzle)
        recipe.cook()
        matings = recipe.matchers["EdgeMatcher"].get_pairwise_as_list()

        assert len(matings) == 14

    def test_from_factory(self):
        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 0
        
        recipe = recipes_factory.create("GeometricPairwise",
                                        db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level)
        recipe.cook()
        matings = recipe.matchers["EdgeMatcher"].get_pairwise_as_list()

        assert len(matings) == 14


class TestSD1Pairwise(unittest.TestCase):

    def test_toy_example(self):
        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 0
        
        recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                        puzzle_noise_level=puzzle_noise_level)
        recipe.cook()

        assert len(recipe.matchers.keys()) == 2

        piece = 0
        edge =0
        non_match_piece = 6
        non_match_edge = 1
        score = recipe.matchers["DotProductExtraToOriginalMatcher"].get_score(piece,edge,non_match_piece,non_match_edge)
        print(score)
        
        print("All compiled")


class TestSynthesisPairwise(unittest.TestCase):

    def test_toy_example(self):
        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 1
        
        recipe = recipes_factory.create("SyntheticPairwise",db=db,puzzle_num=puzzle_num,
                                        puzzle_noise_level=0)
        gd_graph_wrapper = recipe.cook()
        
        recipe = recipes_factory.create("SyntheticPairwise",db=db,puzzle_num=puzzle_num,
                                        puzzle_noise_level=puzzle_noise_level)
        graph_wrapper = recipe.cook()

        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer.init()
        # Because we you use the normalized dot product
        min_edge_weight = -1
        max_edge_weight = 1
        drawer.draw_graph_filtered_matching(graph_wrapper,
                                   min_edge_weight=min_edge_weight,
                                   max_edge_weight=max_edge_weight)
        drawer.draw_graph_matching(graph_wrapper,
                                   min_edge_weight=min_edge_weight,
                                   max_edge_weight=max_edge_weight)

        plt.show()

        print("compiled")
    

    def test_1_staged_db(self):
        db = "1_staged"
        puzzle_num = "12"
        puzzle_noise_level = 1
        
        recipe = recipes_factory.create("SyntheticPairwise",db=db,puzzle_num=puzzle_num,
                                        puzzle_noise_level=0)
        gd_graph_wrapper = recipe.cook()
        
        recipe = recipes_factory.create("SyntheticPairwise",db=db,puzzle_num=puzzle_num,
                                        puzzle_noise_level=puzzle_noise_level)
        graph_wrapper = recipe.cook()

        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer.init()
        # Because we you use the normalized dot product
        min_edge_weight = -1
        max_edge_weight = 1
        drawer.draw_graph_filtered_matching(graph_wrapper,
                                   min_edge_weight=min_edge_weight,
                                   max_edge_weight=max_edge_weight)
        drawer.draw_graph_matching(graph_wrapper,
                                   min_edge_weight=min_edge_weight,
                                   max_edge_weight=max_edge_weight)

        plt.show()

        print("compiled")

if __name__ == "__main__":
    unittest.main()