from src.mating_graphs.matching_graph import MatchingGraphAndSpanTree,get_edge_name,get_piece_name
import numpy as np
import networkx as nx
import math
import matplotlib.pyplot as plt

class MatchingGraphDrawer():

    def __init__(self,noiseless_ground_truth_graph:MatchingGraphAndSpanTree) -> None:
        self.noiseless_ground_truth_graph = noiseless_ground_truth_graph

    def _piece_cluserted_layout(self,graph):
        
        # Create a dictionary to store the clusters (pieces) of nodes
        clusters = {}

        for node in graph.nodes():
            if node.startswith("P_"):
                piece_number = node.split("_")[1]
                if piece_number not in clusters:
                    clusters[piece_number] = []
                clusters[piece_number].append(node)

        # Calculate the number of clusters and assign them to different positions
        num_clusters = len(clusters)
        positions = nx.spring_layout(graph, k=10, seed=42) #k=0.1

        cluster_positions = {}
        for idx, cluster in enumerate(clusters.values()):
            angle = 2 * idx * 3.14 / num_clusters
            for node in cluster:
                x, y = positions[node]
                x_new = x * 0.1 * num_clusters + 0.9 * num_clusters * math.cos(angle)
                y_new = y * 0.1 * num_clusters + 0.9 * num_clusters * math.sin(angle)
                cluster_positions[node] = (x_new, y_new)

        return cluster_positions

    def _pos_by_layout(self,graph,layout):
        layouts = {
            "spring": nx.spring_layout,
            "spectral": nx.spectral_layout,
            "random": nx.random_layout,
            "circular": nx.circular_layout,
            "shell":nx.shell_layout,
            "rescale":nx.rescale_layout,
            "spiral":nx.spiral_layout,
            "kamada_kawai": nx.kamada_kawai_layout,
            "planar":nx.planar_layout,
            "piece_clustered":None
            # "multipartite":nx.multipartite_layout
            #"multipartite": nx.multipartite_layout
            # Add more layout options as needed
        }

        if layout not in layouts:
            raise ValueError(f"Invalid layout option. Choose one of: {', '.join(layouts.keys())}")
        
        if layout == "piece_clustered":
            pos = self._piece_cluserted_layout(graph)
        elif layout == "spring":
            num_nodes = len(list(graph.nodes))
            pos = nx.spring_layout(graph,k=4/np.sqrt(num_nodes))
        else:
            pos = layouts[layout](graph)
        
        return pos

    def _draw_general_layout(self,graph,layout="spectral",title="Graph",ax=None):
        if ax is None:
            # If no existing axis is provided, create a new figure and axis
            fig, ax = plt.subplots()

        pos = self._pos_by_layout(graph,layout)

        nodes_color = ["skyblue" for node_name in graph.nodes()]
        nodes_labels = {}

        for node_name in graph.nodes():
            nodes_labels[node_name] = node_name

        # Draw the nodes and edges of the graph on the provided axis
        nx.draw_networkx_nodes(graph, pos, node_size=500, node_color=nodes_color, ax=ax)
        nx.draw_networkx_labels(graph, pos, labels=nodes_labels, font_size=10, ax=ax)

        edge_weights = [graph[u][v]['compatibility'] for u, v in graph.edges()]
        cmap = plt.cm.get_cmap('plasma')
        
        edges = nx.draw_networkx_edges(graph, pos, edge_color=edge_weights, edge_cmap=cmap,
                                    width=2.0, ax=ax, edge_vmin=min(edge_weights), edge_vmax=max(edge_weights))

        cb = plt.colorbar(edges, ax=ax, label='Comptatibility')

        # Set the title for the plot
        ax.set_title(title)

    def _draw_adjacency_graph(self,adjacency_graph:MatchingGraphAndSpanTree,layout="kamada_kawai",title="Adjacency Graph",ax=None):
        
        if ax is None:
            # If no existing axis is provided, create a new figure and axis
            fig, ax = plt.subplots()
        
        pos = self._pos_by_layout(adjacency_graph,layout)
     
        edges_color = ["red" if get_piece_name(edge[0]) == get_piece_name(edge[1]) else "blue"  for edge in adjacency_graph.edges]
        nx.draw_networkx(adjacency_graph,pos,with_labels=True,node_color="skyblue",
                         edge_color=edges_color,font_size=10,ax=ax)


    def _draw_ground_truth_adjacency(self):
        self._draw_adjacency_graph(self.noiseless_ground_truth_graph.adjacency_graph)

    def _draw_ground_truth_matching(self,layout="planar",title="Matching Graph",ax=None):
        self._draw_general_layout(self.noiseless_ground_truth_graph.matching_graph,layout=layout,title=title,ax=ax)


    def draw_adjacency_graph(self,graph:MatchingGraphAndSpanTree):
        pass