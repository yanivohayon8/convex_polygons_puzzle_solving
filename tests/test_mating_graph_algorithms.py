import unittest
from src.mating_graphs import factory as graph_factory
from src.mating_graphs.algorithms import RedBlueCycleAlgo
from src.recipes import factory as recipes_factory

class TestRedBlueCycleAlgo(unittest.TestCase):

    def _bulid_graph_wrapper(self,db,puzzle_num,puzzle_noise_level,**kwargs):       
        gd_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=puzzle_noise_level,add_geo_features=["AngleLengthExtractor"],**kwargs)
        return gd_puzzle_recipe.cook()
    
    def test_puzzle_19_noise_0(self):
        db="1"
        puzzle_num = 19
        puzzle_noise_level=0

        pairwise_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level,
                                                  add_geo_features=["AngleLengthExtractor"],
                                                  compatibility_threshold=0.38)
        graph_wrapper = pairwise_recipe.cook()

        algo = RedBlueCycleAlgo(id2piece=pairwise_recipe.puzzle_recipe.puzzle.id2piece)
        graph_cycles_noise_0 = algo.compute(graph_wrapper.filtered_adjacency_graph)
        assert len(graph_cycles_noise_0) == 5


if __name__ == "__main__":
    unittest.main()