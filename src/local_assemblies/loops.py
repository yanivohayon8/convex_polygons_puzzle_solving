from src.mating_graphs.matching_graph import get_piece_name
from functools import reduce
from src.mating_graphs.matching_graph import MatchingGraphWrapper,_link_to_mating,INTER_PIECES_LINK_TYPE
from src.physics import assembler
from src import shared_variables
from src.mating import convert_mating_to_vertex_mating


class Loop():

    def __init__(self,graph_wrapper_ref:MatchingGraphWrapper,
                 links:list,level=0,graph_name="filtered_adjacency_graph") -> None:
        '''
            graph_nodes - list of strings
        '''
        self.graph_wrapper_ref = graph_wrapper_ref
        self.graph_name = graph_name # TODO: in future refactor, get rid of this parameter .....
        self.links = links
        self.level = level
        self.physics_score = None

        self.nodes = set()
        
        for link in self.links:
            self.nodes.add(link[0])
            self.nodes.add(link[1])

        for node in self.nodes:
            self.graph_wrapper_ref.assign_node(graph_name,node,self)

    def __repr__(self) -> str:
        pieces_names = sorted(list(set([get_piece_name(node) for node in self.nodes])))
        return reduce(lambda acc,x: f"P_{x}_"+acc,pieces_names,"")[:-1]

    def get_nodes(self):
        self.nodes = set()
        
        for link in self.links:
            self.nodes.add(link[0])
            self.nodes.add(link[1])
        
        return self.nodes

    def get_matings(self):
        matings = []

        for link in self.links:
            attributes = self.graph_wrapper_ref.get_link_attributes(self.graph_name,link)

            if attributes["type"] == INTER_PIECES_LINK_TYPE:
                matings.append(_link_to_mating(link))
            
        return matings
            
    def get_matings_as_csv(self)->str:
        matings = self.get_matings()
        id2piece = shared_variables.puzzle.id2piece
        matings_csv = reduce(lambda acc,mat: acc+convert_mating_to_vertex_mating(mat,id2piece[mat.piece_1],id2piece[mat.piece_2]),matings,"")

        return matings_csv

    def physical_assemble(self,mode="silent"):
        csv = self.get_matings_as_csv()
        screenshot_name = ""

        if mode == "imaged":
            screenshot_name = f"{self.level}-{repr(self)}"

        response = assembler.simulate(csv,screenshot_name=screenshot_name)
        self.physics_score = assembler.score(response)

        return self.physics_score
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value,Loop):
            return __value.nodes == self.nodes

        return False
                    


