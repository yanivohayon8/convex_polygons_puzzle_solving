import pandas as pd
from src.solvers import Assembly,Solver
from src.feature_extraction.geometric import GeometricFeatureExtractor
from src.pairwise_matchers.geometric import GeometricPairwiseMatcher
import numpy as np

class GeometricSolver(Solver):

    def __init__(self, pieces: list):
        super().__init__(pieces)

    def extract_features(self):
        super().extract_features()
        geomteric_extractor = GeometricFeatureExtractor()
        edges_lengths = []

        for i,piece in self.bag_of_pieces:
            coords = list(piece.polygon.exterior.coords)
            edges_lengths.append(geomteric_extractor.get_edges_lengths(coords))
        
        self.features["edges_lengths"] = edges_lengths #np.array(edges_lengths)
    
    def pairwise(self):
        geometric_pairwiser = GeometricPairwiseMatcher()
        geometric_pairwiser.pairwise_edges_lengths(self.features["edges_lengths"])
        

class DoNothing():
    
    def __init__(self,pieces:list):
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

        # df_adjacency_relations = pd.Dataframe({
        #     "pieceA":pieceAs,
        #     "pieceB":pieceBs,
        #     "edgeA":edge1s,
        #     "edgeB":edge2s
        # })
        df_adjacency_relations = None

        return Assembly(df_adjacency_relations,self.pieces)

