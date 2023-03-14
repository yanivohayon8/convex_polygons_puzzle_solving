from functools import reduce

class Mating():
    '''
        A relationship between two mating (match) edges
        piece_1: 
        edge_1: 
        piece_2: 
        edge_2: 

    '''
    def __init__(self,**kwargs) -> None:
        
        if "repr_string" in kwargs.keys():
            '''Look at the __repr__ function '''
            repr_splited = kwargs["repr_string"].split("_")
            self.piece_1 = repr_splited[1]
            self.edge_1 = repr_splited[3].split("<")[0]
            self.piece_2 = repr_splited[-3]
            self.edge_2 = repr_splited[-1]
        else:
        #(piece_1:str, edge_1:str, piece_2:str,edge_2:str)
            self.piece_1 = kwargs["piece_1"]
            self.edge_1 = kwargs["edge_1"]
            self.piece_2 = kwargs["piece_2"]
            self.edge_2 = kwargs["edge_2"]
    
    def __repr__(self) -> str:
        return f"P_{self.piece_1}_e_{self.piece_2}<--->P_{self.piece_2}_e_{self.edge_2}"
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Mating):
            return (self.piece_1 == __o.piece_1 and self.piece_2 == __o.piece_2 and self.edge_1==__o.edge_1 and self.edge_2==__o.edge_2\
            or self.piece_1 == __o.piece_2 and self.piece_2 == __o.piece_1 and self.edge_1==__o.edge_2 and self.edge_2==__o.edge_1)
        return False


class ZeroLoopError(Exception):
    pass

class LoopUnionConflictError(Exception):
    pass

class Loop():
    
    def __init__(self,piece2edge2matings={}) -> None:
        '''
            piece2edge2matings
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


