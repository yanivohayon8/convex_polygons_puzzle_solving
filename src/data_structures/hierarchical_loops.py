from functools import reduce
from src.data_structures import Mating


class ZeroLoopError(Exception):
    pass

class LoopUnionConflictError(Exception):
    pass

class Loop():
    
    def __init__(self,piece2edge2matings={}) -> None:
        '''
            piece2edge2matings: a dictionary of dictionaries
            piece2edge2matings keys are the pieces ids and the values are dictionaries
            that map between edge id to occupied mating (We assume there is a one to one match between edges)
        '''
        self.piece2edge2matings = piece2edge2matings
    
    def get_pieces_invovled(self):
        return self.piece2edge2matings.keys()

    def __repr__(self) -> str:
        # return reduce(lambda acc,x: f"P_{x}_"+acc,self.pieces_involved,"")[:-1]
        pieces = sorted(self.get_pieces_invovled())
        return reduce(lambda acc,x: f"{x}_"+acc,pieces,"")[:-1]
        
    def get_mutual_pieces(self,loop):
        if isinstance(loop,Loop):
            return list(set(self.get_pieces_invovled()) & set(loop.get_pieces_invovled()))
    
    def is_contained(self,loop):
        if isinstance(loop,Loop):
            unmutual_pieces = list(set(self.get_pieces_invovled()) - set(loop.get_pieces_invovled()))
            return len(unmutual_pieces)==0 
    
    def copy(self):
        return Loop(self.piece2edge2matings.copy())

    def _get_piece_matings(self,piece_id):
        return self.piece2edge2matings[piece_id]
    
    def _set_piece_matings(self,piece_id,piece_mating:dict):
        self.piece2edge2matings[piece_id] = piece_mating

    def union(self,other_loop):
        '''
            Unions between the self loop and another loop
        '''

        if not isinstance(other_loop,Loop):
            raise TypeError("other_loop variable is expected to be of type Loop")
        
        mutual_pieces = self.get_mutual_pieces(other_loop)

        if len(mutual_pieces) == 0:
            mess = f"Tried to union between loop {repr(self)} and {repr(other_loop)} but they don't have mutual pieces"
            raise LoopUnionConflictError(mess)
        
        if self.is_contained(other_loop) or other_loop.is_contained(self):
            mess = f"Tried to union between loop {repr(self)} and {repr(other_loop)} but the union does not results with a novel piece"
            raise LoopUnionConflictError(mess)


        new_loop = other_loop.copy()
        
        unmutual_pieces = self.get_pieces_invovled() - mutual_pieces

        for piece_id in unmutual_pieces:
            new_loop._set_piece_matings(piece_id,self._get_piece_matings(piece_id)) 

        for piece_id in mutual_pieces:

            self_edge2matings = self._get_piece_matings(piece_id)
            other_edge2matings = new_loop._get_piece_matings(piece_id)

            for self_edge_id in self_edge2matings.keys():

                if self_edge_id not in other_edge2matings.keys():
                    other_edge2matings[self_edge_id] = self_edge2matings[self_edge_id]
                elif not other_edge2matings[self_edge_id] == self_edge2matings[self_edge_id]:
                    mess = f"Conflict while trying to merge between loop {repr(self)} and loop {repr(other_loop)}."+\
                          f"The former loop assert the mating {repr(self_edge2matings[self_edge_id])} " +\
                            f"while the latter {repr(other_edge2matings[self_edge_id])}"
                    raise LoopUnionConflictError(mess)
                
        return new_loop

    def __eq__(self, other: object) -> bool:
        if isinstance(other,Loop):
            if not (other.is_contained(self) and self.is_contained(other)):
                return False
            
            for piece in self.get_pieces_invovled():
                self_edge2mating = self._get_piece_matings(piece)
                other_edge2mating = other._get_piece_matings(piece)

                if self_edge2mating.keys() != other_edge2mating.keys():
                    return False
                
                for edge in self_edge2mating.keys():
                    if self_edge2mating[edge]!=other_edge2mating[edge]:
                        return False
                
                return True
            
        return False

    def get_as_mating_list(self):
        matings = []
        for piece in self.piece2edge2matings.keys():
            curr_piece_matings = list(self.piece2edge2matings[piece].values())
            [matings.append(mat) for mat in curr_piece_matings if mat not in matings]
        
        return matings
                 

