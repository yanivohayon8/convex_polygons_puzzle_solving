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


class Loop():
    
    # def __init__(self,pieces_involved=None) -> None:
    #     '''
        
    #     '''
    #     self.piece2matings = {}
    #     self.pieces_involved = pieces_involved
    
    def __init__(self,piece2edge2matings={}) -> None:
        '''
        
        '''
        self.piece2edge2matings = piece2edge2matings
    

    def get_pieces_invovled(self):
        return self.piece2edge2matings.keys()

    def __repr__(self) -> str:
        # return reduce(lambda acc,x: f"P_{x}_"+acc,self.pieces_involved,"")[:-1]
        return reduce(lambda acc,x: f"{x}_"+acc,self.get_pieces_invovled(),"")[:-1]
        
    def get_mutual_pieces(self,loop):
        if isinstance(loop,Loop):
            return list(set(self.get_pieces_invovled()) & set(loop.get_pieces_invovled()))
    
    def is_contained(self,loop):
        if isinstance(loop,Loop):
            unmutual_pieces = list(set(self.get_pieces_invovled()) - set(loop.get_pieces_invovled()))
            return len(unmutual_pieces)==0 
    
    def union(self,loop,new_matings:list):
        ''' You should consider where the loops are pairing
            maybe this method belongs to the geometric solver? 
            or it belong to here just give the '''
        pass


class ZeroLoopError(Exception):
    pass

