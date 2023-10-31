import unittest
from src.recipes import factory as recipes_factory
from src.recipes.zero_loops import ZeroLoopsAroundVertex
from src.mating_graphs import factory as graph_factory

class TestZeroLoopsAroundVertex(unittest.TestCase):

    def test_SILENT_db_1_puzzle_19_noise_0(self):
        zero_loops_recipe = ZeroLoopsAroundVertex(db=1,puzzle_num=19,puzzle_noise_level=0,
                                                pairwise_recipe_name = "SD1Pairwise")
        zero_loops = zero_loops_recipe.cook(compatibility_threshold=0.38)

        assert len(zero_loops) == 5

    
    def test_db_1_puzzle_19_noise_1(self):
        zero_loops_recipe = ZeroLoopsAroundVertex(db=1,puzzle_num=19,puzzle_noise_level=1,
                                                pairwise_recipe_name = "SD1Pairwise")
        zero_loops = zero_loops_recipe.cook()
        print(zero_loops)
        # TODO: check the first 5 zero loops are the first 5 zero loops in the puzzle without noise

    def test_IMAGED_db_1_puzzle_19_noise_0(self):
        zero_loops_recipe = ZeroLoopsAroundVertex(db=1,puzzle_num=19,puzzle_noise_level=0,
                                                pairwise_recipe_name = "SD1Pairwise",
                                                simulation_mode="imaged")
        zero_loops = zero_loops_recipe.cook(compatibility_threshold=0.38)

        assert len(zero_loops) == 5
    
    def test_IMAGED_db_1_puzzle_19_noise_1(self):
        zero_loops_recipe = ZeroLoopsAroundVertex(db=1,puzzle_num=19,puzzle_noise_level=1,
                                                pairwise_recipe_name = "SD1Pairwise",
                                                simulation_mode="imaged")
        zero_loops = zero_loops_recipe.cook()

        print("Check if the right loops exists in the folder...")


    def test_SILENT_db_1_puzzle_20_noise_0(self):
        '''
            Test a puzzle that has pieces that are not part of a zero loop (ground truth zero loops)
        '''
        db = 1
        puzzle_num = 20
        puzzle_noise_level = 0

        zero_loops_recipe = ZeroLoopsAroundVertex(db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level,
                                                pairwise_recipe_name = "SD1Pairwise")
        zero_loops = zero_loops_recipe.cook()

        assert len(zero_loops) == 6


class TestLoopMerge(unittest.TestCase):

    def test_db_1_puzzle_19_noise_0(self):
        zero_loops_recipe = ZeroLoopsAroundVertex(db=1,puzzle_num=19,puzzle_noise_level=0,
                                                pairwise_recipe_name = "SD1Pairwise")
        loops = zero_loops_recipe.cook(compatibility_threshold=0.38)
        assert len(loops) == 5

        merger = recipes_factory.create("ZeroLoopsMerge",
                                        ranked_loops=loops,puzzle_num_pieces=10)
        aggregates = merger.cook()
        assert len(aggregates) == 1
        assert len(aggregates[0].get_as_mating_list()) >= 13

    
    def test_db_1_puzzle_19_noise_1(self):
        zero_loops_recipe = ZeroLoopsAroundVertex(db=1,puzzle_num=19,puzzle_noise_level=1,
                                                pairwise_recipe_name = "SD1Pairwise")
        loops = zero_loops_recipe.cook()

        puzzle_num_pieces = 10
        merger = recipes_factory.create("ZeroLoopsMerge",
                                        ranked_loops=loops,puzzle_num_pieces=puzzle_num_pieces)
        aggregates = merger.cook()
        assert len(aggregates) == 1
        assert len(aggregates[0].get_as_mating_list()) == 14
        assert len(aggregates[0].get_pieces_invovled()) == puzzle_num_pieces

    def test_db_1_puzzle_20_noise_0(self):
        zero_loops_recipe = ZeroLoopsAroundVertex(db=1,puzzle_num=20,puzzle_noise_level=0,
                                                pairwise_recipe_name = "SD1Pairwise")
        loops = zero_loops_recipe.cook()

        merger = recipes_factory.create("ZeroLoopsMerge",
                                        ranked_loops=loops,puzzle_num_pieces=10)
        aggregates = merger.cook()
        assert len(aggregates) == 3


if __name__ == "__main__":
    unittest.main()