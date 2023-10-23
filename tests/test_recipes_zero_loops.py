import unittest
from src.recipes import factory as recipes_factory
from src.recipes.zero_loops import ZeroLoopsAroundVertex # so the key would apear in the factory
from src.mating_graphs import factory as graph_factory

class TestZeroLoopsAroundVertex(unittest.TestCase):

    def test_SILENT_db_1_puzzle_19_noise_0(self):
        zero_loops_recipe = ZeroLoopsAroundVertex(db=1,puzzle_num=19,puzzle_noise_level=0,
                                                pairwise_recipe_name = "SD1Pairwise")
        zero_loops = zero_loops_recipe.cook(compatibility_threshold=0.38)

        assert len(zero_loops) == 5

    def test_IMAGED_db_1_puzzle_19_noise_0(self):
        zero_loops_recipe = ZeroLoopsAroundVertex(db=1,puzzle_num=19,puzzle_noise_level=0,
                                                pairwise_recipe_name = "SD1Pairwise",
                                                simulation_mode="imaged")
        zero_loops = zero_loops_recipe.cook(compatibility_threshold=0.38)

        assert len(zero_loops) == 5
    
    def test_db_1_puzzle_19_noise_1(self):
        zero_loops_recipe = ZeroLoopsAroundVertex(db=1,puzzle_num=19,puzzle_noise_level=1,
                                                pairwise_recipe_name = "SD1Pairwise")
        zero_loops = zero_loops_recipe.cook()

        # TODO: check the first 5 zero loops are the first 5 zero loops in the puzzle without noise


class TestLoopMerge(unittest.TestCase):

    def test_db_1_puzzle_19_noise_0(self):

        # # make sure these are the loops
        # graph_cycles = [
        #     ['P_7_E_1', 'P_7_E_2', 'P_8_E_0', 'P_8_E_1', 'P_9_E_3', 'P_9_E_0'],
        #     ['P_2_E_1', 'P_2_E_2', 'P_3_E_0', 'P_3_E_1', 'P_5_E_2', 'P_5_E_3'],
        #     ['P_3_E_1', 'P_3_E_2', 'P_4_E_0', 'P_4_E_1', 'P_6_E_2', 'P_6_E_0', 'P_5_E_1', 'P_5_E_2'],
        #     ['P_0_E_2', 'P_0_E_3', 'P_1_E_0', 'P_1_E_1', 'P_2_E_0', 'P_2_E_1', 'P_5_E_3', 'P_5_E_0'],
        #     ['P_0_E_1', 'P_0_E_2', 'P_5_E_0', 'P_5_E_1', 'P_6_E_0', 'P_6_E_1', 'P_9_E_2', 'P_9_E_3', 'P_8_E_1', 'P_8_E_2']
        # ]

        zero_loops_recipe = ZeroLoopsAroundVertex(db=1,puzzle_num=19,puzzle_noise_level=0,
                                                pairwise_recipe_name = "SD1Pairwise")
        loops = zero_loops_recipe.cook(compatibility_threshold=0.38)

        merger = recipes_factory.create("LoopsMerge",ranked_loops=loops,puzzle_num_pieces=10)
        solution = merger.cook()

        print(solution)




if __name__ == "__main__":
    unittest.main()