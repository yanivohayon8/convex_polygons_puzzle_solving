from src.data_structures.hierarchical_loops import Loop

class PhysicalAssembler():

    def __init__(self,http,id2piece) -> None:
        self.http = http
        self.id2piece = id2piece
    
    def _generate_payload_body(self,loop:Loop):
        data = ""

        for mating in loop.get_as_mating_list():
            piece_1 = self.id2piece[mating.piece_1]
            edge_1_index_before_ccw = piece_1.get_origin_index(mating.edge_1)
            piece_1_vertex_1, piece_1_vertex_2 = piece_1.get_vertices_indices(edge_1_index_before_ccw)

            piece_2 = self.id2piece[mating.piece_2]
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

    def phyiscal_assembly(self, loop):
        body = self._generate_payload_body(loop)
        response = self.http.send_reconstruct_request(body)
        return response