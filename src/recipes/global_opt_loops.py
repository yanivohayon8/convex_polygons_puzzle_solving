from src.local_assemblies import loops as loops_local_assemblies

class UnionLoopsDeprecated():

    def __init__(self,ranked_loops:list,puzzle_num_pieces) -> None:
        self.puzzle_num_pieces = puzzle_num_pieces
        self.ranked_loops = ranked_loops

    def _union(self,to_be_union_loops:list):
        next_level_loops = []
        successfully_union = []

        for i in range(len(to_be_union_loops[:-1])):
            for j in range(len(to_be_union_loops[i+1:])):
                try:
                    new_loop = loops_local_assemblies.merge(to_be_union_loops[i],to_be_union_loops[j])
                    next_level_loops.append(new_loop)

                    if not to_be_union_loops[i] in successfully_union:
                        successfully_union.append(to_be_union_loops[i])
                    
                    if not to_be_union_loops[j] in successfully_union:
                        successfully_union.append(to_be_union_loops[j])
                
                except (loops_local_assemblies.LoopMutualPiecesMergeError,loops_local_assemblies.LoopMergeError) as e:
                    pass
        
        return next_level_loops,successfully_union

                
    def cook(self):
        levels = []
        next_level_loops,successfully_union = self._union(self.ranked_loops)
        levels.append(next_level_loops)

        while len(successfully_union) > 0:
            next_level_loops,successfully_union = self._union(next_level_loops)
            levels.append(next_level_loops)
        
        leves_ranked = []

        for lev_loops in levels:
            lev_loops_scores = [loop.physical_assemble(mode=self.simulation_mode) for loop in lev_loops]
            leves_ranked.append([loop for _,loop in sorted(zip(lev_loops_scores,lev_loops))])


        
        return levels