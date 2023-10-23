from functools import reduce
from src.mating import Mating,convert_mating_to_vertex_mating


class ZeroLoopError(Exception):
    pass

class LoopUnionConflictError(Exception):
    pass

class Loop():
    
    def __init__(self,piece2edge2matings={},availiable_matings=[]) -> None:
        '''
            piece2edge2matings: a dictionary of dictionaries
            piece2edge2matings keys are the pieces ids and the values are dictionaries
            that map between edge id to occupied mating (We assume there is a one to one match between edges)
        '''
        self.piece2edge2matings = piece2edge2matings
        self.availible_matings = availiable_matings
        self.unions_history = [] # For Debug
        self.score = None
        self.matings_as_csv = "" # This is computed in get_loop_matings_as_csv below (the http body request)
    
    def set_score(self,score):
        self.score = score

    def set_matings_as_csv(self,string_lines):
        '''
        string_lines computed in get_loop_matings_as_csv below (the http body request)
        it is from the form:
        piece1,edge1,piece2,edge2
        '''
        self.matings_as_csv = string_lines
   
    def get_matings_as_csv(self):
        return self.matings_as_csv
                           

    def get_pieces_invovled(self):
        return self.piece2edge2matings.keys()

    def __repr__(self) -> str:
        pieces = sorted(self.get_pieces_invovled())
        # return reduce(lambda acc,x: f"{x}_"+acc,pieces,"")[:-1]
        return reduce(lambda acc,x: f"P_{x}_"+acc,pieces,"")[:-1]
        
    def get_mutual_pieces(self,loop):
        if isinstance(loop,Loop):
            return list(set(self.get_pieces_invovled()) & set(loop.get_pieces_invovled()))
    
    def is_contained(self,loop):
        if isinstance(loop,Loop):
            unmutual_pieces = list(set(self.get_pieces_invovled()) - set(loop.get_pieces_invovled()))
            return len(unmutual_pieces)==0 
    
    def copy(self):
        return Loop(self.piece2edge2matings.copy())

    def _get_piece_matings(self,piece_id):
        return self.piece2edge2matings[piece_id]
    
    def _set_piece_matings(self,piece_id,piece_mating:dict):
        self.piece2edge2matings[piece_id] = piece_mating

    def get_availiable_matings(self):
        return self.availible_matings

    def set_availiable_matings(self,availiable_matings:list):
        self.availible_matings = availiable_matings

    def get_mutual_availiable_matings(self,other_loop):
        return [mat for mat in self.get_availiable_matings() if mat in other_loop.get_availiable_matings()]


    def get_as_mating_list(self):
        matings = []

        for piece in self.piece2edge2matings.keys():
            curr_piece_matings = list(self.piece2edge2matings[piece].values())
            [matings.append(mat) for mat in curr_piece_matings if mat not in matings]
        
        return matings
    
    def insert_mating(self,mating:Mating):
        key_p_1 = f"{mating.piece_1}" #f"P_{piece_1}"
        self.piece2edge2matings.setdefault(key_p_1,{})
        self.piece2edge2matings[key_p_1][mating.edge_1] = mating # Because each edge has only one mating in the loop

        key_p_2 = f"{mating.piece_2}" #f"P_{piece_2}"
        self.piece2edge2matings.setdefault(key_p_2,{})
        self.piece2edge2matings[key_p_2][mating.edge_2] = mating
    
    def insert_availiable_mating(self,mating:Mating):
        if mating not in self.availible_matings:
            self.availible_matings.append(mating)

    def _mating_conflict(self,other_loop):
        '''
            The function looks for matings conflict with self loop and other_loop.
            I.e. for the same edge of a piece they have different assigments
            The function returns the confilct or None 
        '''
        mutual_pieces = self.get_mutual_pieces(other_loop)

        for piece_id in mutual_pieces:
            self_edge2matings = self._get_piece_matings(piece_id)
            other_edge2matings = other_loop._get_piece_matings(piece_id)

            for self_edge_id in self_edge2matings.keys():
                if self_edge_id in other_edge2matings.keys():                    
                    if not other_edge2matings[self_edge_id] == self_edge2matings[self_edge_id]:
                        return (self_edge2matings[self_edge_id],other_edge2matings[self_edge_id])
                    
        return None

    def union(self,other_loop):
        '''
            Unions between the self loop and another loop

            Deprecated function!
        '''

        if not isinstance(other_loop,Loop):
            raise TypeError("other_loop variable is expected to be of type Loop")
        
        if self.is_contained(other_loop) or other_loop.is_contained(self):
            mess = f"Tried to union between loop {repr(self)} and {repr(other_loop)} but the union does not results with a novel piece"
            raise LoopUnionConflictError(mess)

        mutual_pieces = self.get_mutual_pieces(other_loop)
        mutual_ava_matings = self.get_mutual_availiable_matings(other_loop)

        if len(mutual_pieces) == 0 and len(mutual_ava_matings) == 0:
            mess = f"Tried to union between loop {repr(self)} and {repr(other_loop)} but they don't have mutual pieces and potential mutual availiable matings"
            raise LoopUnionConflictError(mess)

        conflict = self._mating_conflict(other_loop)

        if conflict is not None:
            '''This should not happen when there is no noise'''
            mess = f"Conflict while trying to merge between loop {repr(self)} and loop {repr(other_loop)}."+\
                    f"The former loop assert the mating {repr(conflict[0])} " +\
                    f"while the latter {repr(conflict[1])}"
            raise LoopUnionConflictError(mess)
        
        new_loop = Loop(piece2edge2matings={},availiable_matings=[])
        
        self_matings = self.get_as_mating_list()
        other_matings = other_loop.get_as_mating_list()
        pieces_involved = []# 
        pieces_involved_with_duplicates = list(self.get_pieces_invovled()) + list(other_loop.get_pieces_invovled())
        [pieces_involved.append(piece) for piece in pieces_involved_with_duplicates if piece not in pieces_involved]

        for mat in self_matings+other_matings:
            new_loop.insert_mating(mat)

        for mat in self.get_availiable_matings() +other_loop.get_availiable_matings():
            
            if mat in mutual_ava_matings:
                if mat.piece_1 in pieces_involved and mat.piece_2 in pieces_involved:
                    new_loop.insert_mating(mat)
                    continue

            if mat in other_matings+self_matings:
                continue

            new_loop.insert_availiable_mating(mat)

        new_loop.unions_history.append((repr(self),repr(other_loop)))
        return new_loop
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other,Loop):
            if not (other.is_contained(self) and self.is_contained(other)):
                return False
            
            for piece in self.get_pieces_invovled():
                self_edge2mating = self._get_piece_matings(piece)
                other_edge2mating = other._get_piece_matings(piece)

                if self_edge2mating.keys() != other_edge2mating.keys():
                    return False
                
                for edge in self_edge2mating.keys():
                    if self_edge2mating[edge]!=other_edge2mating[edge]:
                        return False
                
                return True
            
        return False
         


def get_loop_matings_as_csv(loop:Loop,id2piece:dict):
    matings = loop.get_as_mating_list()
    matings_csv = reduce(lambda acc,mat: acc+convert_mating_to_vertex_mating(mat,id2piece[mat.piece_1],id2piece[mat.piece_2]),matings,"")
    loop.set_matings_as_csv(matings_csv)

    return matings_csv

# def get_loop_matings_as_csv(loop:Loop,id2piece:dict):
#     data = ""

#     for mating in loop.get_as_mating_list():
#         piece_1 = id2piece[mating.piece_1]
#         edge_1_index_before_ccw = piece_1.get_origin_index(mating.edge_1)
#         piece_1_vertex_1, piece_1_vertex_2 = piece_1.get_vertices_indices(edge_1_index_before_ccw)

#         piece_2 = id2piece[mating.piece_2]
#         edge_2_index_before_ccw = piece_2.get_origin_index(mating.edge_2)
#         piece_2_vertex_1, piece_2_vertex_2 = piece_2.get_vertices_indices(edge_2_index_before_ccw)

#         '''The following way of putting springs might be probelmatic'''
#         overlap_area,_,__ = piece_1.align_pieces_on_edge_and_compute_overlap_area(
#             piece_2,
#             [piece_1_vertex_1, piece_1_vertex_2],
#             [piece_2_vertex_1, piece_2_vertex_2])
        
#         overlap_area_opp,_,__ = piece_1.align_pieces_on_edge_and_compute_overlap_area(
#             piece_2,
#             [piece_1_vertex_1, piece_1_vertex_2],
#             [piece_2_vertex_2, piece_2_vertex_1])

#         epsilon = 1

#         if (overlap_area > epsilon and overlap_area_opp > epsilon) or \
#             (overlap_area < epsilon and overlap_area_opp < epsilon):
#             raise("Problematic transformation")

#         if overlap_area < epsilon:
#             data += f"{mating.piece_1},{piece_1_vertex_1},{mating.piece_2},{piece_2_vertex_1}\r\n"
#             data += f"{mating.piece_1},{piece_1_vertex_2},{mating.piece_2},{piece_2_vertex_2}\r\n"
#         else:
#             data += f"{mating.piece_1},{piece_1_vertex_1},{mating.piece_2},{piece_2_vertex_2}\r\n"
#             data += f"{mating.piece_1},{piece_1_vertex_2},{mating.piece_2},{piece_2_vertex_1}\r\n"

#     return data 