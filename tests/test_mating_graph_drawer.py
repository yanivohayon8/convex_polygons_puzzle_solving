import unittest
from src.recipes import factory as recipes_factory
from src.mating_graphs.drawer import MatchingGraphDrawer
import matplotlib.pyplot as plt

class TestGraphDrawer(unittest.TestCase):


    def test_draw_adjacency(self,noise_level = 1):
        db = "1"
        puzzle_num = "19"
        
        gd_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=0)
        gd_graph_wrapper = gd_puzzle_recipe.cook()

        noisy_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                     puzzle_noise_level=noise_level)
        noisy_graph_wrapper = noisy_puzzle_recipe.cook()

        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer.init()

        fig, axs = plt.subplots(1,2)

        drawer.draw_adjacency_graph(noisy_graph_wrapper.adjacency_graph,ax=axs[0])
        axs[0].set_title("Noised")
        drawer.draw_adjacency_graph(gd_graph_wrapper.adjacency_graph,ax=axs[1])
        axs[1].set_title("Noiseless")

        plt.show()
    
    def test_draw_filtered_adjacency(self,noise_level = 1):
        db = "1"
        puzzle_num = "19"
        
        gd_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=0)
        gd_graph_wrapper = gd_puzzle_recipe.cook()

        noisy_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                     puzzle_noise_level=noise_level)
        noisy_graph_wrapper = noisy_puzzle_recipe.cook()

        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer.init()

        fig, axs = plt.subplots(1,2)
        fig.suptitle(f"db_{db}_puzzle_{puzzle_num}_noise_level_{noise_level}")

        drawer.draw_adjacency_graph(noisy_graph_wrapper.adjacency_graph,
                                    ax=axs[0])
        axs[0].set_title("Unfiltered")
        drawer.draw_adjacency_graph(noisy_graph_wrapper.filtered_adjacency_graph,
                                    ax=axs[1])
        axs[1].set_title("Filtered")

        plt.show()

    def test_draw_ground_truth(self):
        db = "1"
        puzzle_num = 19
                
        gd_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=0)
        gd_graph_wrapper = gd_puzzle_recipe.cook()

        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer._draw_ground_truth_adjacency()
        plt.show()
    
    
    def test_draw_matching(self,noise_level = 1):
        db = "1"
        puzzle_num = "19"       
        
        gd_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=0)
        gd_graph_wrapper = gd_puzzle_recipe.cook()
        
        noisy_puzzle_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                     puzzle_noise_level=noise_level)
        noisy_graph_wrapper = noisy_puzzle_recipe.cook()

        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer.init()
        # Because we you use the normalized dot product
        min_edge_weight = -1
        max_edge_weight = 1
        drawer.draw_graph_matching(noisy_graph_wrapper,min_edge_weight=min_edge_weight,max_edge_weight=max_edge_weight)
        drawer.draw_graph_filtered_matching(noisy_graph_wrapper,min_edge_weight=min_edge_weight,max_edge_weight=max_edge_weight)

        plt.show()
        

    def test_draw_aggregate_graph(self):
        db = 1
        puzzle_num = 20 # 19
        puzzle_noise_level = 1

        gd_pairwise_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=0)
        gd_graph_wrapper = gd_pairwise_recipe.cook()
        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer.init()

        zero_loops_recipe = recipes_factory.create("ZeroLoopsAroundVertexFilteredByScore",
                                                   db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level,
                                                   pairwise_recipe_name = "SD1Pairwise")
        loops = zero_loops_recipe.cook()

        merger = recipes_factory.create("ZeroLoopsMerge",
                                        ranked_loops=loops,puzzle_num_pieces=10)
        aggregates_loops = merger.cook()
        aggregates_matings = [loop.get_as_mating_list() for loop in aggregates_loops]
        agg_graph = zero_loops_recipe.graph_wrapper.compute_aggregated_filtered_pot_graph(aggregates_matings)

        drawer.draw_filtered_pot_aggregated_graph(agg_graph)

        plt.show()

    

    def test_draw_after_merge_loop_graph(self):
        db = 1
        puzzle_num = 20 # 19
        puzzle_noise_level = 1

        gd_pairwise_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=0)
        gd_graph_wrapper = gd_pairwise_recipe.cook()
        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer.init()

        zero_loops_recipe = recipes_factory.create("ZeroLoopsAroundVertexFilteredByScore",
                                                   db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level,
                                                   pairwise_recipe_name = "SD1Pairwise")
        loops = zero_loops_recipe.cook()

        merger = recipes_factory.create("ZeroLoopsMerge",
                                        ranked_loops=loops,puzzle_num_pieces=10)
        aggregates_loops = merger.cook()
        agg_graph = zero_loops_recipe.graph_wrapper.compute_loops_graph(aggregates_loops)

        drawer.draw_loops_graph(agg_graph)

        plt.show()


    def test_draw_zero_loop_graph_19_0(self):
        db = 1
        puzzle_num = 19 # 19
        puzzle_noise_level = 0

        gd_pairwise_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=0)
        gd_graph_wrapper = gd_pairwise_recipe.cook()
        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer.init()

        fig, axs = plt.subplots(1,2)

        zero_loops_recipe = recipes_factory.create("ZeroLoopsAroundVertexFilteredByScore",
                                                   db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level,
                                                   pairwise_recipe_name = "SD1Pairwise")
        loops = zero_loops_recipe.cook(compatibility_threshold=0.38)
        zero_loops_graph = zero_loops_recipe.graph_wrapper.compute_loops_graph(loops)
        drawer.draw_loops_graph(zero_loops_graph,ax=axs[0])
        axs[0].set_title("zero_loops_graph")

        merger = recipes_factory.create("ZeroLoopsMerge",
                                        ranked_loops=loops,puzzle_num_pieces=10)
        aggregates_loops = merger.cook()
        agg_graph = zero_loops_recipe.graph_wrapper.compute_loops_graph(aggregates_loops)
        drawer.draw_loops_graph(agg_graph,ax=axs[1])
        axs[1].set_title("aggregates_loops")

        plt.show()


    def test_draw_zero_loop_graph_19_0_new_ds(self):
        db = 1
        puzzle_num = 19 # 19
        puzzle_noise_level = 1

        gd_pairwise_recipe = recipes_factory.create("SD1Pairwise",db=db,puzzle_num=puzzle_num,
                                                  puzzle_noise_level=0)
        gd_graph_wrapper = gd_pairwise_recipe.cook()
        drawer = MatchingGraphDrawer(gd_graph_wrapper)
        drawer.init()

        ax = plt.subplot()

        zero_loops_recipe = recipes_factory.create("ZeroLoopsAroundVertex",
                                                   db=db,puzzle_num=puzzle_num,puzzle_noise_level=puzzle_noise_level,
                                                   pairwise_recipe_name = "SD1Pairwise")
        zero_loops_recipe.cook()
        graph = zero_loops_recipe.graph_wrapper.filtered_adjacency_graph
        
        drawer.draw_filtered_adjacency_with_loops(graph,ax=ax)

        plt.show()


        
        

if __name__ == "__main__":
    unittest.main()