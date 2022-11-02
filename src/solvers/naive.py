import pandas as pd
from solvers import Assembly


class Concater():
    
    def __init__(self,pieces):
        self.pieces = pieces


    '''we need an option of live stream video of the assembly for debugging'''
    def run(self):
        edge_index = 1
        pieceAs = []
        pieceBs = []
        edge1s = []
        edge2s = []
        for piece_index in range(len(self.pieces)-1):
            pieceAs.append(self.pieces[piece_index])
            pieceBs.append(self.pieces[piece_index+1])
            edge1s.append(edge_index%2)
            edge2s.append((edge_index+1)%2)

        df_adjacency_relations = pd.Dataframe({
            "pieceA":pieceAs,
            "pieceB":pieceBs,
            "edgeA":edge1s,
            "edgeB":edge2s
        })

        # eihhhssss:
        df_locations = pd.read_csv("data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0/ground_truth_puzzle.csv") 
        return Assembly(df_adjacency_relations,df_locations)
        # return an object of "assembly that will be very similar to puzzle (or rather the same)?"