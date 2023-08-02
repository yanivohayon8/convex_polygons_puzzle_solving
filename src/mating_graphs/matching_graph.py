import networkx as nx
from src.data_structures import Mating
import matplotlib.pyplot as plt
import matplotlib.collections as mpc
from  matplotlib.cm import ScalarMappable
import numpy as np

class MatchingGraphAndSpanTree():

    def __init__(self,pieces,match_edges=None,match_pieces_score=None) -> None:
        self.pieces = pieces
        self.match_edges = match_edges
        self.match_pieces_score = match_pieces_score
        self.matching_graph = nx.Graph()
        self.adjacency_graph = nx.Graph()

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

    def build_graph(self):
        pass
    
    def get_matching_graph_nodes(self):
        return list(self.matching_graph.nodes)

    def _draw_general_layout(self,graph,layout="spectral",title="Graph",ax=None):
        layouts = {
            "spring": nx.spring_layout,
            "spectral": nx.spectral_layout,
            "random": nx.random_layout,
            "circular": nx.circular_layout,
            "shell":nx.shell_layout,
            "rescale":nx.rescale_layout,
            "spiral":nx.spiral_layout,
            "kamada_kawai": nx.kamada_kawai_layout,
            "planar":nx.planar_layout
            # "multipartite":nx.multipartite_layout
            #"multipartite": nx.multipartite_layout
            # Add more layout options as needed
        }

        if layout not in layouts:
            raise ValueError(f"Invalid layout option. Choose one of: {', '.join(layouts.keys())}")

        if ax is None:
            # If no existing axis is provided, create a new figure and axis
            fig, ax = plt.subplots()

        pos = layouts[layout](graph)

        nodes_color = ["skyblue" for node_name in graph.nodes()]
        nodes_labels = {}

        for node_name in graph.nodes():
            nodes_labels[node_name] = node_name

        # Draw the nodes and edges of the graph on the provided axis
        nx.draw_networkx_nodes(graph, pos, node_size=500, node_color=nodes_color, ax=ax)
        nx.draw_networkx_labels(graph, pos, labels=nodes_labels, font_size=10, ax=ax)

        edge_weights = [graph[u][v]['compatibility'] for u, v in graph.edges()]
        cmap = plt.cm.get_cmap('plasma')
        
        # Draw edges separately to get a mappable for colorbar
        edges = nx.draw_networkx_edges(graph, pos, edge_color=edge_weights, edge_cmap=cmap,
                                    width=2.0, ax=ax, edge_vmin=min(edge_weights), edge_vmax=max(edge_weights))

        # # Add a color bar to show the mapping of edge weights to colors
        cb = plt.colorbar(edges, ax=ax, label='Comptatibility')
        # cb.set_ticks([min(edge_weights), max(edge_weights)]) 

        # Set the title for the plot
        ax.set_title(title)
    
    
    
    def draw(self,layout="spectral",title="Matching Graph",ax=None):
        self._draw_general_layout(self.matching_graph,layout=layout,title=title,ax=ax)