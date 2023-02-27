from src.solvers import Assembly,Solver
from src.feature_extraction.geometric import GeometricFeatureExtractor
from src.pairwise_matchers.geometric import GeometricPairwiseMatcher
import numpy as np
import networkx as nx


class Loop():
    
    def __init__(self,traversal) -> None:
        edge_rels = [edge for edge in traversal if "RELS" in edge]
        pieces_involved = [elm.split("_")[1] for elm in edge_rels] #P_<NUM_PIECE>_.....
        pieces_involved_set = set(pieces_involved)
        
        if len(pieces_involved_set) <=2:
            raise ValueError("Loop must contain at least 3 pieces due to the convexity assumption")
        
        '''
            Since we assume the pieces are convex, in the hierchical loops they will appear only twice
        '''
        is_valid = True
        for piece_id in pieces_involved_set:
            if pieces_involved.count(piece_id) != 2:
                is_valid = False
                break
        if not is_valid:
            raise ValueError("Loop is not valid, each piece must appear exactly twice. ")

        self.traversal = traversal
        self.edge_rels = edge_rels
        self.pieces_involved = pieces_involved_set
    
    def get_accumulated_angle(self,mating_graph_edges):
        pass


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

    def _compute_edges_mating_graph(self):
        self.edges_mating_graph = nx.DiGraph()
        pieces_angles = []

        '''
            For create an loop we need to step through a edge that corresponds to the current edge
            and then to step into one its neighbors (adjacent edge). 
            So for each edge we have rels that from it out a links to a potential mating.
            and enviorment that describes the enviorment of the edge.
        '''

        for piece in self.pieces:
            coords = piece.get_coords()[:-1]
            
            self.edges_mating_graph.add_nodes_from(
                [f"P_{piece.id}_RELS_E_{edge_index}" for edge_index in range(len(coords))]
            )

        for piece in self.pieces:
            angles = piece.features["angles"]
            for edge_index in range(len(angles)):
                central_edge = f"P_{piece.id}_ENV_{edge_index}"

                '''Since the polygons are oriented counter clockwise (ccw) than we need to check only one adjacent edge (and not both)'''
                adj_edge_index = (edge_index+1)%len(angles)
                adj_edge = f"P_{piece.id}_ENV_{edge_index}_ADJ_{adj_edge_index}"
                angle = angles[(edge_index+1)%len(angles)]
                
                self.edges_mating_graph.add_nodes_from(
                    [central_edge,(adj_edge,{"angle":angle})]
                )

                self.edges_mating_graph.add_edges_from(
                    [
                    (central_edge,adj_edge,{'angle': angle}),
                    (f"P_{piece.id}_RELS_E_{edge_index}",central_edge),
                    (adj_edge,f"P_{piece.id}_RELS_E_{adj_edge_index}")
                    ]
                )
        
        num_pieces = len(self.pieces)
        for piece_i in range(num_pieces):
            for piece_j in range(num_pieces):
                mating_edges = self.geometric_pairwiser.match_edges[piece_i,piece_j]
                if len(mating_edges)>0:
                    mating_edges = mating_edges[0] # In refactor make this not necessary
                    new_links = [
                        (f"P_{self.pieces[piece_i].id}_RELS_E_{mating[0]}",f"P_{self.pieces[piece_j].id}_RELS_E_{mating[1]}") \
                                for mating in mating_edges]
                    self.edges_mating_graph.add_edges_from(new_links)


    def _filter_unvalid_loops(self,cycles):
        pass

    def global_optimize(self):
        self._compute_edges_mating_graph()
        cycles = nx.simple_cycles(self.edges_mating_graph)
        list_cycle = list(cycles)
        valid_loops = []

        for cycle in list_cycle:
            try:
                loop = Loop(cycle)
                print(loop.pieces_involved)
                valid_loops.append(valid_loops)
            except ValueError as ve:
                pass

        valid_loops = self._filter_unvalid_loops(list_cycle)
        print(self.edges_mating_graph.edges[('P_0_ENV_1', 'P_0_ENV_1_ADJ_2')]["angle"])
        print(valid_loops)
      
                
                
            


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

