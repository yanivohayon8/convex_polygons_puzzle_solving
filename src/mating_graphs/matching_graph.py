import networkx as nx
from src.mating import Mating
import matplotlib.pyplot as plt
import matplotlib.collections as mpc
from  matplotlib.cm import ScalarMappable
import numpy as np
import math

class MatchingGraphWrapper():

    def __init__(self,pieces,id2piece:dict,match_edges=None,match_pieces_score=None) -> None:
        self.pieces = pieces
        self.id2piece = id2piece
        self.match_edges = match_edges
        self.match_pieces_score = match_pieces_score
        self.potential_matings_graph = None#nx.Graph()
        self.pieces_only_graph = None#nx.Graph()
        self.adjacency_graph = None

    def _name_node(self,piece_name,edge_name):
        return f"P_{piece_name}_E_{edge_name}"

    def _build_matching_graph(self):
        self.potential_matings_graph = nx.Graph()
        num_pieces = len(self.pieces)

        for piece_i in range(num_pieces):
            piece_i_id = self.pieces[piece_i].id
            for piece_j in range(piece_i+1,num_pieces):
                piece_j_id = self.pieces[piece_j].id
                mating_edges = self.match_edges[piece_i,piece_j]
                if len(mating_edges)>0:
                    mating_edges_scores = self.match_pieces_score[piece_i,piece_j]
                    for k,mat_edge in enumerate(mating_edges):
                        new_links = []

                        for mating in mat_edge:
                            first_node = self._name_node(piece_i_id,mating[0])
                            second_node = self._name_node(piece_j_id,mating[1])
                            compatibility = mating_edges_scores[k]
                            new_links.append((first_node,second_node,{"compatibility":compatibility}))
                        
                        self.potential_matings_graph.add_edges_from(new_links)

    def _bulid_only_pieces_graph(self):
        self.pieces_only_graph = nx.Graph()

        for piece in self.pieces:
            num_vertices = piece.get_num_coords()
            piece_nodes = [self._name_node(piece.id,edge_index) for edge_index in range(num_vertices)]
            self.pieces_only_graph.add_nodes_from(piece_nodes)
            
            for prev_node,next_node in zip(piece_nodes,piece_nodes[1:]+[piece_nodes[0]]):
                self.pieces_only_graph.add_edge(prev_node,next_node,compatibility=0)
    
    def _build_adjacency_graph(self):
        self.adjacency_graph = nx.Graph()#self.pieces_only_graph.copy()
        self.adjacency_graph.add_nodes_from(self.pieces_only_graph.nodes)
        self.adjacency_graph.add_edges_from(self.pieces_only_graph.edges, type="within_piece")

        potential_matings = [edge for edge in self.potential_matings_graph.edges if not edge in self.pieces_only_graph]
        self.adjacency_graph.add_edges_from(potential_matings,type="inter_piece")

    def build_graph(self):
        self._build_matching_graph()
        self._bulid_only_pieces_graph()
        self._build_adjacency_graph()
    
    def get_matching_graph_nodes(self):
        return list(self.potential_matings_graph.nodes)

    def compute_max_weight_matching(self):
        self.matching =  list(nx.matching.max_weight_matching(self.potential_matings_graph,weight="compatibility"))

        # self.adjacency_graph = self.pieces_only_graph.copy()
        # self.adjacency_graph.add_edges_from(self.matching)

        # matings = []

        # for match in self.matching:
        #     piece_1 = get_piece_name(match[0])
        #     edge_1 = int(get_edge_name(match[0]))
        #     piece_2 = get_piece_name(match[1])
        #     edge_2 = int(get_edge_name(match[1]))
        #     matings.append(Mating(piece_1=piece_1,edge_1=edge_1,piece_2=piece_2,edge_2=edge_2))

        # return matings

    def compute_cycles(self,graph=None,max_length=-1):

        if graph is None:
            graph = self.adjacency_graph

        if max_length != -1:
            raw_cycles = nx.simple_cycles(graph,length_bound=max_length)
        else:
            raw_cycles = nx.simple_cycles(graph)
        
        return raw_cycles
        
    
    def _compute_red_blue_cycles(self, start_node, curr_node,computed_cycles:list, visited=None):
        '''
            start_node: like P_7_E_1, from where to start the search
            curr_node: the current visited node. Calling the function for the first time put edge start_node->curr_node
            computed_cycles: a list initiated outside. It will contain all the cycles
        '''
        if visited is None:
            visited = [start_node]

        if curr_node == start_node and len(visited) > 1:            
            computed_cycles.append(visited)

        curr_step_type = self.adjacency_graph[visited[-1]][curr_node]["type"]    

        for neighbor in self.adjacency_graph.neighbors(curr_node):
            if neighbor in visited and neighbor != start_node:
                continue
            
            next_step_type = self.adjacency_graph[curr_node][neighbor]["type"]
            
            if next_step_type != curr_step_type:
                self._compute_red_blue_cycles(start_node, neighbor,computed_cycles,visited + [curr_node])
    
    def compute_red_blue_360_loops(self, visited, curr_node,computed_cycles:list, 
                                   accumulated_loop_angle=0,loop_angle_error=3):
        '''
            computes zero loops around a vertex 360 degrees.
            start_node: like P_7_E_1, from where to start the search
            curr_node: the current visited node. Calling the function for the first time put edge start_node->curr_node
            computed_cycles: a list initiated outside. It will contain all the cycles
        '''
        # if visited is None:
        #     visited = [start_node]
        #     accumulated_loop_angle = 0
        
        if len(visited)==2:
            piece_name = get_piece_name(visited[-1])
            edge_index_1 = int(get_edge_name(visited[-2]))
            edge_index_2 = int(get_edge_name(visited[-1]))
            accumulated_loop_angle =  self.id2piece[piece_name].get_inner_angle(edge_index_1,edge_index_2)


        if curr_node == visited[0]: #and len(visited) > 2:            
            computed_cycles.append(visited)

        if accumulated_loop_angle > 360+loop_angle_error:
            return
        
        prev_step_type = self.adjacency_graph[visited[-1]][curr_node]["type"]

        '''
            Because we pre-sorted the edges counterclock wise,
            to find a 360 loop, we sum the angles in clockwise direction.
            Remember, for an edge of a piece, it has two adjacent edges (within the piece)
            So we select the one of the right
        '''
        if prev_step_type == "inter_piece":
            curr_piece = get_piece_name(curr_node)
            curr_edge = int(get_edge_name(curr_node))
            neighbor = self._name_node(curr_piece,(curr_edge-1)%self.id2piece[curr_piece].get_num_coords())
            self.compute_red_blue_360_loops(visited + [curr_node], neighbor,computed_cycles,
                                                accumulated_loop_angle=accumulated_loop_angle)
        elif prev_step_type == "within_piece":
            piece_name = get_piece_name(curr_node)
            edge_index_1 = int(get_edge_name(curr_node))
            edge_index_2 = int(get_edge_name(visited[-1]))
            inner_angle =  self.id2piece[piece_name].get_inner_angle(edge_index_1,edge_index_2)
            accumulated_loop_angle += inner_angle

            for neighbor in self.adjacency_graph.neighbors(curr_node):
                
                if neighbor in visited and neighbor != visited[0]:
                    continue
                
                next_step_type = self.adjacency_graph[curr_node][neighbor]["type"]
                
                if next_step_type == "inter_piece":
                    self.compute_red_blue_360_loops(visited + [curr_node], neighbor,computed_cycles,
                                                    accumulated_loop_angle=accumulated_loop_angle)

    
    def _link_to_mating(self,link):
        '''
         link - an edge in potential_matings_graph e.g ("P_7_E_1","P_9_E_0")
        '''
        piece1 = get_piece_name(link[0])
        edge1 = int(get_edge_name(link[0]))
        piece2 = get_piece_name(link[1])
        edge2 = int(get_edge_name(link[1]))
        
        return Mating(piece_1=piece1,edge_1=edge1,piece_2=piece2,edge_2=edge2)
        
    def compute_piece2potential_matings_dict(self):
        piece2potential_matings = {}

        for link in self.potential_matings_graph.edges():
            piece1 = get_piece_name(link[0])
            piece2potential_matings.setdefault(piece1,[])
            piece2 = get_piece_name(link[1])
            piece2potential_matings.setdefault(piece2,[])
            mating = self._link_to_mating(link)
            
            piece2potential_matings[piece1].append(mating)
            piece2potential_matings[piece2].append(mating)

        return piece2potential_matings



def get_piece_name(node_name:str):
    # edge_name P_4_E_2
    return node_name.split("_")[1]

def get_edge_name(node_name:str):
    # edge_name P_4_E_2
    return node_name.split("_")[-1]
