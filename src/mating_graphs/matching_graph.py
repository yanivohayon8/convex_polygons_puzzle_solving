import networkx as nx
from src.data_types.mating import Mating
from src.mating_graphs import factory


INTER_PIECES_LINK_TYPE = "inter_piece"
WITHIN_PIECE_LINK_TYPE = "within_piece"
INTER_AGGREGATE_LINK_TYPE = "inter_agg"
WITHIN_AGGREGATE_LINK_TYPE = "within_agg"

class MatchingGraphWrapper():

    def __init__(self,pieces,id2piece:dict,geometric_match_edges=None,
                 pictorial_matcher=None,compatibility_threshold = 0.4) -> None:
        self.pieces = pieces
        self.id2piece = id2piece
        self.geometric_match_edges = geometric_match_edges
        self.pictorial_matcher = pictorial_matcher
        self.potential_matings_graph = None#nx.Graph()
        self.filtered_potential_matings_graph = None
        self.pieces_only_graph = None#nx.Graph()
        self.adjacency_graph = None
        self.filtered_adjacency_graph = None
        self.compatibility_threshold = compatibility_threshold

    def _name_node(self,piece_name,edge_name):
        return f"P_{piece_name}_E_{edge_name}"

    def _build_matching_graph(self):
        self.potential_matings_graph = nx.Graph()
        num_pieces = len(self.pieces)

        for piece_i in range(num_pieces):
            piece_i_id = self.pieces[piece_i].id
            for piece_j in range(piece_i+1,num_pieces):
                piece_j_id = self.pieces[piece_j].id
                mating_edges = self.geometric_match_edges[piece_i,piece_j]
                if len(mating_edges)>0:
                    # mating_edges_scores = self.geometric_match_pieces_score[piece_i,piece_j]
                    for k,mat_edge in enumerate(mating_edges):
                        new_links = []

                        for mating in mat_edge:
                            first_node = self._name_node(piece_i_id,mating[0])
                            second_node = self._name_node(piece_j_id,mating[1])
                            
                            if self.pictorial_matcher is None:
                                compatibility = 1
                            else:
                                compatibility = self.pictorial_matcher.get_score(piece_i_id,mating[0],piece_j_id,mating[1]) #mating_edges_scores[k]
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
    
    

    def _build_filtered_matching_graph(self):
        # self.filtered_potential_matings_graph = self.potential_matings_graph.copy()
        self.filtered_potential_matings_graph = nx.Graph()
        
        for node, attributes in self.potential_matings_graph.nodes(data=True):
            self.filtered_potential_matings_graph.add_node(node, **attributes)

        filtered_edges = []

        for edge_attributes in self.potential_matings_graph.edges(data=True):
            if edge_attributes[2]["compatibility"] >= self.compatibility_threshold:
                filtered_edges.append(edge_attributes)
        
        self.filtered_potential_matings_graph.add_edges_from(filtered_edges,type="inter_piece")    

    def _build_adjacency_graph(self):
        self.adjacency_graph = nx.Graph()#self.pieces_only_graph.copy()
        self.adjacency_graph.add_nodes_from(self.pieces_only_graph.nodes)
        self.adjacency_graph.add_edges_from(self.pieces_only_graph.edges, type="within_piece")

        potential_matings = [edge for edge in self.potential_matings_graph.edges if not edge in self.pieces_only_graph]
        self.adjacency_graph.add_edges_from(potential_matings,type="inter_piece")
    
    def _build_filtered_adjacency_graph(self):     
        self.filtered_adjacency_graph = nx.Graph()
        self.filtered_adjacency_graph.add_nodes_from(self.pieces_only_graph.nodes,local_assembly=None)
        self.filtered_adjacency_graph.add_edges_from(self.pieces_only_graph.edges, type=WITHIN_PIECE_LINK_TYPE)
        potential_matings = [edge for edge in self.filtered_potential_matings_graph.edges if not edge in self.pieces_only_graph]
        self.filtered_adjacency_graph.add_edges_from(potential_matings, type=INTER_PIECES_LINK_TYPE)


    def build_graph(self):
        self._build_matching_graph()
        self._bulid_only_pieces_graph()
        self._build_adjacency_graph()
        self._build_filtered_matching_graph()
        self._build_filtered_adjacency_graph()
    

    def update_node(self,graph_name,node,att,val):
        graph = getattr(self,graph_name)
        graph.nodes[node][att] = val

    def assign_node(self,graph_name:str,node:str,local_assembly):
        graph = getattr(self,graph_name)

        if graph.nodes[node]["local_assembly"] is None:
            graph.nodes[node]["local_assembly"] = [local_assembly]
        else:
            graph.nodes[node]["local_assembly"].append(local_assembly)

    def dissociate_node(self,graph_name,node:str,local_assemly):
        graph = getattr(self,graph_name)

        if not graph.nodes[node]["local_assembly"] is None:
            if local_assemly in graph.nodes[node]["local_assembly"]:
                graph.nodes[node]["local_assembly"].remove(local_assemly)

                if len(graph.nodes[node]["local_assembly"]) == 0:
                    graph.nodes[node]["local_assembly"] = None

    def clear_unassigned_inter_links(self,graph_name,loops):
        graph = getattr(self,graph_name)
        links_to_remove = []

        for link in graph.edges(data=True):
            
            if link[2]["type"] != INTER_PIECES_LINK_TYPE:
                continue
            
            node1_assemblies = graph.nodes[link[0]]["local_assembly"]
            adj1 = [neighbor for neighbor in graph.adj[link[0]] if graph.edges[link[0],neighbor]["type"] == INTER_PIECES_LINK_TYPE]
            node2_assemblies = graph.nodes[link[1]]["local_assembly"]
            adj2 = [neighbor for neighbor in graph.adj[link[1]] if graph.edges[link[1],neighbor]["type"] == INTER_PIECES_LINK_TYPE]

            if node1_assemblies is None and node2_assemblies is None:
                continue
            elif node1_assemblies is None and len(node2_assemblies) == 1 and len(adj2) == 1:
                continue
            elif node2_assemblies is None and len(node1_assemblies) == 1 and len(adj1) == 1:
                continue
            else:
                
                is_to_remove = True

                for loop in loops:
                    if loop.is_link_present((link[0],link[1])):
                        is_to_remove = False 
                        break
                
                if is_to_remove:
                    links_to_remove.append(link)
    
        graph.remove_edges_from(links_to_remove)

    
    def get_mating(self,graph_name,node):
        '''
            deprecated
        '''
        graph = getattr(self,graph_name)

        for neighbor in graph.adj[node]:
            if graph.edges[node,neighbor]["type"] == INTER_PIECES_LINK_TYPE:
                return _link_to_mating((node,neighbor))

    def get_link_attributes(self,graph_name,link):
        graph = getattr(self,graph_name)
        return graph.edges[link]


    def get_matching_graph_nodes(self):
        return list(self.potential_matings_graph.nodes)

    def compute_max_weight_matching(self):
        self.matching =  list(nx.matching.max_weight_matching(self.potential_matings_graph,weight="compatibility"))

    def _get_piece2matings(self,matings_graph):
        piece2matings = {}

        for link in matings_graph.edges():
            piece1 = get_piece_name(link[0])
            piece2matings.setdefault(piece1,[])
            piece2 = get_piece_name(link[1])
            piece2matings.setdefault(piece2,[])
            mating = _link_to_mating(link)
            
            piece2matings[piece1].append(mating)
            piece2matings[piece2].append(mating)

        return piece2matings
    
    def get_piece2potential_matings(self):
        return self._get_piece2matings(self.potential_matings_graph)
    
    def get_piece2filtered_potential_matings(self):
        return self._get_piece2matings(self.filtered_potential_matings_graph)
        
    def _aggregate_matings_graph(self,mating_graph:nx.Graph,base_graph:nx.Graph,aggregates_matings:list)->nx.Graph:
        '''
            mating_graph - the graph to act on. it could be self.filtered_potential_matings_graph etc
            aggregates_matings - list of list of matings. each list represents a loop (cluster)
        '''
        agg_graph =  nx.Graph()
        agg_graph.add_nodes_from(base_graph.nodes)
        agg_graph.add_edges_from(base_graph.edges, type=WITHIN_PIECE_LINK_TYPE)
        # This line is should be computed outside the function?
        flat_mating_list = [mat for agg in aggregates_matings for mat in agg]
        occupied_nodes = set()

        for mating in flat_mating_list:
            node1 = name_node(mating.piece_1,mating.edge_1)
            occupied_nodes.add(node1)
            node2 = name_node(mating.piece_2,mating.edge_2)
            occupied_nodes.add(node2)
            agg_graph.add_edge(node1,node2,type=WITHIN_AGGREGATE_LINK_TYPE)


        for link in mating_graph.edges:
            
            if link in base_graph:
                continue
            
            node1 = link[0]
            node2 = link[1]

            if node1 in occupied_nodes or node2 in occupied_nodes:
                continue

            agg_graph.add_edge(node1,node2,type=INTER_AGGREGATE_LINK_TYPE)

        return agg_graph

    def compute_aggregated_filtered_pot_graph(self,aggregates_matings:list)->nx.Graph:
        '''
            DEPRECATED ?
        '''
        return self._aggregate_matings_graph(self.filtered_potential_matings_graph,
                                             self.pieces_only_graph,
                                             aggregates_matings)


    def compute_loops_graph(self,loops:list)->nx.Graph:
        agg_graph =  nx.Graph()
        agg_graph.add_nodes_from(self.pieces_only_graph.nodes)
        agg_graph.add_edges_from(self.pieces_only_graph.edges, type=WITHIN_PIECE_LINK_TYPE)

        num_loops = len(loops)

        for loop_i,loop in enumerate(loops):
            within_matings = loop.get_as_mating_list() # known interface (?)

            for mating in within_matings:
                node1 = name_node(mating.piece_1,mating.edge_1)
                node2 = name_node(mating.piece_2,mating.edge_2)
                
                agg_graph.add_edge(node1,node2,type=WITHIN_AGGREGATE_LINK_TYPE,
                                   debug=repr(loop),loop_index=loop_i,total_num_loops=num_loops) # for the repr I insisted to get loop as parameter... (and for the easy interface...)

            inter_matings = loop.get_availiable_matings() # known interface (?)

            for mating in inter_matings:
                node1 = name_node(mating.piece_1,mating.edge_1)
                node2 = name_node(mating.piece_2,mating.edge_2)
                agg_graph.add_edge(node1,node2,type=INTER_AGGREGATE_LINK_TYPE)

        return agg_graph

    def get_final_matings(self):
        final_matings = []

        for link in self.filtered_adjacency_graph.edges(data=True):

            if link[2]["type"] == INTER_PIECES_LINK_TYPE: #or link[2]["type"] == INTER_AGGREGATE_LINK_TYPE:
                final_matings.append(_link_to_mating((link[0],link[1])))
        
        return final_matings

def get_piece_name(node_name:str):
    # edge_name P_4_E_2
    return node_name.split("_")[1]

def get_edge_name(node_name:str):
    # edge_name P_4_E_2
    return node_name.split("_")[-1]

def _link_to_mating(link):
    '''
        link - an edge in potential_matings_graph e.g ("P_7_E_1","P_9_E_0")
    '''
    piece1 = get_piece_name(link[0])
    edge1 = int(get_edge_name(link[0]))
    piece2 = get_piece_name(link[1])
    edge2 = int(get_edge_name(link[1]))
    
    return Mating(piece_1=piece1,edge_1=edge1,piece_2=piece2,edge_2=edge2)


def name_node(piece_name,edge_name):
    '''
        same as _name_node but not an instance function
    '''
    return f"P_{piece_name}_E_{edge_name}"




def _construct_wrapper(pieces,id2piece:dict,geometric_match_edges=None,pictorial_matcher=None,compatibility_threshold=0.4):
    return MatchingGraphWrapper(pieces,id2piece,
                                geometric_match_edges=geometric_match_edges,
                                pictorial_matcher=pictorial_matcher,
                                compatibility_threshold=compatibility_threshold)

factory.register_builder(MatchingGraphWrapper.__name__,_construct_wrapper)