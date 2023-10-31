from typing import Any
from src.recipes import Recipe,factory as recipes_factory
from src.mating_graphs import factory as graph_factory
from src.data_structures.zero_loops import ZeroLoopKeepCycleAsIs
from src.data_structures.loop_merger import BasicLoopMerger,LoopMutualPiecesMergeError,LoopMergeError
from src import shared_variables
from src.local_assemblies.loops import Loop,create_loop_from_single
from src.mating_graphs.algorithms import red_blue_cycle

MAX_DERIVATIVE = 50

class ZeroLoopsAroundVertex(Recipe):

    def __init__(self,db,puzzle_num,puzzle_noise_level,
                 pairwise_recipe_name = "SD1Pairwise",
                 simulation_mode="silent",max_derivative= MAX_DERIVATIVE) -> None:
        self.db = db
        self.puzzle_num = puzzle_num
        self.puzzle_noise_level = puzzle_noise_level
        self.pairwise_recipe_name = pairwise_recipe_name
        self.simulation_mode = simulation_mode
        self.loops_scores = []
        self.max_derivative = max_derivative
    
    def _compute_graph_wrapper(self,**kwargs):
        self.pairwise_recipe = recipes_factory.create(self.pairwise_recipe_name,db=self.db,puzzle_num=self.puzzle_num,puzzle_noise_level=self.puzzle_noise_level,**kwargs)
        self.graph_wrapper = self.pairwise_recipe.cook()

    def _compute_loops_from_cycles(self,**kwargs):
        cycles = red_blue_cycle.compute(self.graph_wrapper.filtered_adjacency_graph)
        loops = [Loop(self.graph_wrapper,cycle.debug_graph_links) for cycle in cycles]
        return loops
    
    def _rank_loops(self,loops,**kwargs):
        self.loops_scores = [loop.physical_assemble(mode=self.simulation_mode) for loop in loops]
        self.loops_ranked = [loop for _,loop in sorted(zip(self.loops_scores,loops))]

    def _filter_best(self):
        self.best_loops = [self.loops_ranked[0]]
        
        for ii in range(1,len(self.loops_ranked),1):
            curr_score = self.loops_ranked[ii].get_physics_score()
            prev_score = self.loops_ranked[ii-1].get_physics_score()

            if curr_score - prev_score > self.max_derivative:
                break

            self.best_loops.append(self.loops_ranked[ii])

        return self.best_loops

    def _create_lonely_loops(self):
        pieces_not_own_loops = [piece.id for piece in shared_variables.puzzle.bag_of_pieces]
        [pieces_not_own_loops.remove(piece_id) for loop in self.best_loops for piece_id in loop.get_pieces_involved() if piece_id in pieces_not_own_loops]
                    
        for piece_id in pieces_not_own_loops:
            loop = create_loop_from_single(piece_id)
            self.best_loops.append(loop)
        
        return self.best_loops

    def cook(self,**kwargs):
        self._compute_graph_wrapper(**kwargs)
        loops = self._compute_loops_from_cycles(**kwargs)
        self._rank_loops(loops)
        self._filter_best()
        self._create_lonely_loops()        

        return self.best_loops
    
    def get_num_piece_in_puzzle(self):
        return len(self.pairwise_recipe.puzzle_recipe.puzzle.bag_of_pieces)



class ZeroLoopsAroundVertexBuilder():

    def __call__(self,db,puzzle_num,puzzle_noise_level,
                 pairwise_recipe_name = "SD1Pairwise",simulation_mode="silent",max_derivative= MAX_DERIVATIVE,**_ignored) -> Any:
        return ZeroLoopsAroundVertex(db,puzzle_num,puzzle_noise_level,
                                     pairwise_recipe_name=pairwise_recipe_name,
                                     simulation_mode=simulation_mode,max_derivative=max_derivative)




class ZeroLoopsMerge():

    def __init__(self,ranked_loops:list,puzzle_num_pieces) -> None:
        self.puzzle_num_pieces = puzzle_num_pieces
        self.ranked_loops = ranked_loops
        self.merger = BasicLoopMerger()

    def _merge(self,to_be_merge_loops:list):
        aggregated_loop = to_be_merge_loops[0]
        queued_loops = []
        is_changed = True
        
        while is_changed:
            is_changed = False

            for i,curr_loop in enumerate(to_be_merge_loops[1:]):
                queue_size = len(queued_loops)

                for _ in range(queue_size):
                    lop = queued_loops.pop(0)
                    try:
                        aggregated_loop = self.merger.merge(aggregated_loop,lop)    
                        is_changed = True
                        to_be_merge_loops.remove(lop)
                    except (LoopMutualPiecesMergeError,LoopMergeError) as e:
                        if not lop in queued_loops:
                            queued_loops.append(lop)

                try:
                    aggregated_loop = self.merger.merge(aggregated_loop,curr_loop)
                    is_changed = True
                    to_be_merge_loops.remove(curr_loop)
                except (LoopMutualPiecesMergeError,LoopMergeError) as e:
                    if not curr_loop in queued_loops:
                        queued_loops.append(curr_loop)
                
                if len(aggregated_loop.get_pieces_invovled()) == self.puzzle_num_pieces:
                    return aggregated_loop,list() #queued_loops
        
        return aggregated_loop,queued_loops
                
    def cook(self):
        aggregated_loop,queued_loops = self._merge(self.ranked_loops)
        aggregates = [aggregated_loop]

        while len(queued_loops) > 0:
            aggregated_loop,queued_loops = self._merge(queued_loops)
            aggregates.append(aggregated_loop)
        
        return aggregates
            



recipes_factory.register_builder(ZeroLoopsAroundVertex.__name__,ZeroLoopsAroundVertexBuilder())
recipes_factory.register_builder(ZeroLoopsMerge.__name__,lambda ranked_loops,puzzle_num_pieces: ZeroLoopsMerge(ranked_loops,puzzle_num_pieces))