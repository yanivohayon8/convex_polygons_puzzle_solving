import unittest
from src.recipes import factory as recipes_factory
from src.recipes.zero_loops import ZeroLoopsAroundVertex
from src.mating_graphs import factory as graph_factory
from src.local_assemblies.loops import merge
from src.mating_graphs.drawer import MatchingGraphDrawer
import matplotlib.pyplot as plt


class TestZeroLoopsAroundVertex(unittest.TestCase):

    def test_SILENT_db_1_puzzle_19_noise_0(self):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0

        gd_pairwise_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=0)
        gd_graph_wrapper = gd_pairwise_recipe.cook()
        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer.init()

        noisy_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                     puzzle_noise_level=puzzle_noise_level)
        noisy_graph_wrapper = noisy_puzzle_recipe.cook()

        fig,axs = plt.subplots(1,2)

        drawer.draw_adjacency_graph(noisy_graph_wrapper.adjacency_graph,ax=axs[0])

        zero_loops_recipe = ZeroLoopsAroundVertex(db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level,
                                                pairwise_recipe_name = "SD1Pairwise")
        zero_loops = zero_loops_recipe.cook(compatibility_threshold=0.38)
        assert len(zero_loops) == 5

        graph = zero_loops_recipe.graph_wrapper.filtered_adjacency_graph
        drawer.draw_filtered_adjacency_with_loops(graph,ax=axs[1])

        fig2,ax = plt.subplots(1,1)
        loop_0_1 = merge(zero_loops[4],zero_loops[1])
        # zero_loops[1].remove_from_graph()
        # zero_loops[4].remove_from_graph()

        drawer.draw_filtered_adjacency_with_loops(graph,ax=ax)
        # loop_1_2 = merge(zero_loops[3],zero_loops[2])

        plt.show()




    
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

    def _run(self,db,puzzle_num,puzzle_noise_level,
             expected_num_zero_loops=-1,**kwargs):
        gd_pairwise_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=0)
        gd_graph_wrapper = gd_pairwise_recipe.cook()
        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer.init()

        zero_loops_recipe = ZeroLoopsAroundVertex(db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level,
                                                pairwise_recipe_name = "SD1Pairwise")
        zero_loops = zero_loops_recipe.cook(**kwargs)
        
        if expected_num_zero_loops != -1:
            assert len(zero_loops) == expected_num_zero_loops

        merger = recipes_factory.create("ZeroLoopsMerge",
                                        ranked_loops=zero_loops,puzzle_num_pieces=10)
        aggregates = merger.cook()

        graph = zero_loops_recipe.graph_wrapper.filtered_adjacency_graph
        drawer.draw_filtered_adjacency_with_loops(graph)

        plt.show()

        return aggregates,zero_loops

    def test_db_1_puzzle_19_noise_0(self):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0

        aggregates,loops = self._run(db,puzzle_num,puzzle_noise_level,
                                     expected_num_zero_loops=5,compatibility_threshold=0.38)

        assert len(aggregates) == 1
        assert len(aggregates[0].get_matings()) >= 13

        
    
    def test_db_1_puzzle_19_noise_1(self):
        # zero_loops_recipe = ZeroLoopsAroundVertex(db=1,puzzle_num=19,puzzle_noise_level=1,
        #                                         pairwise_recipe_name = "SD1Pairwise")
        # loops = zero_loops_recipe.cook()

        # puzzle_num_pieces = 10
        # merger = recipes_factory.create("ZeroLoopsMerge",
        #                                 ranked_loops=loops,puzzle_num_pieces=puzzle_num_pieces)
        # aggregates = merger.cook()
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 1

        aggregates,loops = self._run(db,puzzle_num,puzzle_noise_level,expected_num_zero_loops=5)

        assert len(aggregates) == 1
        assert len(aggregates[0].get_matings()) == 14
        assert len(aggregates[0].get_pieces_invovled()) == 10

    def test_db_1_puzzle_20_noise_0(self):
        db = 1
        puzzle_num = 20
        puzzle_noise_level = 0

        aggregates,loops = self._run(db,puzzle_num,puzzle_noise_level,expected_num_zero_loops=6)

        assert len(aggregates) == 3
    
    def test_db_1_puzzle_20_noise_1(self):
        db = 1
        puzzle_num = 20
        puzzle_noise_level = 1

        aggregates,loops = self._run(db,puzzle_num,puzzle_noise_level,expected_num_zero_loops=6)

        assert len(aggregates) == 3


if __name__ == "__main__":
    unittest.main()