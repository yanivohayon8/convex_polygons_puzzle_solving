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
        matchers = pairwise_recipes.GeometricPairwise(puzzle_recipe.puzzle).cook()
        matings =  matchers["EdgeMatcher"].get_pairwise_as_list()

        assert len(matings) == 14

    def test_from_factory(self):
        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 0
        puzzle_recipe = recipes_factory.create("loadRegularPuzzle",
                                                db=db,puzzle_num=puzzle_num,noise_level=puzzle_noise_level)
        puzzle_recipe.cook()
        matchers = recipes_factory.create("GeometricPairwise",puzzle=puzzle_recipe.puzzle).cook()
        matings =  matchers["EdgeMatcher"].get_pairwise_as_list()

        assert len(matings) == 14




if __name__ == "__main__":
    unittest.main()