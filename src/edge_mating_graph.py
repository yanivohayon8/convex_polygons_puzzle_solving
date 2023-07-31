import networkx as nx
from src.data_structures import Mating
import matplotlib.pyplot as plt


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

    def _bulid_relationship_nodes(self):
        for piece in self.pieces:
            coords = piece.get_coords()
            
            self.edges_mating_graph.add_nodes_from(
                [f"P_{piece.id}_RELS_E_{edge_index}" for edge_index in range(len(coords))]
            )

    def _bulid_enviorments_nodes(self):
        for piece in self.pieces:
            num_vertices = len(piece.get_coords())
            for edge_index in range(num_vertices):
                central_edge = f"P_{piece.id}_ENV_{edge_index}"

                '''Since the polygons are oriented counter clockwise (ccw) than we need to check only one adjacent edge (and not both)'''
                adj_edge_index = (edge_index+1)%num_vertices
                adj_edge = f"P_{piece.id}_ENV_{edge_index}_ADJ_{adj_edge_index}"
                
                self.edges_mating_graph.add_nodes_from(
                    [central_edge,adj_edge]
                )

                self.edges_mating_graph.add_edges_from(
                    [
                    (central_edge,adj_edge),
                    (f"P_{piece.id}_RELS_E_{edge_index}",central_edge),
                    (adj_edge,f"P_{piece.id}_RELS_E_{adj_edge_index}")
                    ]
                )

    def _connect_relationship_nodes(self):
        num_pieces = len(self.pieces)
        for piece_i in range(num_pieces):
            for piece_j in range(num_pieces):
                mating_edges = self.match_edges[piece_i,piece_j]
                if len(mating_edges)>0:
                    for mat_edge in mating_edges:
                        new_links = [
                            (f"P_{self.pieces[piece_i].id}_RELS_E_{mating[0]}",f"P_{self.pieces[piece_j].id}_RELS_E_{mating[1]}") \
                                    for mating in mat_edge]
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
        # E.g P_6_RELS_E_1
        if "RELS" in name:
            return f"P_{splitted[1]}_e_{splitted[-1]}"
        elif "ENV" in name:
            #E.g P_6_ENV_2_ADJ_3
            if "ADJ" in name:
                return f"P_{splitted[1]}_e_{splitted[-1]}"
            else:
                #E.g P_6_ENV_2
                return f"P_{splitted[1]}_e_{splitted[-1]}"
        else:
            return "gray"

    def _get_node_color(self,name):
        if "RELS" in name:
            return "gold"
        elif "ENV" in name:
            if "ADJ" in name:
                return "skyblue"
            else:
                return "cyan"
        else:
            return "gray"
        
    def draw(self,layout="spring", title="Graph", ax=None):
        layouts = {
            "spring": nx.spring_layout,
            "random": nx.random_layout,
            # "circular": nx.circular_layout,
            "kamada_kawai": nx.kamada_kawai_layout,
            "multipartite": nx.multipartite_layout
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

        # Draw the nodes and edges of the graph on the provided axis
        nx.draw(self.edges_mating_graph, pos, labels=nodes_labels, node_size=500, node_color=nodes_color,
                font_size=10, ax=ax)

        # Set the title for the plot
        ax.set_title(title)



