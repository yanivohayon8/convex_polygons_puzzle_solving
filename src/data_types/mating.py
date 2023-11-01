

class Mating():
    '''
        A relationship between two mating (match) edges
        piece_1: The piece id of edge 1 
        edge_1: edge 1 id 
        piece_2: The piece of edge 2
        edge_2: edge 2 id
    '''
    def __init__(self,**kwargs) -> None:

        if "repr_string" in kwargs.keys():
            '''Look at the __repr__ function '''
            repr_splited = kwargs["repr_string"].split("_")
            self.piece_1 = repr_splited[1]
            self.edge_1 = repr_splited[3].split("<")[0]
            self.piece_2 = repr_splited[-3]
            self.edge_2 = repr_splited[-1]
        else:
        #(piece_1:str, edge_1:str, piece_2:str,edge_2:str)
            self.piece_1 = kwargs["piece_1"]
            self.edge_1 = kwargs["edge_1"]
            self.piece_2 = kwargs["piece_2"]
            self.edge_2 = kwargs["edge_2"]

    def __repr__(self) -> str:
        return f"P_{self.piece_1}_e_{self.edge_1}<--->P_{self.piece_2}_e_{self.edge_2}"

    def __eq__(self, other) -> bool:
        if isinstance(other, Mating):
            exact_match = self.piece_1 == other.piece_1 and self.piece_2 == other.piece_2\
                  and self.edge_1==other.edge_1 and self.edge_2==other.edge_2
            flip_match = self.piece_1 == other.piece_2 and self.piece_2 == other.piece_1 \
                and self.edge_1==other.edge_2 and self.edge_2==other.edge_1
            return (exact_match or flip_match)

        return False
    
def convert_mating_to_vertex_mating(mating:Mating,piece_1,piece_2):
    '''
        Select the right vertex pairing to send for the spring simulation.
        Send it correctly, there are two possible transformations, select the one without overlap
    '''
    data = ""

    edge_1_index_before_ccw = piece_1.get_origin_index(mating.edge_1)
    piece_1_vertex_1, piece_1_vertex_2 = piece_1.get_vertices_indices(edge_1_index_before_ccw)

    edge_2_index_before_ccw = piece_2.get_origin_index(mating.edge_2)
    piece_2_vertex_1, piece_2_vertex_2 = piece_2.get_vertices_indices(edge_2_index_before_ccw)

    '''The following way of putting springs might be probelmatic'''
    overlap_area,_,__ = piece_1.align_pieces_on_edge_and_compute_overlap_area(
        piece_2,
        [piece_1_vertex_1, piece_1_vertex_2],
        [piece_2_vertex_1, piece_2_vertex_2])
    
    overlap_area_opp,_,__ = piece_1.align_pieces_on_edge_and_compute_overlap_area(
        piece_2,
        [piece_1_vertex_1, piece_1_vertex_2],
        [piece_2_vertex_2, piece_2_vertex_1])

    epsilon = 1

    if (overlap_area > epsilon and overlap_area_opp > epsilon) or \
        (overlap_area < epsilon and overlap_area_opp < epsilon):
        raise("Problematic transformation")

    if overlap_area < epsilon:
        data += f"{mating.piece_1},{piece_1_vertex_1},{mating.piece_2},{piece_2_vertex_1}\r\n"
        data += f"{mating.piece_1},{piece_1_vertex_2},{mating.piece_2},{piece_2_vertex_2}\r\n"
    else:
        data += f"{mating.piece_1},{piece_1_vertex_1},{mating.piece_2},{piece_2_vertex_2}\r\n"
        data += f"{mating.piece_1},{piece_1_vertex_2},{mating.piece_2},{piece_2_vertex_1}\r\n"

    return data 