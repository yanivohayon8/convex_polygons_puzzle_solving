import numpy as np


class ExtrapolatorMatcher():
    
    def __init__(self,pieces) -> None:
        self.pieces = pieces
        self.total_num_edges = 0
        self.edge2pieceid = {}
        self.edge2piece_index = {}
        self.local_index2global_index = {}
        self.global_index2local_index = {}
        edge_i = 0

        for piece_i,piece in enumerate(pieces):
            num_coords = piece.get_num_coords()

            for edge in range(num_coords):
                self.edge2pieceid[edge_i] = piece.id
                self.local_index2global_index[f"{piece.id}-{edge}"] = edge_i
                self.edge2piece_index[edge_i] = piece_i
                self.global_index2local_index[edge_i] = edge
                edge_i+=1

            self.total_num_edges+= num_coords

        self.matching_edges_scores = np.zeros((self.total_num_edges,self.total_num_edges))
    
    def _score_pair(self,edge1_content:np.array,edge2_content:np.array):
        assert edge1_content.shape[1] == 3
        assert edge2_content.shape[1] == 3

        small = edge2_content
        big = edge1_content

        if edge1_content.shape[0] < edge2_content.shape[0]:
            small = edge1_content
            big = edge2_content
        
        length_diff = big.shape[0]-small.shape[0]
        right_padd_size = length_diff//2
        left_padd_size = length_diff//2

        if length_diff%2==1:
            right_padd_size+=1

        small_padded = np.pad(small,((left_padd_size,right_padd_size),(0,0)),constant_values=0)

        # A temporary score I found to avoid as possible
        # from numerical instabiility
        return np.linalg.norm(big-small_padded)

    def pairwise(self):
        for edge1_i in range(self.total_num_edges):
            for edge2_j in range(self.total_num_edges):
            
                if self.edge2pieceid[edge1_i] == self.edge2pieceid[edge2_j]:
                    continue

                piece1_i = self.edge2piece_index[edge1_i]
                edge1_local_i = self.global_index2local_index[edge1_i]
                edge1_content = self.pieces[piece1_i].features["edges_extrapolated_lama"][edge1_local_i]

                piece2_j = self.edge2piece_index[edge2_j]
                edge2_local_j = self.global_index2local_index[edge2_j]
                edge2_content = self.pieces[piece2_j].features["edges_extrapolated_lama"][edge2_local_j]
                
                self.matching_edges_scores[edge1_i,edge2_j] = self._score_pair(edge1_content,edge2_content)

    def get_score(self,piece1,edge1,piece2,edge2):
        global_index1 = self.local_index2global_index[f"{piece1}-{edge1}"]
        global_index2 = self.local_index2global_index[f"{piece2}-{edge2}"]
        return self.matching_edges_scores[global_index1,global_index2] 



