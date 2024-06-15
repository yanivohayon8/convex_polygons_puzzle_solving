from src.recipes.zero_loops import ZeroLoopsAroundVertex,ZeroLoopsMerge
import matplotlib.pyplot as plt
from src.recipes import factory as recipes_factory
from src.mating_graphs.drawer import MatchingGraphDrawer
from src.data_types.assembly import Assembly
from src.physics import assembler
from src.pairwise_matchers.geometric import EdgeMatcher

'''
for factory to compile.....
'''
from src.recipes import pairwise as pairwise_factory
from src.recipes import puzzle as puzzle_factory
from src.feature_extraction import geometric
from src.pairwise_matchers import geometric
from src.feature_extraction.extrapolator import stable_diffusion
from src.pairwise_matchers import stable_diffusion
from src.pairwise_matchers import synthesis
from src.mating_graphs import cycle


def run(db,puzzle_num,puzzle_noise_level,pairwise_recipe_name,is_debug_solver=False):
    
    if is_debug_solver:
      gd_pairwise_recipe = recipes_factory.create("GeometricPairwise",db=db,puzzle_num=puzzle_num,puzzle_noise_level=0,is_load_extrapolation_data=False)
      gd_pairwise_recipe.cook()
      drawer = MatchingGraphDrawer(gd_pairwise_recipe.graph_wrapper)
      drawer.init()

      # drawer.draw_adjacency_graph(graph)
    print("\tCompute zero loops")
    zero_loops_recipe = ZeroLoopsAroundVertex(db=db,puzzle_num=puzzle_num,
                                              puzzle_noise_level=puzzle_noise_level,
                                                pairwise_recipe_name = pairwise_recipe_name)
    zero_loops = zero_loops_recipe.cook(is_debug=is_debug_solver)
    

    print("\tAggregate zero loops")
    merger = ZeroLoopsMerge(zero_loops,zero_loops_recipe.get_num_piece_in_puzzle())
    aggregates = merger.cook()

    if is_debug_solver:
      graph = zero_loops_recipe.graph_wrapper.filtered_adjacency_graph
      drawer.draw_filtered_adjacency_with_loops(graph)

    print("\tSolving conflicts")
    aggregates[0].win_conficts()
    stronger_aggregates = [aggregates[0]]

    if len(aggregates) > 1:
      for agg in aggregates[1:]:
        agg.win_conficts(stronger_loops=stronger_aggregates)
        stronger_aggregates.append(agg)


    if is_debug_solver:
      graph = zero_loops_recipe.graph_wrapper.filtered_adjacency_graph
      drawer.draw_filtered_adjacency_with_loops(graph,title="After conflicts")
      
      plt.show()

    print("\tSettle up")
    final_matings = zero_loops_recipe.graph_wrapper.get_final_matings()
    response = assembler.simulate(final_matings)
    # physical_score = assembler.score(response)
    final_solution_polygons,excluded_pieces = assembler.get_final_coordinates_as_polygons(response)
    
    return Assembly(final_solution_polygons,final_matings,excluded_pieces=excluded_pieces), zero_loops_recipe.get_puzzle()
