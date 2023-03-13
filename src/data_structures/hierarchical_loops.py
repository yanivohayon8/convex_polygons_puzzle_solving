from functools import reduce



class MatingLink():
    '''
        A relationship between two mating (match) edges
    '''

    def __init__(self, piece_1, edge_1, piece_2,edge_2) -> None:
        self.piece_1 = piece_1
        self.edge_1 = edge_1
        self.piece_2 = piece_2
        self.edge_2 = edge_2
    
    def __repr__(self) -> str:
        return f"P_{self.piece_1}_e_{self.piece_2}<--->P_{self.piece_2}_e_{self.edge_2}"


class Loop():
    
    def __init__(self,graph_path=None,mating_rels=None,nodes_adj=None,pieces_involved=None) -> None:
        self.graph_path = graph_path
        self.mating_rels = mating_rels
        self.nodes_adj = nodes_adj
        self.pieces_involved = pieces_involved
    
    def __repr__(self) -> str:
        return reduce(lambda acc,x: f"P_{x}_"+acc,self.pieces_involved,"")[:-1]
        
    
    def get_accumulated_angle(self,edges_mating_graph):
        return sum([edges_mating_graph.nodes[node]["angle"] for node in self.nodes_adj])

    def mutual_mating_rels(self,loop):
        return list(set(self.mating_rels) & set(loop.mating_rels))
    
    def union(self,loop):
        union_loop_rels = [] #self.mating_rels
        [union_loop_rels.append(rel) for rel in self.mating_rels + loop.mating_rels if rel not in union_loop_rels] 

        union_nodes_adj = []
        [union_nodes_adj.append(node) for node in self.nodes_adj + loop.nodes_adj if node not in union_nodes_adj]
        
        union_pieces_involved = []
        [union_pieces_involved.append(p) for p in self.pieces_involved + loop.pieces_involved if p not in union_pieces_involved]

        '''Is this a naive implementation?'''
        union_graph_path = []
        [union_graph_path.append(node) for node in self.graph_path + loop.graph_path]

        union_loop  = Loop(graph_path=union_graph_path,
                           mating_rels=union_loop_rels,
                           nodes_adj=union_nodes_adj,
                           pieces_involved=union_pieces_involved)

        return union_loop


class ZeroLoop(Loop):

    def __init__(self,graph_path) -> None:
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
    
        


