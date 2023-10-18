from src.mating_graphs.matching_graph import MatchingGraphWrapper,get_edge_name,get_piece_name
import numpy as np
import networkx as nx
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class MatchingGraphDrawer():

    def __init__(self,noiseless_ground_truth_wrapper:MatchingGraphWrapper) -> None:
        self.noiseless_ground_truth_wrapper = noiseless_ground_truth_wrapper
        self.node2position = {}

    def init(self):
        self._pos_nodes_by_ground_truth()

    def _pos_nodes_by_ground_truth(self,layout="kamada_kawai"):
        ground_truth_adj_graph = self.noiseless_ground_truth_wrapper.adjacency_graph
        self.node2position = self._pos_by_layout(ground_truth_adj_graph,layout=layout)

        return self.node2position

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

    def _draw_general_layout(self,graph,layout="kamada_kawai",title="Graph",ax=None):
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

    
    def _draw_ground_truth_adjacency(self,layout="kamada_kawai",title="Adjacency Graph",ax=None):
        # self._draw_adjacency_graph(self.noiseless_ground_truth_wrapper.adjacency_graph)
        adjacency_graph = self.noiseless_ground_truth_wrapper.adjacency_graph
        if ax is None:
            # If no existing axis is provided, create a new figure and axis
            fig, ax = plt.subplots()
        
        pos = self._pos_by_layout(adjacency_graph,layout)
     
        edges_color = ["red" if get_piece_name(edge[0]) == get_piece_name(edge[1]) else "blue"  for edge in adjacency_graph.edges]
        nx.draw_networkx(adjacency_graph,pos,with_labels=True,node_color="skyblue",
                         edge_color=edges_color,font_size=10,ax=ax)

    def draw_adjacency_graph(self,graph,layout="kamada_kawai",title="Adjacency Graph",ax=None):
        if ax is None:
            fig, ax = plt.subplots()


        edges_color = []
        color2edge_meaning = {
            "intra_piece":"red",
            "ground_truth_edge":"blue",
            "missed_edge":"black",
            "potential":"orange"
        }


        # for edge in adjacency_with_potential_graph.edges:
        for edge in graph.edges:
            if get_piece_name(edge[0]) == get_piece_name(edge[1]):
                edges_color.append(color2edge_meaning["intra_piece"])
            elif edge in self.noiseless_ground_truth_wrapper.potential_matings_graph.edges:
                edges_color.append(color2edge_meaning["ground_truth_edge"])
            else:
                edges_color.append(color2edge_meaning["potential"])
        
        nx.draw_networkx(graph,self.node2position,with_labels=True,node_color="skyblue",
                         edge_color=edges_color,font_size=10,ax=ax,width=1.5)
        

        red_patch = mpatches.Patch(color=color2edge_meaning["intra_piece"], label='Internal edge')
        blue_patch = mpatches.Patch(color=color2edge_meaning["ground_truth_edge"], label='Ground Truth edge')
        gray_patch = mpatches.Patch(color=color2edge_meaning["potential"], label='Potential edge')

        # Plot empty lists with the desired colors and labels
        ax.plot([], [], color=color2edge_meaning["intra_piece"], label='Internal edge', linewidth=5)
        ax.plot([], [], color=color2edge_meaning["ground_truth_edge"], label='Ground Truth edge', linewidth=5)
        ax.plot([], [], color=color2edge_meaning["potential"], label='Potential edge', linewidth=5)

        # Create and show legend
        ax.legend(loc='upper left')
        handles = [red_patch, blue_patch,gray_patch]
        ax.legend(handles=handles, loc='upper left')
        ax.axis('off')

    
    def _draw_ground_truth_matching(self,layout="planar",title="Ground Truth Matching",ax=None):
        self._draw_general_layout(self.noiseless_ground_truth_wrapper.potential_matings_graph,layout=layout,title=title,ax=ax)
    
    def _draw_graph_matching(self,matings_graph:nx.Graph,
                             layout="planar",title="Matching Graph",
                             ax=None,
                             max_edge_weight = None,min_edge_weight = None):

        if ax is None:
            # If no existing axis is provided, create a new figure and axis
            fig, ax = plt.subplots()

        # pos = self._pos_by_layout(graph.matching_graph,layout)
        my_graph = nx.Graph()
        my_graph.add_nodes_from(self.noiseless_ground_truth_wrapper.pieces_only_graph.nodes)
        my_graph.add_edges_from(matings_graph.edges)

        nodes_labels = {}

        for node_name in my_graph.nodes():
            nodes_labels[node_name] = node_name

        # Draw the nodes and edges of the graph on the provided axis
        nx.draw_networkx_nodes(my_graph, self.node2position, node_size=500, node_color="skyblue", ax=ax)
        nx.draw_networkx_labels(my_graph, self.node2position, labels=nodes_labels, font_size=10, ax=ax)

        edge_weights = [matings_graph[u][v]['compatibility'] for u, v in matings_graph.edges()]
        cmap = plt.cm.get_cmap('plasma')
        
        if max_edge_weight is None:
            max_edge_weight = max(edge_weights)
        
        if min_edge_weight is None:
            min_edge_weight = min(edge_weights)
        
        edges = nx.draw_networkx_edges(my_graph, self.node2position, edge_color=edge_weights, edge_cmap=cmap,
                                    width=2.0, ax=ax, 
                                    edge_vmin=min_edge_weight, edge_vmax=max_edge_weight,
                                    edgelist=matings_graph.edges(data=True))

        
        cb = plt.colorbar(edges, ax=ax, label='Comptatibility')

        # Set the title for the plot
        ax.set_title(title)

        nx.draw_networkx_edges(my_graph, self.node2position, edge_color="gray",
                               edgelist=self.noiseless_ground_truth_wrapper.pieces_only_graph.edges)

    def draw_graph_matching(self,graph_wrapper:MatchingGraphWrapper,
                            layout="planar",title="Matching Graph",
                            ax=None,
                            max_edge_weight = None,min_edge_weight = None):
        self._draw_graph_matching(graph_wrapper.potential_matings_graph,
                                  layout=layout,title=title,ax=ax,
                                  max_edge_weight=max_edge_weight,min_edge_weight=min_edge_weight)
    
    def draw_graph_filtered_matching(self,graph_wrapper:MatchingGraphWrapper,
                                     layout="planar",title="Filtered Matching Graph",
                                     ax=None,
                                     max_edge_weight = None,min_edge_weight = None):
        self._draw_graph_matching(graph_wrapper.filtered_potential_matings_graph,
                                  layout=layout,title=title+f"( >{graph_wrapper.compatibility_threshold})",ax=ax,
                                  max_edge_weight = max_edge_weight,min_edge_weight = min_edge_weight)