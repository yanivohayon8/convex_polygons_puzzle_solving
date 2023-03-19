class Mating():
    '''
        A relationship between two mating (match) edges
        piece_1: The piece id of edge 1 
        edge_1: edge 1 id 
        piece_2: The piece of edge 2
        edge_2: edge 2 id
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
        return f"P_{self.piece_1}_e_{self.edge_1}<--->P_{self.piece_2}_e_{self.edge_2}"
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Mating):
            return (self.piece_1 == __o.piece_1 and self.piece_2 == __o.piece_2 and self.edge_1==__o.edge_1 and self.edge_2==__o.edge_2\
            or self.piece_1 == __o.piece_2 and self.piece_2 == __o.piece_1 and self.edge_1==__o.edge_2 and self.edge_2==__o.edge_1)
        return False
