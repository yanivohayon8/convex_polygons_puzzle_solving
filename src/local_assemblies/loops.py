from src.mating_graphs.cycle import Cycle
from src.mating_graphs.matching_graph import get_piece_name

class Loop():

    def __init__(self,graph_nodes:list,level=0) -> None:
        self.graph_nodes = set(graph_nodes)
        self.pieces_involved = set()
        self.level = level
        self.physics_score = None
        [self.pieces_involved.add(get_piece_name(node)) for node in graph_nodes]


    
                    


