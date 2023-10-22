import unittest
from src.recipes import factory as recipes_factory
from src.recipes.zero_loops import ZeroLoopsAroundVertex # so the key would apear in the factory


class TestZeroLoopsAroundVertex(unittest.TestCase):

    def test_db_1_puzzle_19_noise_0(self):
        # zero_loops_recipe = recipes_factory.create("ZeroLoopsAroundVertex",
        #                                            db=1,puzzle_num=19,puzzle_noise_level=0,
        #                                             pairwise_recipe_name = "SD1Pairwise")

        zero_loops_recipe = ZeroLoopsAroundVertex(db=1,puzzle_num=19,puzzle_noise_level=0,
                                                pairwise_recipe_name = "SD1Pairwise")
        zero_loops = zero_loops_recipe.cook(compatibility_threshold=0.38)

        assert len(zero_loops) == 5



if __name__ == "__main__":
    unittest.main()