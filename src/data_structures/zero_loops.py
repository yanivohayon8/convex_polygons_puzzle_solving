from src.data_structures.hierarchical_loops import Loop

CIRCLE_DEGREES = 360


class ZeroLoopAroundVertexLoader():

    def __init__(self,id2piece,cycles,piece2potential_matings) -> None:
        self.id2piece = id2piece
        self.cycles = cycles
        self.piece2potential_matings = piece2potential_matings
    
    def _is_valid(self,cycle,accumulated_angle_err):
        '''
                Since we assume the pieces are convex, in the hierchical loops they will appear only twice
            '''
        if not cycle.is_all_piece_occur(2):
            return False
        
        accumulated_angle = 0
        for mate in cycle.matings_chain:
            next_piece = self.id2piece[mate.piece_2]
            accumulated_angle += next_piece.features["angles"][int(mate.edge_2)]

        if abs(CIRCLE_DEGREES-accumulated_angle) > accumulated_angle_err:
            return False
        
        return True

    def load(self,accumulated_angle_err):
        '''
            Todo: compute accumulated_angle_err based on the noise
        '''

        self.zero_loops = []
        pieces_in_zero_loops = []

        for cycle in self.cycles:
            
            if not self._is_valid(cycle,accumulated_angle_err):
                continue
            
            next_loop = Loop(piece2edge2matings={},availiable_matings=[],cycle=cycle)

            for piece in cycle.get_pieces_involved():
                for mating in self.piece2potential_matings[piece]:
                    if mating in cycle.matings_chain:
                        next_loop.insert_mating(mating)
                    else:
                        next_loop.insert_availiable_mating(mating)

            for piece_id in cycle.get_pieces_involved():
                pieces_in_zero_loops.append(piece_id)
                
            self.zero_loops.append(next_loop)
        
        # for piece_id in self.piece2potential_matings.keys():

        #     if piece_id in pieces_in_zero_loops:
        #         continue

        #     loop_single_piece = Loop(piece2edge2matings={piece_id:{}},availiable_matings=[])

        #     for mat in self.piece2potential_matings[piece_id]:
        #         loop_single_piece.insert_availiable_mating(mat)

        #     self.zero_loops.append(loop_single_piece)
        
        return self.zero_loops
    
    def create_loop_from_lonely(self,piece_id):
        loop = Loop(piece2edge2matings={piece_id:{}},availiable_matings=[])

        for mat in self.piece2potential_matings[piece_id]:
            loop.insert_availiable_mating(mat)

        self.zero_loops.append(loop)

        return loop
    
class ZeroLoopKeepCycleAsIs(ZeroLoopAroundVertexLoader):

    def _is_valid(self, cycle, accumulated_angle_err):
        return True
    
    def load(self):
        return super().load(None)
    
class ZeroLoopTwoEdgesPerPiece(ZeroLoopAroundVertexLoader):

    def _is_valid(self, cycle, accumulated_angle_err):
        if not cycle.is_all_piece_occur(2):
            return False
        return True