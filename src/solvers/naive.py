from src.solvers import Assembly,Solver
from src.feature_extraction.geometric import GeometricFeatureExtractor
from src.pairwise_matchers.geometric import GeometricPairwiseMatcher
import numpy as np
import networkx as nx


class GeometricNoiselessSolver(Solver):

    def __init__(self, pieces: list):
        super().__init__(pieces)
        self.geomteric_feature_extractor = GeometricFeatureExtractor()
        self.geometric_pairwiser = GeometricPairwiseMatcher()
        self.edges_mating_graph = None

    def extract_features(self):
        super().extract_features()
        self.features["edges_lengths"] = []
        self.features["pieces_degree"] = []

        for piece in self.pieces:
            coords = piece.get_coords() #list(piece.polygon.exterior.coords)
            # self.features["edges_lengths"].append(self.geomteric_feature_extractor.get_polygon_edges_lengths(coords))
            # self.features["pieces_degree"].append(len(coords)-1)
            piece.features["edges_lengths"] = self.geomteric_feature_extractor.get_polygon_edges_lengths(coords)
            piece.features["poly_degree"] = len(coords)-1
            piece.features["angles"] = self.geomteric_feature_extractor.get_polygon_angles(np.array(coords))
        
        #self.features["edges_lengths"] = edges_lengths #np.array(edges_lengths)
    
    def pairwise(self):        
        edges_lengths = [piece.features["edges_lengths"] for piece in self.pieces]
        self.geometric_pairwiser.pairwise_edges_lengths(edges_lengths,confidence_interval=1)
        pass

    def compute_edges_mating_graph(self):
        self.edges_mating_graph = nx.DiGraph()
        pieces_angles = []

        '''
            For create an loop we need to step through a edge that corresponds to the current edge
            and then to step into one its neighbors (adjacent edge). 
            So for each edge we have rels that from it out a links to a potential mating.
            and enviorment that describes the enviorment of the edge.
        '''

        for piece in self.pieces:
            coords = piece.get_coords()
            
            self.edges_mating_graph.add_nodes_from(
                [f"P_{piece.id}_RELS_E_{edge_index}" for edge_index in range(len(coords))]
            )

        for piece in self.pieces:
            angles = piece.features["angles"]
            for edge_index in range(len(angles)):
                central_edge = f"P_{piece.id}_ENV_{edge_index}"
                adj_edge_1 = f"P_{piece.id}_ENV_{edge_index}_ADJ_{(edge_index-1)%len(coords)}"
                adj_edge_2 = f"P_{piece.id}_ENV_{edge_index}_ADJ_{(edge_index+1)%len(coords)}"

                self.edges_mating_graph.add_nodes_from([central_edge,adj_edge_1,adj_edge_2])
                angle_1 = angles[(edge_index)%len(angles)]
                angle_2 = angles[(edge_index+1)%len(angles)]
                self.edges_mating_graph.add_edges_from(
                    [
                    (central_edge,adj_edge_1,{'weight': angle_1}),
                    (central_edge,adj_edge_2,{'weight': angle_2}),
                    (adj_edge_1,f"P_{piece.id}_RELS_E_{adj_edge_1}"),
                    (adj_edge_2,f"P_{piece.id}_RELS_E_{adj_edge_2}")
                    ]
                )
        
        num_pieces = len(self.pieces)
        for piece_i in range(num_pieces):
            #for piece_j in range(piece_i+1,num_pieces):
            for piece_j in range(num_pieces):
                mating_edges = self.geometric_pairwiser.match_edges[piece_i,piece_j]
                if len(mating_edges)>0:
                    mating_edges = mating_edges[0] # In refactor make this not necessary
                    new_links = [
                        (f"P_{self.pieces[piece_i].id}_RELS_E_{mating[0]}",f"P_{self.pieces[piece_j].id}_RELS_E_{mating[1]}") \
                                for mating in mating_edges]
                    self.edges_mating_graph.add_edges_from(new_links)

        
    def global_optimize(self):
        cycles = nx.simple_cycles(self.edges_mating_graph)
        print(sorted(cycles))
        pass




        #for piece_index in range(num_pieces):
        #    


        # accumulated_angle = 180
        # #for i_row in range()
        # row_i = 0
        # num_pieces = len(self.pieces)
        # curr_match_pieces = [col_i for col_i in range(num_pieces) if self.geometric_pairwiser.match_edges[row_i,col_i] !=[]]
        # next_piece = curr_match_pieces[0]
        # match_edges = self.geometric_pairwiser.match_edges[row_i,next_piece]
        # # because we don't know the orientation of the piece
        # next_edge_in_loop_1 = int(match_edges[0][0][1]+1)%(self.features["pieces_degree"][next_piece])
        # next_edge_in_loop_2 = int(match_edges[0][0][1]-1)%(self.features["pieces_degree"][next_piece])
        
        # curr_match_pieces_copy = [col_i for col_i in range(num_pieces)\
        #                           if self.geometric_pairwiser.match_edges[next_piece,col_i] !=[]]
        # print(self.geometric_pairwiser.match_edges[next_piece,2])

        pass
            
                
                
            


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

