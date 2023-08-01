import networkx as nx
from src.data_structures import Mating
import matplotlib.pyplot as plt
import matplotlib.collections as mpc
import math


class Cycle():

    def __init__(self, matings_chain:list, piece2occurence:dict) -> None:
        self.matings_chain = matings_chain
        self.piece2occurence = piece2occurence
    
    def get_pieces_involved(self):
        return self.piece2occurence.keys()

    def get_num_pieces(self):
        return len(self.piece2occurence.keys())

    def is_all_piece_occur(self,occurence_num):
        for piece_id in self.piece2occurence.keys():
            
            if self.piece2occurence[piece_id] != occurence_num:
                return  False
        
        return True

    def is_has_piece_duplicate_occurence(self):

        for piece_id in self.piece2occurence.keys():
            
            if self.piece2occurence[piece_id] > 2:
                return  True
        
        return False
    
    def __repr__(self) -> str:
        acc = ""
        delimiter = "==>"

        for mate in self.matings_chain:
            acc = acc + delimiter + repr(mate)
        
        return acc[len(delimiter):]





class EdgeMatingGraph():
    
    def __init__(self,pieces,match_edges=None,match_pieces_score=None) -> None:
        '''
        pieces - bag of pieces
        match_edges - the attribute from the pairwiser
        match_pieces_score - the attribute from the pairwiser
        '''
        self.pieces = pieces
        self.match_edges = match_edges
        self.match_pieces_score = match_pieces_score
        self.edges_mating_graph = nx.DiGraph()
        self.cycles = None
        self.raw_cycles = None

    def _name_inter_node(self,piece_name,edge_name):
        return f"P_{piece_name}_E_{edge_name}_INTER"
    
    def _name_env_node(self,piece_name,edge_name):
        return f"P_{piece_name}_E_{edge_name}_ENV" # In terms of english, could be INTRA instead of ENV, but I found it more confusing


    def _bulid_relationship_nodes(self):
        for piece in self.pieces:
            num_coords = piece.get_num_coords()
            
            self.edges_mating_graph.add_nodes_from(
                #[f"P_{piece.id}_RELS_E_{edge_index}" for edge_index in range(len(coords))]
                [self._name_inter_node(piece.id,edge_index) for edge_index in range(num_coords)]
            )

    def _bulid_enviorments_nodes(self):
        for piece in self.pieces:
            num_vertices = piece.get_num_coords()
            for edge_index in range(num_vertices):
                env_node = self._name_env_node(piece.id,edge_index)#f"P_{piece.id}_ENV_{edge_index}"

                '''Since the polygons are oriented counter clockwise (ccw) than we need to check only one adjacent edge (and not both)'''
                #next_adj_edge = self._get_inter_pieces_node_name(piece.id,(edge_index+1)%num_vertices)
                #prev_adj_edge = self._get_inter_pieces_node_name((edge_index-1)%num_vertices

                # adj_edge = f"P_{piece.id}_ENV_{edge_index}_ADJ_{adj_edge_index}"
                self.edges_mating_graph.add_nodes_from([env_node])
    
    def _connect_env_nodes(self):
        for piece in self.pieces:
            num_vertices = piece.get_num_coords()
            for edge_index in range(num_vertices):
                env_node = self._name_env_node(piece.id,edge_index)#f"P_{piece.id}_ENV_{edge_index}"
                next_adj_edge = self._name_inter_node(piece.id,(edge_index+1)%num_vertices)
                prev_adj_edge = self._name_inter_node(piece.id,(edge_index-1)%num_vertices)

                self.edges_mating_graph.add_edges_from(
                    [(env_node,next_adj_edge,{"compatibility":0}),(env_node,prev_adj_edge,{"compatibility":0})]
                )

    def _connect_relationship_nodes(self):
        num_pieces = len(self.pieces)
        for piece_i in range(num_pieces):
            piece_i_id = self.pieces[piece_i].id
            for piece_j in range(num_pieces):
                piece_j_id = self.pieces[piece_j].id
                mating_edges = self.match_edges[piece_i,piece_j]
                if len(mating_edges)>0:
                    mating_edges_scores = self.match_pieces_score[piece_i,piece_j]
                    for k,mat_edge in enumerate(mating_edges):
                        new_links = []

                        for mating in mat_edge:
                            inter_node = self._name_inter_node(piece_i_id,mating[0])
                            env_node = self._name_env_node(piece_j_id,mating[1])
                            compatibility = mating_edges_scores[k]
                            new_links.append((inter_node,env_node,{"compatibility":compatibility}))
                        
                        self.edges_mating_graph.add_edges_from(new_links)

    def build_graph(self):
        '''
            Computes the mating graph (direct graph) between edges. 
            It was design in the following way to allow the nx package to find zero loops.
            Each edge has the following nodes in the graphs:
            1. Relationships node. P_{piece.id}_RELS_E_{edge_index}: a node that represents the pairwise matching of the edge.
                 It has links (edges in the mating graph) to other edges that pairwise it
            2. P_{piece.id}_ENV_{edge_index}: it has in a in-link to relationship node and out link to two nodes that represent adjacent edge to it.
            3. P_{piece.id}_ENV_{edge_index}_ADJ_{adj_edge_index}: represent an edge that adjacent to another edge. the link from the type 2 to this type has weight with the value of the angle.        
        '''
        self._bulid_relationship_nodes()
        self._bulid_enviorments_nodes()
        self._connect_env_nodes()
        self._connect_relationship_nodes()
    
    def load_raw_cycles(self,path_to_load):
        #Because the nx package would brings random results, make the test deterministic
        with open(path_to_load, 'r') as f:
            self.raw_cycles = [eval(line.rstrip('\n')) for line in f]

    def compute_raw_cycles(self):
        self.raw_cycles = list(nx.simple_cycles(self.edges_mating_graph))

    def find_cycles(self):

        if self.raw_cycles is None:
            raise ("You need to load or compute the raw cycles")
        
        self.cycles = []

        for cycle in self.raw_cycles:
            edges_involved = [edge for edge in cycle if "RELS" in edge]
            piece2occurence = {}
            matings_chain = []

            for edge_prev,edge_next in zip(edges_involved,edges_involved[1:] + [edges_involved[0]]):
                '''The convention of node of edge rels in the mating graph is the following:
                f"P_{piece.id}_RELS_E_{edge_index}"'''
                split_prev = edge_prev.split("_")
                piece_1 = split_prev[1]
                edge_1 = eval(split_prev[-1])
                split_next = edge_next.split("_")
                piece_2 = split_next[1]
                edge_2 = eval(split_next[-1])

                # internal jump between adjacent edges inside a piece
                if piece_1 == piece_2:
                    continue
                
                piece2occurence.setdefault(piece_1,0)
                piece2occurence[piece_1]+=1
                piece2occurence.setdefault(piece_2,0)
                piece2occurence[piece_2]+=1

                matings_chain.append(Mating(piece_1=piece_1,edge_1=edge_1,piece_2=piece_2,edge_2=edge_2))

            next_cycle = Cycle(matings_chain,piece2occurence)

            if next_cycle.get_num_pieces() <=2:
                continue

            # if next_cycle.is_has_piece_duplicate_occurence():
            #     continue

            self.cycles.append(next_cycle)
        
        return self.cycles

    def save_raw_cycles(self,output_path):
        with open(output_path, 'w') as fp:
            for item in self.raw_cycles:
                fp.write("%s\n" % item)


    def _get_node_display_name(self,name:str):
        splitted = name.split("_")
        # E.g P_6_E_1_INTER
        if "INTER" in name or "ENV" in name:
            return f"P_{splitted[1]}_e_{splitted[3]}"
        else:
            return "None"

    def _get_node_color(self,name):
        if "INTER" in name:
            return "skyblue" #"gold"
        elif "ENV" in name:
            return "red" 
        else:
            return "gray"
    

    def draw_all(self,layout="kamada_kawai", title="Complete_Graph", ax=None):
        layouts = {
            "spring": nx.spring_layout,
            "spectral": nx.spectral_layout,
            "random": nx.random_layout,
            "circular": nx.circular_layout,
            "shell":nx.shell_layout,
            "rescale":nx.rescale_layout,
            "spiral":nx.spiral_layout,
            "kamada_kawai": nx.kamada_kawai_layout
            # "multipartite":nx.multipartite_layout
            # "planar":nx.planar_layout
            #"multipartite": nx.multipartite_layout
            # Add more layout options as needed
        }

        if layout not in layouts:
            raise ValueError(f"Invalid layout option. Choose one of: {', '.join(layouts.keys())}")

        if ax is None:
            # If no existing axis is provided, create a new figure and axis
            fig, ax = plt.subplots()

        # Create the layout for the nodes
        pos = layouts[layout](self.edges_mating_graph)

        nodes_color = [self._get_node_color(node_name) for node_name in self.edges_mating_graph.nodes()]
        nodes_labels = {}

        for node_name in self.edges_mating_graph.nodes():
            nodes_labels[node_name] = self._get_node_display_name(node_name)

        # Get edge weights from the graph
        edge_weights = [self.edges_mating_graph[u][v]['compatibility'] for u, v in self.edges_mating_graph.edges()]

        # Draw the nodes and edges of the graph on the provided axis
        nx.draw_networkx_nodes(self.edges_mating_graph, pos, node_size=500, node_color=nodes_color, ax=ax)
        nx.draw_networkx_labels(self.edges_mating_graph, pos, labels=nodes_labels, font_size=10, ax=ax)

        cmap = plt.cm.get_cmap('plasma')
        # Draw edges separately to get a mappable for colorbar
        edges = nx.draw_networkx_edges(self.edges_mating_graph, pos, edge_color=edge_weights, edge_cmap=cmap,
                                    width=2.0, ax=ax, edge_vmin=min(edge_weights), edge_vmax=max(edge_weights))

        
        pc = mpc.PatchCollection(edges, cmap=cmap)
        pc.set_array(edge_weights)

        # Add a color bar to show the mapping of edge weights to colors
        cb = plt.colorbar(pc, ax=ax, label='Comptatibility')
        cb.set_ticks([min(edge_weights), max(edge_weights)]) 

        # Set the title for the plot
        ax.set_title(title)


    def _important_subgraph(self):
        subgraph = nx.DiGraph()

        for node in self.edges_mating_graph.nodes:

            if "ENV" in node:
                in_edges = list(self.edges_mating_graph.in_edges(node))
                if len(in_edges) > 0:
                    subgraph.add_node(node)

                    for in_edg in in_edges:
                        comp = self.edges_mating_graph.get_edge_data(in_edg[0],in_edg[1])["compatibility"]
                        subgraph.add_edge(in_edg[0],in_edg[1],compatibility=comp)
                
                    out_edges = list(self.edges_mating_graph.out_edges(node))

                    for edge in out_edges:
                        dst_inter_node = edge[1]
                        if len(list(self.edges_mating_graph.out_edges(dst_inter_node))) > 0:
                            comp = self.edges_mating_graph.get_edge_data(edge[0],edge[1])["compatibility"]
                            subgraph.add_edge(edge[0],edge[1],compatibility=comp)

        return subgraph                    

    def draw_compressed_piece_clustered(self,title="Compressed_and_Clustered", ax=None):

        if ax is None:
            # If no existing axis is provided, create a new figure and axis
            fig, ax = plt.subplots()

        # Create the layout for the nodes
        # pos = layouts[layout](self.edges_mating_graph)
        

        subgraph = self._important_subgraph()

    
        # Get the nodes containing "ENV" and "INTER"
        # Create a dictionary to store the clusters (pieces) of nodes
        clusters = {}

        for node in subgraph.nodes():
            if node.startswith("P_"):
                piece_number = node.split("_")[1]
                if piece_number not in clusters:
                    clusters[piece_number] = []
                clusters[piece_number].append(node)

        # Calculate the number of clusters and assign them to different positions
        num_clusters = len(clusters)
        positions = nx.spring_layout(subgraph, k=10, seed=42) #k=0.1

        cluster_positions = {}
        for idx, cluster in enumerate(clusters.values()):
            angle = 2 * idx * 3.14 / num_clusters
            for node in cluster:
                x, y = positions[node]
                x_new = x * 0.1 * num_clusters + 0.9 * num_clusters * math.cos(angle)
                y_new = y * 0.1 * num_clusters + 0.9 * num_clusters * math.sin(angle)
                cluster_positions[node] = (x_new, y_new)

        pos = cluster_positions

        # pos = nx.planar_layout(subgraph)

        nodes_color = [self._get_node_color(node_name) for node_name in subgraph.nodes()]
        nodes_labels = {}

        for node_name in subgraph.nodes():
            nodes_labels[node_name] = self._get_node_display_name(node_name)

        # Get edge weights from the graph
        edge_weights = [subgraph[u][v]['compatibility'] for u, v in subgraph.edges()]

        # Draw the nodes and edges of the graph on the provided axis
        nx.draw_networkx_nodes(subgraph, pos, node_size=500, node_color=nodes_color, ax=ax)
        nx.draw_networkx_labels(subgraph, pos, labels=nodes_labels, font_size=10, ax=ax)

        cmap = plt.cm.get_cmap('plasma')
        # Draw edges separately to get a mappable for colorbar
        edges = nx.draw_networkx_edges(subgraph, pos, edge_color=edge_weights, edge_cmap=cmap,
                                    width=2.0, ax=ax, edge_vmin=min(edge_weights), edge_vmax=max(edge_weights))

        
        pc = mpc.PatchCollection(edges, cmap=cmap)
        pc.set_array(edge_weights)

        # Add a color bar to show the mapping of edge weights to colors
        cb = plt.colorbar(pc, ax=ax, label='Comptatibility')
        cb.set_ticks([min(edge_weights), max(edge_weights)]) 

        # Set the title for the plot
        ax.set_title(title)


    def draw_compressed(self,layout="planar", title="Compressed_and_Planar", ax=None):
        layouts = {
            "spring": nx.spring_layout,
            "spectral": nx.spectral_layout,
            "random": nx.random_layout,
            "circular": nx.circular_layout,
            "shell":nx.shell_layout,
            "rescale":nx.rescale_layout,
            "spiral":nx.spiral_layout,
            "kamada_kawai": nx.kamada_kawai_layout,
            # "multipartite":nx.multipartite_layout
            "planar":nx.planar_layout
            #"multipartite": nx.multipartite_layout
            # Add more layout options as needed
        }

        if ax is None:
            # If no existing axis is provided, create a new figure and axis
            fig, ax = plt.subplots()


        subgraph = self._important_subgraph()

        pos = layouts[layout](subgraph)

        nodes_color = [self._get_node_color(node_name) for node_name in subgraph.nodes()]
        nodes_labels = {}

        for node_name in subgraph.nodes():
            nodes_labels[node_name] = self._get_node_display_name(node_name)

        # Get edge weights from the graph
        edge_weights = [subgraph[u][v]['compatibility'] for u, v in subgraph.edges()]

        # Draw the nodes and edges of the graph on the provided axis
        nx.draw_networkx_nodes(subgraph, pos, node_size=500, node_color=nodes_color, ax=ax)
        nx.draw_networkx_labels(subgraph, pos, labels=nodes_labels, font_size=10, ax=ax)

        cmap = plt.cm.get_cmap('plasma')
        # Draw edges separately to get a mappable for colorbar
        edges = nx.draw_networkx_edges(subgraph, pos, edge_color=edge_weights, edge_cmap=cmap,
                                    width=2.0, ax=ax, edge_vmin=min(edge_weights), edge_vmax=max(edge_weights))

        
        pc = mpc.PatchCollection(edges, cmap=cmap)
        pc.set_array(edge_weights)

        # Add a color bar to show the mapping of edge weights to colors
        cb = plt.colorbar(pc, ax=ax, label='Comptatibility')
        cb.set_ticks([min(edge_weights), max(edge_weights)]) 

        # Set the title for the plot
        ax.set_title(title)

