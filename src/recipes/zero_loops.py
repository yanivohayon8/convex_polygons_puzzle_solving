from typing import Any
from src.recipes import Recipe,factory as recipes_factory
from src.mating_graphs import factory as graph_factory
from src.data_structures.zero_loops import ZeroLoopKeepCycleAsIs
from functools import reduce
from src.mating import convert_mating_to_vertex_mating
from src.my_http_client import HTTPClient
from src.data_structures.physical_assember import PhysicalAssembler
from src.data_structures.hierarchical_loops import get_loop_matings_as_csv

class silentLoopsSimulation():
    
    def __init__(self, physical_assembler:PhysicalAssembler) -> None:
        self.physical_assembler = physical_assembler
        self.next_screen_shot_name = ""

    def simulate(self,loops:list,id2piece):      
        loops_scores = []

        for i,loop in enumerate(loops):
            csv = get_loop_matings_as_csv(loop,id2piece)
            response = self.physical_assembler.run(csv,screenshot_name=self.next_screen_shot_name)
            score = self.physical_assembler.score_assembly(response)
            loop.set_score(score)
            loops_scores.append(score)

        return loops_scores

class ZeroLoopsAroundVertex(Recipe):

    def __init__(self,db,puzzle_num,puzzle_noise_level,
                 pairwise_recipe_name = "SD1Pairwise",
                 simulation_mode="silent") -> None:
        self.db = db
        self.puzzle_num = puzzle_num
        self.puzzle_noise_level = puzzle_noise_level
        self.pairwise_recipe_name = pairwise_recipe_name
        
        self.http = HTTPClient(self.db,self.puzzle_num,self.puzzle_noise_level)
        self.physical_assembler = PhysicalAssembler(self.http)

        if simulation_mode == "silent":
            self.simulator = silentLoopsSimulation(self.physical_assembler)

        self.loops_scores = []
    

    def cook(self,**kwargs):
        pairwise_recipe = recipes_factory.create(self.pairwise_recipe_name,db=self.db,puzzle_num=self.puzzle_num,puzzle_noise_level=self.puzzle_noise_level,**kwargs)
        graph_wrapper = pairwise_recipe.cook()

        id2piece = pairwise_recipe.puzzle_recipe.puzzle.id2piece
        algo = graph_factory.create("RedBlueCycleAlgo",id2piece=id2piece)
        cycles = algo.compute(graph_wrapper.filtered_adjacency_graph)

        piece2matings = graph_wrapper.get_piece2filtered_potential_matings()
        zero_loops_loader = ZeroLoopKeepCycleAsIs(id2piece,cycles,piece2matings)
        loops = zero_loops_loader.load()

        self.loops_scores = self.simulator.simulate(loops,id2piece)
        loops_ranked = [loop for _,loop in sorted(zip(self.loops_scores,loops))]

        return loops_ranked



class ZeroLoopsAroundVertexBuilder():

    def __call__(self,db,puzzle_num,puzzle_noise_level,
                 pairwise_recipe_name = "SD1Pairwise",simulation_mode="silent",**_ignored) -> Any:
        return ZeroLoopsAroundVertex(db,puzzle_num,puzzle_noise_level,
                                     pairwise_recipe_name=pairwise_recipe_name,simulation_mode=simulation_mode)
    

recipes_factory.register_builder(ZeroLoopsAroundVertex.__name__,ZeroLoopsAroundVertexBuilder())