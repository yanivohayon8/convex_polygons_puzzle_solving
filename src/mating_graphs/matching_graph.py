import networkx as nx
from src.mating import Mating
from src.mating_graphs import factory

INTER_PIECES_EDGE_TYPE = "inter_piece"


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
        # self.filtered_adjaceny_graph = self.filtered_potential_matings_graph.copy()
        # self.filtered_adjaceny_graph.add_nodes_from(self.pieces_only_graph.nodes)
        # self.filtered_adjaceny_graph.add_edges_from(self.pieces_only_graph.edges, type="within_piece")
        
        self.filtered_adjacency_graph = nx.Graph()
        self.filtered_adjacency_graph.add_nodes_from(self.pieces_only_graph.nodes)
        self.filtered_adjacency_graph.add_edges_from(self.pieces_only_graph.edges, type="within_piece")
        potential_matings = [edge for edge in self.filtered_potential_matings_graph.edges if not edge in self.pieces_only_graph]
        self.filtered_adjacency_graph.add_edges_from(potential_matings, type="inter_piece")


    def build_graph(self):
        self._build_matching_graph()
        self._bulid_only_pieces_graph()
        self._build_adjacency_graph()
        self._build_filtered_matching_graph()
        self._build_filtered_adjacency_graph()
    
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
    
    def _compute_red_blue_360_loops_rec(self, visited, curr_node,computed_cycles:list, 
                                   accumulated_loop_angle=0,loop_angle_error=3):
        '''
            computes zero loops around a vertex 360 degrees.
            start_node: like P_7_E_1, from where to start the search
            curr_node: the current visited node. Calling the function for the first time put edge start_node->curr_node
            computed_cycles: a list initiated outside. It will contain all the cycles
        '''
        # print(f"\tVISITED: {visited}")

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
            # debug_is_acc_360 = abs(360-accumulated_loop_angle)<loop_angle_error
            # if debug_is_acc_360:
            #     computed_cycles.append(visited)
            # else:    
            #     pass
            #     # print("Debug:Problematic loop")

            return

        # if accumulated_loop_angle > 360+loop_angle_error:
        #     return
        
        prev_step = self.filtered_adjacency_graph[visited[-1]]
        prev_step_type = prev_step[curr_node]["type"]

        '''
            Because we pre-sorted the edges counterclock wise,
            to find a 360 loop, we sum the angles in clockwise direction.
            Remember, for an edge of a piece, it has two adjacent edges (within the piece)
            So we select the one of the right
        '''
        if prev_step_type == "inter_piece":
            curr_piece = get_piece_name(curr_node)
            curr_edge = int(get_edge_name(curr_node))
            # adjacent_edge = self.get_clockwise_adjacent_edge(curr_edge,curr_piece)#(curr_edge-1)%self.id2piece[curr_piece].get_num_coords()
            adjacent_edge = self.get_counter_clockwise_adjacent_edge(curr_edge,curr_piece)#(curr_edge-1)%self.id2piece[curr_piece].get_num_coords()
            neighbor = self._name_node(curr_piece,adjacent_edge)
            self._compute_red_blue_360_loops_rec(visited + [curr_node], neighbor,computed_cycles,
                                                accumulated_loop_angle=accumulated_loop_angle,loop_angle_error=loop_angle_error)
        elif prev_step_type == "within_piece":
            piece_name = get_piece_name(curr_node)
            edge_index_1 = int(get_edge_name(curr_node))
            edge_index_2 = int(get_edge_name(visited[-1]))
            inner_angle =  self.id2piece[piece_name].get_inner_angle(edge_index_1,edge_index_2)
            accumulated_loop_angle += inner_angle

            for neighbor in self.filtered_adjacency_graph.neighbors(curr_node):
                
                if neighbor in visited and neighbor != visited[0]:
                    continue
                
                next_step_type = self.filtered_adjacency_graph[curr_node][neighbor]["type"]
                
                if next_step_type == "inter_piece":
                    self._compute_red_blue_360_loops_rec(visited + [curr_node], neighbor,computed_cycles,
                                                    accumulated_loop_angle=accumulated_loop_angle,loop_angle_error=loop_angle_error)

    def compute_red_blue_360_loops(self,loop_angle_error=6):
        cycles_without_duplicates = []
        cycles_without_duplicates_sets = []

        def _compute_from_edge(visited,curr_node): #,cycles_without_duplicates:list,cycles_without_duplicates_sets:list
            new_cycles = []
            self._compute_red_blue_360_loops_rec(visited,curr_node,new_cycles,loop_angle_error=loop_angle_error)

            for cycle in new_cycles:
                cycle_set = set(cycle) 

                if  cycle_set not in cycles_without_duplicates_sets:
                    cycles_without_duplicates.append(cycle)
                    cycles_without_duplicates_sets.append(cycle_set)

        for inter_piece_link in self.filtered_potential_matings_graph.edges():

            graph_node1,graph_node2 = inter_piece_link
            piece_edge1 = int(get_edge_name(graph_node1))
            node_1_piece_id = get_piece_name(graph_node1)

            # piece_edge1_adj = self.get_counter_clockwise_adjacent_edge(piece_edge1,node_1_piece_id)
            piece_edge1_adj = self.get_clockwise_adjacent_edge(piece_edge1,node_1_piece_id)
            visited = [
                self._name_node(node_1_piece_id,piece_edge1_adj),
                graph_node1
            ]
            _compute_from_edge(visited,graph_node2) 

            piece_edge2 = int(get_edge_name(graph_node2))
            node_2_piece_id = get_piece_name(graph_node2)
            # piece_edge2_adj = self.get_counter_clockwise_adjacent_edge(piece_edge2,node_2_piece_id)
            piece_edge2_adj = self.get_clockwise_adjacent_edge(piece_edge2,node_2_piece_id)
            visited = [
                self._name_node(node_2_piece_id,piece_edge2_adj),
                graph_node2
            ]
            _compute_from_edge(visited,graph_node1) 

        return cycles_without_duplicates

    
        
    def compute_piece2potential_matings_dict(self):
        piece2potential_matings = {}

        for link in self.potential_matings_graph.edges():
            piece1 = get_piece_name(link[0])
            piece2potential_matings.setdefault(piece1,[])
            piece2 = get_piece_name(link[1])
            piece2potential_matings.setdefault(piece2,[])
            mating = _link_to_mating(link)
            
            piece2potential_matings[piece1].append(mating)
            piece2potential_matings[piece2].append(mating)

        return piece2potential_matings

    def get_clockwise_adjacent_edge(self,edge,piece_id):
        return (edge-1)%self.id2piece[piece_id].get_num_coords()
    
    def get_counter_clockwise_adjacent_edge(self,edge,piece_id):
        return (edge+1)%self.id2piece[piece_id].get_num_coords()



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



def _construct_wrapper(pieces,id2piece:dict,geometric_match_edges=None,pictorial_matcher=None,compatibility_threshold=0.4):
    return MatchingGraphWrapper(pieces,id2piece,
                                geometric_match_edges=geometric_match_edges,
                                pictorial_matcher=pictorial_matcher,
                                compatibility_threshold=compatibility_threshold)

factory.register_builder(MatchingGraphWrapper.__name__,_construct_wrapper)