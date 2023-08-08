import networkx as nx
from src.mating import Mating
import matplotlib.pyplot as plt
import matplotlib.collections as mpc
from  matplotlib.cm import ScalarMappable
import numpy as np
import math

class MatchingGraphWrapper():

    def __init__(self,pieces,match_edges=None,match_pieces_score=None) -> None:
        self.pieces = pieces
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
        self.adjacency_graph = self.pieces_only_graph.copy()
        potential_matings = [edge for edge in self.potential_matings_graph.edges if not edge in self.pieces_only_graph]
        self.adjacency_graph.add_edges_from(potential_matings)

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
        
    

def get_piece_name(node_name:str):
    # edge_name P_4_E_2
    return node_name.split("_")[1]

def get_edge_name(node_name:str):
    # edge_name P_4_E_2
    return node_name.split("_")[-1]