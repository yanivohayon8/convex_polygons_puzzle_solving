import unittest
from src.recipes.puzzle import loadRegularPuzzle
from src.recipes import factory as recipes_factory
from src.recipes import pairwise as pairwise_recipes

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
        puzzle_recipe = recipes_factory.create("loadRegularPuzzle",
                                                db=db,puzzle_num=puzzle_num,noise_level=puzzle_noise_level)
        puzzle_recipe.cook()
        recipe = recipes_factory.create("GeometricPairwise",puzzle=puzzle_recipe.puzzle)
        recipe.cook()
        matings = recipe.matchers["EdgeMatcher"].get_pairwise_as_list()

        assert len(matings) == 14


class TestSD1Pairwise(unittest.TestCase):

    def test_toy_example(self):
        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 0
        puzzle_recipe = recipes_factory.create("loadRegularPuzzle",
                                                db=db,puzzle_num=puzzle_num,noise_level=puzzle_noise_level)
        puzzle_recipe.cook()
        recipe = recipes_factory.create("SD1Pairwise",puzzle=puzzle_recipe.puzzle)
        recipe.cook()

        assert len(recipe.matchers.keys()) == 2

        piece = 0
        edge =0
        non_match_piece = 6
        non_match_edge = 1
        score = recipe.matchers["DotProductExtraToOriginalMatcher"].get_score(piece,edge,non_match_piece,non_match_edge)
        print(score)
        
        print("All compiled")

if __name__ == "__main__":
    unittest.main()