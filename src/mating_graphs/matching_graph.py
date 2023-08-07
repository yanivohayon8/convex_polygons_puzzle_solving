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

    # def _pos_by_layout(self,graph,layout):
    #     layouts = {
    #         "spring": nx.spring_layout,
    #         "spectral": nx.spectral_layout,
    #         "random": nx.random_layout,
    #         "circular": nx.circular_layout,
    #         "shell":nx.shell_layout,
    #         "rescale":nx.rescale_layout,
    #         "spiral":nx.spiral_layout,
    #         "kamada_kawai": nx.kamada_kawai_layout,
    #         "planar":nx.planar_layout,
    #         "piece_clustered":None
    #         # "multipartite":nx.multipartite_layout
    #         #"multipartite": nx.multipartite_layout
    #         # Add more layout options as needed
    #     }

    #     if layout not in layouts:
    #         raise ValueError(f"Invalid layout option. Choose one of: {', '.join(layouts.keys())}")
        
    #     if layout == "piece_clustered":
    #         pos = self._pos_nodes_by_pieces(graph)
    #     elif layout == "spring":
    #         num_nodes = len(list(graph.nodes))
    #         pos = nx.spring_layout(graph,k=4/np.sqrt(num_nodes))
    #     else:
    #         pos = layouts[layout](graph)
        
    #     return pos

    # def _pos_nodes_by_pieces(self,graph):
        
    #     # Create a dictionary to store the clusters (pieces) of nodes
    #     clusters = {}

    #     for node in graph.nodes():
    #         if node.startswith("P_"):
    #             piece_number = node.split("_")[1]
    #             if piece_number not in clusters:
    #                 clusters[piece_number] = []
    #             clusters[piece_number].append(node)

    #     # Calculate the number of clusters and assign them to different positions
    #     num_clusters = len(clusters)
    #     positions = nx.spring_layout(graph, k=10, seed=42) #k=0.1

    #     cluster_positions = {}
    #     for idx, cluster in enumerate(clusters.values()):
    #         angle = 2 * idx * 3.14 / num_clusters
    #         for node in cluster:
    #             x, y = positions[node]
    #             x_new = x * 0.1 * num_clusters + 0.9 * num_clusters * math.cos(angle)
    #             y_new = y * 0.1 * num_clusters + 0.9 * num_clusters * math.sin(angle)
    #             cluster_positions[node] = (x_new, y_new)

    #     return cluster_positions

    # def _draw_general_layout(self,graph,layout="spectral",title="Graph",ax=None):
    #     if ax is None:
    #         # If no existing axis is provided, create a new figure and axis
    #         fig, ax = plt.subplots()

    #     pos = self._pos_by_layout(graph,layout)

    #     nodes_color = ["skyblue" for node_name in graph.nodes()]
    #     nodes_labels = {}

    #     for node_name in graph.nodes():
    #         nodes_labels[node_name] = node_name

    #     # Draw the nodes and edges of the graph on the provided axis
    #     nx.draw_networkx_nodes(graph, pos, node_size=500, node_color=nodes_color, ax=ax)
    #     nx.draw_networkx_labels(graph, pos, labels=nodes_labels, font_size=10, ax=ax)

    #     edge_weights = [graph[u][v]['compatibility'] for u, v in graph.edges()]
    #     cmap = plt.cm.get_cmap('plasma')
        
    #     edges = nx.draw_networkx_edges(graph, pos, edge_color=edge_weights, edge_cmap=cmap,
    #                                 width=2.0, ax=ax, edge_vmin=min(edge_weights), edge_vmax=max(edge_weights))

    #     cb = plt.colorbar(edges, ax=ax, label='Comptatibility')

    #     # Set the title for the plot
    #     ax.set_title(title)
    
    # def draw_adjacency_graph(self,layout="kamada_kawai",title="Adjacency Graph",ax=None):
        
    #     if ax is None:
    #         # If no existing axis is provided, create a new figure and axis
    #         fig, ax = plt.subplots()
        
    #     # pos = layouts[layout](self.adjacency_graph)
    #     pos = self._pos_by_layout(self.adjacency_graph,layout)
     
    #     edges_color = ["red" if self.piece_name(edge[0]) ==self.piece_name(edge[1]) else "blue"  for edge in self.adjacency_graph.edges]
    #     nx.draw_networkx(self.adjacency_graph,pos,with_labels=True,node_color="skyblue",
    #                      edge_color=edges_color,font_size=10,ax=ax)
        

    # def draw(self,layout="planar",title="Matching Graph",ax=None):
    #     self._draw_general_layout(self.matching_graph,layout=layout,title=title,ax=ax)
    

    def draw_adjacency_with_potential_matings(self,layout="kamada_kawai",title="Adjacency Graph",ax=None):
        
        if ax is None:
            # If no existing axis is provided, create a new figure and axis
            fig, ax = plt.subplots()
        
        # pos = layouts[layout](self.adjacency_graph)
        
        adjacency_with_potential_graph = self.adjacency_graph.copy()
        potential_matings = [edge for edge in self.matching_graph.edges if edge not in self.matching]

        adjacency_with_potential_graph.add_edges_from(potential_matings)

        pos = self._pos_by_layout(adjacency_with_potential_graph,layout)
     
        edges_color = []
        for edge in adjacency_with_potential_graph.edges:
            if get_piece_name(edge[0]) == get_piece_name(edge[1]):
                edges_color.append("red")
            elif edge in self.adjacency_graph.edges:
                edges_color.append("blue")
            else:
                edges_color.append("gray")
        
        nx.draw_networkx(adjacency_with_potential_graph,pos,with_labels=True,node_color="skyblue",
                         edge_color=edges_color,font_size=10,ax=ax)
        
        
        # nx.draw_networkx_edges(self.adjacency_graph,pos,potential_matings,edge_color="purple")
    


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