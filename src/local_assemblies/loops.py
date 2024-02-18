from src.mating_graphs.matching_graph import get_piece_name
from functools import reduce
from src.mating_graphs.matching_graph import MatchingGraphWrapper,_link_to_mating,INTER_PIECES_LINK_TYPE,name_node
from src.physics import assembler
from src import shared_variables
from src.data_types.mating import convert_mating_to_vertex_mating


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

        # for node in self.nodes:
        #     self.graph_wrapper_ref.assign_node(graph_name,node,self)
            
        for link in self.links:
            self.graph_wrapper_ref.assign_link(graph_name,(link[0],link[1]),self)

    def get_pieces_involved(self):
        return list(set([get_piece_name(node) for node in self.nodes]))

    def __repr__(self) -> str:
        pieces_names = sorted(self.get_pieces_involved())
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
    
    def get_physics_score(self):
        return self.physics_score
                    
    def remove_from_graph(self):
        # for node in self.nodes:
        #     self.graph_wrapper_ref.dissociate_node(self.graph_name,node,self)     
        for link in self.links:
            self.graph_wrapper_ref.dissociate_link(self.graph_name,(link[0],link[1]),self)



    def win_conficts(self):
        for link in self.links:
            att = self.graph_wrapper_ref.get_link_attributes(self.graph_name,link)

            if not att["loops"] is None:
                if len(att["loops"]) > 0:
                    att["loops"] = [self]

    def is_link_present(self,link):
        link_reversed = (link[1],link[0])
        return link in self.links or link_reversed in self.links

    def is_contained_all_pieces(self,loop):

        if isinstance(loop,Loop):
            unmutual_pieces = list(set(self.get_pieces_involved()) - set(loop.get_pieces_involved()))
            return len(unmutual_pieces)==0 
        
    
    def get_mutual_pieces(self,loop):
        
        if isinstance(loop,Loop):
            self_pieces = self.get_pieces_involved()
            loop_pieces = loop.get_pieces_involved()
            return [piece for piece in loop_pieces if piece in self_pieces]
    
    def mating_conflict(self,loop):

        if isinstance(loop,Loop):

            for self_link in self.links:
                self_attributes = self.graph_wrapper_ref.get_link_attributes(self.graph_name,self_link)

                if self_attributes["type"] != INTER_PIECES_LINK_TYPE:
                    continue

                for other_link in loop.links:
                    other_attributes = self.graph_wrapper_ref.get_link_attributes(self.graph_name,other_link)

                    if other_attributes["type"] != INTER_PIECES_LINK_TYPE:
                        continue
                    
                    # Test all permutation of two tuples

                    if self_link[0] == other_link[1] and self_link[1] != other_link[0]:
                        return (self_link,other_link)
                    
                    if self_link[1] == other_link[0] and self_link[0] != other_link[1]:
                        return (self_link,other_link)
                    
                    if self_link[0] == other_link[0] and self_link[1] != other_link[1]:
                        return (self_link,other_link)
                    
                    if self_link[1] == other_link[1] and self_link[0] != other_link[0]:
                        return (self_link,other_link)
                
            return None
                

    def get_mutual_matings(self,loop):
        self_matings = self.get_matings()
        other_matings = loop.get_matings()

        return [mating for mating in self_matings if mating in other_matings]


def create_loop_from_single(piece_id,graph_name = "filtered_adjacency_graph"):
    piece = shared_variables.puzzle.id2piece[piece_id]
    nodes = [name_node(piece_id,edge_i) for edge_i in range(piece.get_num_coords())]
    links = [(prev_node,next_node) for prev_node,next_node in zip(nodes[:-1],nodes[1:])]
    links.append((nodes[-1],nodes[0]))
    graph_wrapper = shared_variables.graph_wrapper

    return Loop(graph_wrapper,links,graph_name=graph_name)

class LoopMergeError(Exception):
    pass

class LoopMutualPiecesMergeError(LoopMergeError):
    pass


def merge(loop1:Loop,loop2:Loop):
    
    if loop1.is_contained_all_pieces(loop2) or loop2.is_contained_all_pieces(loop1):
        mess = f"The merge of loop {repr(loop1)} and {repr(loop2)} does not results in a novel piece"
        raise LoopMergeError(mess)
    
    mutual_pieces = loop1.get_mutual_pieces(loop2)
        
    if len(mutual_pieces) == 0:
        mess = f"The loops {repr(loop1)} and {repr(loop2)} don't have mutual pieces"
        raise LoopMutualPiecesMergeError(mess)
    
    problmatic_matings = loop1.mating_conflict(loop2)
    if problmatic_matings is not None:
        '''This should not happen when there is no noise'''
        mess = f"Conflict while trying to merge between loop {repr(loop1)} and loop {repr(loop2)}."+\
                f"The former loop assert the mating {repr(problmatic_matings[0])} " +\
                f"while the latter {repr(problmatic_matings[1])}"
        raise LoopMergeError(mess)
    
    mutual_matings = loop1.get_mutual_matings(loop2)
    expected_num_matings = min(loop1.level,loop2.level) + 1

    # if len(mutual_matings) < expected_num_matings:
    #     mess = f"Expected to have at least {expected_num_matings} mutual matings since "
    #     mess = mess +  f"{loop1} is {loop1.level}-loop and {loop2} is {loop2.level}-loop"
    #     raise LoopMergeError(mess)
    
    new_level = max(loop1.level,loop2.level) + 1
    new_links = list(set(loop1.links + loop2.links))
    
    # This might have side affects
    loop1.remove_from_graph()
    loop2.remove_from_graph()

    return Loop(loop1.graph_wrapper_ref,new_links,level=new_level,graph_name=loop1.graph_name)

        

