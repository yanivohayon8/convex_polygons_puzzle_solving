import unittest 
from src.recipes import global_opt_loops
from src.recipes import factory as recipes_factory
from src.recipes.zero_loops import ZeroLoopsAroundVertex
from src.mating_graphs.drawer import MatchingGraphDrawer

class TestUnion(unittest.TestCase):

    def test_toy_example(self):

        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 1

        gd_pairwise_recipe = recipes_factory.create("SyntheticPairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=0)
        gd_graph_wrapper = gd_pairwise_recipe.cook()
        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer.init()

        zero_loops_recipe = ZeroLoopsAroundVertex(db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level,
                                                pairwise_recipe_name = "SyntheticPairwise")
        zero_loops = zero_loops_recipe.cook()


        union = global_opt_loops.UnionLoopsDeprecated(zero_loops,zero_loops_recipe.get_num_piece_in_puzzle())
        union.cook()



if  __name__ == "__main__":
    unittest.main()