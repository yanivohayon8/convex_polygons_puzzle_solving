from typing import Any
from src.recipes import Recipe,factory as recipes_factory
from src.mating_graphs import factory as graph_factory
from src.data_structures.zero_loops import ZeroLoopKeepCycleAsIs
from src.my_http_client import HTTPClient
from src.data_structures.physical_assember import PhysicalAssembler
from src.data_structures.hierarchical_loops import get_loop_matings_as_csv
from src.data_structures.loop_merger import BasicLoopMerger,LoopMutualPiecesMergeError,LoopMergeError
from src import shared_variables



class ZeroLoopsAroundVertex(Recipe):

    def __init__(self,db,puzzle_num,puzzle_noise_level,
                 pairwise_recipe_name = "SD1Pairwise",
                 simulation_mode="silent") -> None:
        self.db = db
        self.puzzle_num = puzzle_num
        self.puzzle_noise_level = puzzle_noise_level
        self.pairwise_recipe_name = pairwise_recipe_name
        self.simulation_mode = simulation_mode
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

        self.loops_scores = [loop.physical_assemble(mode=self.simulation_mode) for loop in loops]
        self.loops_ranked = [loop for _,loop in sorted(zip(self.loops_scores,loops))]

        MAX_DERIVATIVE = 50
        scores = sorted(self.loops_scores)
        best_loops = [self.loops_ranked[0]]

        pieces_not_own_loops = [piece.id for piece in shared_variables.puzzle.bag_of_pieces]

        for ii in range(1,len(scores),1):
            if scores[ii] - scores[ii-1] > MAX_DERIVATIVE:
                break

            best_loops.append(self.loops_ranked[ii])

            for piece_id in self.loops_ranked[ii].get_pieces_invovled():
                if piece_id in pieces_not_own_loops:
                    pieces_not_own_loops.remove(piece_id)
        
        for piece_id in pieces_not_own_loops:
            lonely_loop = zero_loops_loader.create_loop_from_lonely(piece_id)
            best_loops.append(lonely_loop)

        return best_loops
    
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
                        if not lop in to_be_merged_loops:
                            to_be_merged_loops.append(lop)

                try:
                    aggregated_loop = self.merger.merge(aggregated_loop,curr_loop)
                except (LoopMutualPiecesMergeError,LoopMergeError) as e:
                    if not curr_loop in to_be_merged_loops:
                        to_be_merged_loops.append(curr_loop)
                
                if len(aggregated_loop.get_pieces_invovled()) == self.puzzle_num_pieces:
                    return aggregated_loop
            



recipes_factory.register_builder(ZeroLoopsAroundVertex.__name__,ZeroLoopsAroundVertexBuilder())
recipes_factory.register_builder(LoopsMerge.__name__,lambda ranked_loops,puzzle_num_pieces: LoopsMerge(ranked_loops,puzzle_num_pieces))