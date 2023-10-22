from typing import Any
from src.recipes import Recipe,factory as recipes_factory
from src.mating_graphs import factory as graph_factory
from src.data_structures.zero_loops import ZeroLoopKeepCycleAsIs

class ZeroLoopsAroundVertex(Recipe):

    def __init__(self,db,puzzle_num,puzzle_noise_level,
                 pairwise_recipe_name = "SD1Pairwise",**kwargs) -> None:
        self.db = db
        self.puzzle_num = puzzle_num
        self.puzzle_noise_level = puzzle_noise_level
        self.pairwise_recipe_name = pairwise_recipe_name
    

    def cook(self,**kwargs):
        pairwise_recipe = recipes_factory.create(self.pairwise_recipe_name,db=self.db,puzzle_num=self.puzzle_num,puzzle_noise_level=self.puzzle_noise_level,**kwargs)
        graph_wrapper = pairwise_recipe.cook()

        id2piece = pairwise_recipe.puzzle_recipe.puzzle.id2piece
        algo = graph_factory.create("RedBlueCycleAlgo",id2piece=id2piece)
        cycles = algo.compute(graph_wrapper.filtered_adjacency_graph)

        piece2matings = graph_wrapper.get_piece2filtered_potential_matings()
        zero_loops_loader = ZeroLoopKeepCycleAsIs(id2piece,cycles,piece2matings)
        zero_loops = zero_loops_loader.load()

        return zero_loops



class ZeroLoopsAroundVertexBuilder():

    def __call__(self,db,puzzle_num,puzzle_noise_level,
                 pairwise_recipe_name = "SD1Pairwise",**_ignored) -> Any:
        return ZeroLoopsAroundVertex(db,puzzle_num,puzzle_noise_level,
                                     pairwise_recipe_name=pairwise_recipe_name)
    

recipes_factory.register_builder(ZeroLoopsAroundVertex.__name__,ZeroLoopsAroundVertexBuilder())