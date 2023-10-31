from src.mating_graphs.matching_graph import get_piece_name
from functools import reduce
from src.mating_graphs.matching_graph import MatchingGraphWrapper


class Loop():

    def __init__(self,graph_wrapper_ref:MatchingGraphWrapper,nodes:list,level=0,graph_name="filtered_adjacency_graph") -> None:
        '''
            graph_nodes - list of strings
        '''
        self.graph_wrapper_ref = graph_wrapper_ref
        self.graph_name = graph_name

        self.nodes = nodes
        self.pieces_involved = set()
        self.level = level
        self.physics_score = None

        for node in self.nodes:
            self.graph_wrapper_ref.update_node(graph_name,node,"local_assembly",self)

    def __repr__(self) -> str:
        pieces_names = sorted(list(set([get_piece_name(node) for node in self.nodes])))
        return reduce(lambda acc,x: f"P_{x}_"+acc,pieces_names,"")[:-1]



    
                    


