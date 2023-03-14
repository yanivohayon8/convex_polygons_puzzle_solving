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
        
    # def mutual_mating_rels(self,loop):
    #     return list(set(self.mating_rels) & set(loop.mating_rels))
    
    def get_mutual_pieces(self,loop):
        if isinstance(loop,Loop):
            return list(set(self.pieces_involved) & set(loop.pieces_involved))
    
    def is_contained(self,loop):
        if isinstance(loop,Loop):
            unmutual_pieces = list(set(self.pieces_involved) - set(loop.pieces_involved))
            return len(unmutual_pieces)==0 
    
    def union(self,loop,new_matings:list):
        ''' You should consider where the loops are pairing
            maybe this method belongs to the geometric solver? 
            or it belong to here just give the '''
        pass


class ZeroLoop(Loop):

    def __init__(self,graph_path) -> None:
        self.graph_path = graph_path

        edge_rels = [edge for edge in graph_path if "RELS" in edge]
        pieces_involved_with_duplicates = [elm.split("_")[1] for elm in edge_rels] #P_<NUM_PIECE>_.....
        pieces_involved_set = set(pieces_involved_with_duplicates)
        pieces_involved = []
        [pieces_involved.append(p) for p in pieces_involved_with_duplicates if p not in pieces_involved]
        
        if len(pieces_involved_set) <=2:
            raise ValueError("Loop must contain at least 3 pieces due to the convexity assumption")
        
        '''
            Since we assume the pieces are convex, in the hierchical loops they will appear only twice
        '''
        is_valid = True
        for piece_id in pieces_involved_set:
            if pieces_involved_with_duplicates.count(piece_id) != 2:
                is_valid = False
                break
        if not is_valid:
            raise ValueError("Loop is not valid, each piece must appear exactly twice. ")

        # self.traversal = traversal
        self.graph_path = graph_path 
        # self.nodes_rels = edge_rels
        self.mating_rels = edge_rels
        self.nodes_adj = [edge for edge in graph_path if "_ADJ_" in edge]
        # self.pieces_involved = pieces_involved_set
        self.pieces_involved = pieces_involved # To save counter clockwise ordering
        self.piece2matings = {}

        for edge_prev,edge_next in zip(edge_rels,edge_rels[1:] + [edge_rels[0]]):
            '''The convention of node of edge rels in the mating graph is the following:
            f"P_{piece.id}_RELS_E_{edge_index}"'''
            split_prev = edge_prev.split("_")
            piece_1 = split_prev[1]
            edge_1 = split_prev[-1]
            split_next = edge_next.split("_")
            piece_2 = split_next[1]
            edge_2 = split_next[-1]

            if piece_1 == piece_2:
                continue

            mating = Mating(piece_1,edge_1,piece_2,edge_2)
            key_1 = f"P_{piece_1}"
            self.piece2matings.setdefault(key_1,[])
            
            if mating not in self.piece2matings[key_1]:
                self.piece2matings[key_1].append(mating) 
            
            key_2 = f"P_{piece_2}"
            self.piece2matings.setdefault(key_2,[])
            if mating not in self.piece2matings[key_2]:
                self.piece2matings[key_2].append(mating)

    def get_accumulated_angle(self,edges_mating_graph):
        return sum([edges_mating_graph.nodes[node]["angle"] for node in self.nodes_adj])

    
        

class ZeroLoopError(Exception):
    pass

