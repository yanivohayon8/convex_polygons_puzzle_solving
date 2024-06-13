from typing import Any
from networkx import Graph as nxGraph
from src.mating_graphs.matching_graph import get_edge_name,get_piece_name,name_node,INTER_PIECES_LINK_TYPE
from src.mating_graphs import factory as graph_factory
from src import shared_variables 



def compute(graph:nxGraph):
    cycles = []

    for inter_piece_link in graph.edges(data=True):

        if inter_piece_link[2]["type"] == INTER_PIECES_LINK_TYPE:
            graph_node1 = inter_piece_link[0]
            graph_node2 = inter_piece_link[1]
            piece_edge1 = int(get_edge_name(graph_node1))
            node_1_piece_id = get_piece_name(graph_node1)

            piece_edge1_adj = shared_variables.puzzle.id2piece[node_1_piece_id].get_clockwise_adjacent_edge(piece_edge1)
            visited = [
                name_node(node_1_piece_id,piece_edge1_adj),
                graph_node1
            ]

            new_cycles = []
            _compute_from(graph,visited,graph_node2,new_cycles,visited_pieces=list())
            [cycles.append(cycle) for cycle in new_cycles if cycle not in cycles]
                    
    return cycles 

def _compute_from(graph:nxGraph,visited, curr_node,
                    computed_cycles:list, visited_pieces=[],max_num_visited=20):
    '''
        TODO: fill this documentation...
        start_node: like P_7_E_1, from where to start the search
        curr_node: the current visited node. Calling the function for the first time put edge start_node->curr_node
        computed_cycles: a list initiated outside. It will contain all the cycles
    '''
    
    if len(visited)==2:
        piece_name = get_piece_name(visited[-1])
        visited_pieces.append(piece_name)

    if len(visited) == max_num_visited:
        return

    if curr_node == visited[0]:
        
        if len(visited_pieces) > 2:
            curr_cycle = graph_factory.create("Cycle",debug_graph_cycle=visited)
            computed_cycles.append(curr_cycle)

        return
    
    prev_step_type = graph[visited[-1]][curr_node]["type"]

    '''
        Because we pre-sorted the edges counterclock wise,
        to find a 360 loop, we sum the angles in clockwise direction.
        Remember, for an edge of a piece, it has two adjacent edges (within the piece)
        So we select the one of the right
    '''
    if prev_step_type == "inter_piece":
        curr_piece = get_piece_name(curr_node)
        curr_edge = int(get_edge_name(curr_node))
        adjacent_edge = shared_variables.puzzle.id2piece[curr_piece].get_counter_clockwise_adjacent_edge(curr_edge)
        neighbor = name_node(curr_piece,adjacent_edge)
        visited_piece_tmp = visited_pieces+[curr_piece]
        _compute_from(graph,visited + [curr_node], neighbor,computed_cycles,
                            visited_pieces=visited_piece_tmp)
        
    elif prev_step_type == "within_piece":

        for neighbor in graph.neighbors(curr_node):
            
            if neighbor in visited and neighbor != visited[0]:
                continue
            
            neighbor_piece = get_piece_name(neighbor)

            if neighbor_piece in visited_pieces and neighbor != visited[0]:
                continue

            next_step_type = graph[curr_node][neighbor]["type"]
            
            if next_step_type == "inter_piece":
                _compute_from(graph,visited + [curr_node], neighbor,
                                    computed_cycles,visited_pieces=visited_pieces)
                
