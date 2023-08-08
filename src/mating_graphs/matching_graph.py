import networkx as nx
from src.mating import Mating
import matplotlib.pyplot as plt
import matplotlib.collections as mpc
from  matplotlib.cm import ScalarMappable
import numpy as np
import math

class MatchingGraphAndSpanTree():

    def __init__(self,pieces,match_edges=None,match_pieces_score=None) -> None:
        self.pieces = pieces
        self.match_edges = match_edges
        self.match_pieces_score = match_pieces_score
        self.matching_graph = nx.Graph()
        self.adjacency_base_graph = nx.Graph()
        self.adjacency_graph = None

    def _name_node(self,piece_name,edge_name):
        return f"P_{piece_name}_E_{edge_name}"

    def _build_matching_graph(self):
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
                        
                        self.matching_graph.add_edges_from(new_links)

    def _bulid_base_adjacency_graph(self):
        for piece in self.pieces:
            num_vertices = piece.get_num_coords()
            piece_nodes = [self._name_node(piece.id,edge_index) for edge_index in range(num_vertices)]
            self.adjacency_base_graph.add_nodes_from(piece_nodes)
            
            for prev_node,next_node in zip(piece_nodes,piece_nodes[1:]+[piece_nodes[0]]):
                self.adjacency_base_graph.add_edge(prev_node,next_node,compatibility=0)

        self.adjacency_graph = self.adjacency_base_graph.copy()
    
    def build_graph(self):
        self._build_matching_graph()
        self._bulid_base_adjacency_graph()
    
    def get_matching_graph_nodes(self):
        return list(self.matching_graph.nodes)

   
    def find_matching(self):
        self.matching =  list(nx.matching.max_weight_matching(self.matching_graph,weight="compatibility"))

        self.adjacency_graph = self.adjacency_base_graph.copy()
        self.adjacency_graph.add_edges_from(self.matching)

        matings = []

        for match in self.matching:
            piece_1 = get_piece_name(match[0])
            edge_1 = int(get_edge_name(match[0]))
            piece_2 = get_piece_name(match[1])
            edge_2 = int(get_edge_name(match[1]))
            matings.append(Mating(piece_1=piece_1,edge_1=edge_1,piece_2=piece_2,edge_2=edge_2))

        return matings



def get_piece_name(node_name:str):
    # edge_name P_4_E_2
    return node_name.split("_")[1]

def get_edge_name(node_name:str):
    # edge_name P_4_E_2
    return node_name.split("_")[-1]