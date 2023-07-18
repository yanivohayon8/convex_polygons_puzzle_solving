from src.data_structures.hierarchical_loops import Loop

class LoopMergeError(Exception):
    pass

class BasicLoopMerger():
    
    def __init__(self) -> None:
        pass
    
    def _is_merge_valid(self,loop_1:Loop, loop_2:Loop):
        if loop_1.is_contained(loop_2) or loop_2.is_contained(loop_1):
            mess = f"The merge of loop {repr(loop_1)} and {repr(loop_2)} does not results in a novel piece"
            raise LoopMergeError(mess)

        mutual_pieces = loop_1.get_mutual_pieces(loop_2)
        mutual_availiable_matings = loop_1.get_mutual_availiable_matings(loop_2)
        
        if len(mutual_pieces) == 0 and len(mutual_availiable_matings) == 0:
            mess = f"The loops {repr(loop_1)} and {repr(loop_2)} don't have mutual pieces and potential mutual availiable matings"
            raise LoopMergeError(mess)
        
        conflict = loop_1._mating_conflict(loop_2)

        if conflict is not None:
            '''This should not happen when there is no noise'''
            mess = f"Conflict while trying to merge between loop {repr(loop_1)} and loop {repr(loop_2)}."+\
                    f"The former loop assert the mating {repr(conflict[0])} " +\
                    f"while the latter {repr(conflict[1])}"
            raise LoopMergeError(mess)

    def merge(self,loop_1:Loop, loop_2:Loop):
        try:
            self._is_merge_valid(loop_1,loop_2)

            new_loop = Loop(piece2edge2matings={},availiable_matings=[])
            loop_1_matings = loop_1.get_as_mating_list()
            loop_2_matings = loop_2.get_as_mating_list()
            total_occupied_matings = loop_1_matings+loop_2_matings

            for mating in total_occupied_matings:
                new_loop.insert_mating(mating)

            pieces_involved = []# 
            pieces_involved_with_duplicates = list(loop_1.get_pieces_invovled()) + list(loop_2.get_pieces_invovled())
            [pieces_involved.append(piece) for piece in pieces_involved_with_duplicates if piece not in pieces_involved]
            mutual_availiable_matings = loop_1.get_mutual_availiable_matings(loop_2)
            total_availiable_matings = loop_1.get_availiable_matings() +loop_2.get_availiable_matings()

            for mating in total_availiable_matings:
                if mating in mutual_availiable_matings:
                    if mating.piece_1 in pieces_involved and mating.piece_2 in pieces_involved:
                        new_loop.insert_mating(mating)
                        continue

                if mating in total_occupied_matings:
                    continue

                new_loop.insert_availiable_mating(mating)
            
            new_loop.unions_history.append((repr(loop_1),repr(loop_2)))
            return new_loop

        except LoopMergeError as e:
            print(e)
            return None
        
        
        
