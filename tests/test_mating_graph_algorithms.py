import unittest
from src.mating_graphs import factory as graph_factory
from src.mating_graphs.algorithms import red_blue_cycle 
from src.recipes import factory as recipes_factory

class TestRedBlueCycleAlgo(unittest.TestCase):

    def _bulid_graph_wrapper(self,db,puzzle_num,puzzle_noise_level,**kwargs):       
        recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=puzzle_noise_level,
                                                  add_geo_features=["AngleLengthExtractor"],**kwargs)
        graph_wrapper = recipe.cook()

        return graph_wrapper,recipe
    
    def test_compute_from_puzzle_19_noise_0(self):
        db = "1"
        puzzle_num = 19
        graph_wrapper,pairwise_recipe = self._bulid_graph_wrapper(db,puzzle_num,0)

        cycles = []
        visited = ["P_2_E_1"]
        visited.append("P_2_E_2")
        red_blue_cycle._compute_from(graph_wrapper.filtered_adjacency_graph,visited,"P_3_E_0",cycles)
        
        assert len(cycles) == 1
        assert cycles[0].debug_graph_cycle == ['P_2_E_1', 'P_2_E_2', 'P_3_E_0', 'P_3_E_1', 'P_5_E_2', 'P_5_E_3']

    def test_compute_from_puzzle_19_noise_1(self):
        # image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        db = "1"
        puzzle_num = 19
        graph_wrapper,pairwise_recipe = self._bulid_graph_wrapper(db,puzzle_num,1)

        cycles = []
        visited = ["P_2_E_1"]
        visited.append("P_2_E_2")
        red_blue_cycle._compute_from(graph_wrapper.filtered_adjacency_graph,visited,"P_3_E_0",cycles)
        print(cycles)

    def test_puzzle_19_noise_0(self):
        db="1"
        puzzle_num = 19

        graph_wrapper,pairwise_recipe = self._bulid_graph_wrapper(db,puzzle_num,0,
                                                    compatibility_threshold=0.38)


        cycles = red_blue_cycle.compute(graph_wrapper.filtered_adjacency_graph)
        cycles_names = [ repr(cycle) for cycle in cycles]
        cycles = [c for c,_ in zip(cycles,sorted(cycles_names))]

        assert len(cycles) == 5

    def test_puzzle_19_noise_1(self):
        db="1"
        puzzle_num = 19
        puzzle_noise_level = 1
        graph_wrapper,pairwise_recipe = self._bulid_graph_wrapper(db,puzzle_num,puzzle_noise_level)
        
        cycles = red_blue_cycle.compute(graph_wrapper.filtered_adjacency_graph)
        cycles_names = [ repr(cycle) for cycle in cycles]
        cycles = [c for c,_ in zip(cycles,sorted(cycles_names))]

        print(cycles)
    
    def test_puzzle_19(self):
        db="1"
        puzzle_num = 19

        # Because we want the test to pass set compatibility_threshold to 0.38
        # So all the ground truth links will be present.
        graph_wrapper,pairwise_recipe = self._bulid_graph_wrapper(db,puzzle_num,0,
                                                    compatibility_threshold=0.38)
        
        graph_cycles_noise_0 = red_blue_cycle.compute(graph_wrapper.filtered_adjacency_graph)
        assert len(graph_cycles_noise_0) == 5

        graph_wrapper,pairwise_recipe = self._bulid_graph_wrapper(db,puzzle_num,1)
        graph_cycles_noise_1 = red_blue_cycle.compute(graph_wrapper.filtered_adjacency_graph)

        # making sure all the cycles found in the noise 0 puzzle
        # are found also in the noised puzzle
        for cycle in graph_cycles_noise_0:
            assert cycle in graph_cycles_noise_1, f"expected cycle {cycle} was not computed"


if __name__ == "__main__":
    unittest.main()