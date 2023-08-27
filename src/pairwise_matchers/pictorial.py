import numpy as np


class ExtrapolatorMatcher():
    
    def __init__(self,pieces) -> None:
        self.pieces = pieces
        self.total_num_edges = 0
        self.edge2pieceid = {}
        self.local_index2global_index = {}
        edge_i = 0

        for piece in pieces:
            num_coords = piece.get_num_coords()

            for edge in range(num_coords):
                self.edge2pieceid[edge_i] = piece.id
                self.local_index2global_index[f"{piece.id}-{edge}"] = edge_i
                edge_i+=1

            self.total_num_edges+= num_coords

        self.matching_edges_scores = np.zeros((self.total_num_edges,self.total_num_edges))
    
    def _score_pair(self,edge1,edge2):
        return 0

    def pairwise(self):
        for edge_i in range(self.total_num_edges):
            for edge_j in range(self.total_num_edges):
            
                if self.edge2pieceid[edge_i] == self.edge2pieceid[edge_j]:
                    continue
                
                self.matching_edges_scores[edge_i,edge_j] = self._score_pair(edge_i,edge_j)

    def get_score(self,piece1,edge1,piece2,edge2):
        global_index1 = self.local_index2global_index[f"{piece1}-{edge1}"]
        global_index2 = self.local_index2global_index[f"{piece2}-{edge2}"]
        return self.matching_edges_scores[global_index1,global_index2] 



