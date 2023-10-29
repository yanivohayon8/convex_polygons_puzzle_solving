from typing import Any
from src.recipes import Recipe,factory as recipes_factory
from src.mating_graphs import factory as graph_factory
from src.data_structures.zero_loops import ZeroLoopKeepCycleAsIs
from src.my_http_client import HTTPClient
from src.data_structures.physical_assember import PhysicalAssembler
from src.data_structures.hierarchical_loops import get_loop_matings_as_csv
from src.data_structures.loop_merger import BasicLoopMerger,LoopMutualPiecesMergeError,LoopMergeError

class silentLoopsSimulation():
    
    def __init__(self, physical_assembler:PhysicalAssembler) -> None:
        self.physical_assembler = physical_assembler

    def _send_request(self,loop,id2piece,screenshot_name):
        csv = get_loop_matings_as_csv(loop,id2piece)
        return self.physical_assembler.run(csv,screenshot_name=screenshot_name)

    def _score(self,loop,response):
        score = self.physical_assembler.score_assembly(response)
        loop.set_score(score)
        return score
    
    def simulate(self,loops:list,id2piece):      
        loops_scores = []

        for loop in loops:
            response = self._send_request(loop,id2piece,"")
            score = self._score(loop,response)  
            loops_scores.append(score)

        return loops_scores
    

class imagedLoopsSimulator(silentLoopsSimulation):
    '''
        Saves images to display after the simulation ends
    '''
    def simulate(self, loops: list, id2piece,level=None):
        
        # Because we score only after we save an image, we need to save the 
        # images of all loops and then 

        loops_scores = []

        for loop in loops:
            screenshot_name = repr(loop)

            if not level is None:
                screenshot_name = f"{level}-{screenshot_name}"

            response = self._send_request(loop,id2piece,screenshot_name)
            score = self._score(loop,response)  
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
        elif simulation_mode == "imaged":
            self.simulator = imagedLoopsSimulator(self.physical_assembler)

        self.loops_scores = []
    

    def cook(self,**kwargs):
        self.pairwise_recipe = recipes_factory.create(self.pairwise_recipe_name,db=self.db,puzzle_num=self.puzzle_num,puzzle_noise_level=self.puzzle_noise_level,**kwargs)
        graph_wrapper = self.pairwise_recipe.cook()

        id2piece = self.pairwise_recipe.puzzle_recipe.puzzle.id2piece
        algo = graph_factory.create("RedBlueCycleAlgo",id2piece=id2piece)
        cycles = algo.compute(graph_wrapper.filtered_adjacency_graph)

        piece2matings = graph_wrapper.get_piece2filtered_potential_matings()
        zero_loops_loader = ZeroLoopKeepCycleAsIs(id2piece,cycles,piece2matings)
        loops = zero_loops_loader.load()

        self.loops_scores = self.simulator.simulate(loops,id2piece)
        loops_ranked = [loop for _,loop in sorted(zip(self.loops_scores,loops))]

        return loops_ranked
    
    def get_num_piece_in_puzzle(self):
        return len(self.pairwise_recipe.puzzle_recipe.puzzle.bag_of_pieces)



class ZeroLoopsAroundVertexBuilder():

    def __call__(self,db,puzzle_num,puzzle_noise_level,
                 pairwise_recipe_name = "SD1Pairwise",simulation_mode="silent",**_ignored) -> Any:
        return ZeroLoopsAroundVertex(db,puzzle_num,puzzle_noise_level,
                                     pairwise_recipe_name=pairwise_recipe_name,simulation_mode=simulation_mode)


class LoopsMerge():

    def __init__(self,ranked_loops:list,puzzle_num_pieces) -> None:
        self.puzzle_num_pieces = puzzle_num_pieces
        self.ranked_loops = ranked_loops
        self.merger = BasicLoopMerger()

    def cook(self):
        aggregated_loop = self.ranked_loops[0]
        to_be_merged_loops = []
        
        while True:
            for i,curr_loop in enumerate(self.ranked_loops[1:]):
                queue_size = len(to_be_merged_loops)

                for _ in range(queue_size):
                    lop = to_be_merged_loops.pop(0)
                    try:
                        aggregated_loop = self.merger.merge(aggregated_loop,lop)    
                    except (LoopMutualPiecesMergeError,LoopMergeError) as e:
                        to_be_merged_loops.append(lop)

                try:
                    aggregated_loop = self.merger.merge(aggregated_loop,curr_loop)
                except (LoopMutualPiecesMergeError,LoopMergeError) as e:
                    to_be_merged_loops.append(curr_loop)
                
                if len(aggregated_loop.get_pieces_invovled()) == self.puzzle_num_pieces:
                    return aggregated_loop
            



recipes_factory.register_builder(ZeroLoopsAroundVertex.__name__,ZeroLoopsAroundVertexBuilder())
recipes_factory.register_builder(LoopsMerge.__name__,lambda ranked_loops,puzzle_num_pieces: LoopsMerge(ranked_loops,puzzle_num_pieces))