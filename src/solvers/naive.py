from src.solvers import Assembly,Solver
from src.feature_extraction.geometric import GeometricFeatureExtractor
from src.pairwise_matchers.geometric import GeometricPairwiseMatcher
import numpy as np
import networkx as nx
from src.data_structures.hierarchical_loops import ZeroLoop,Loop,MatingLink


class GeometricNoiselessSolver(Solver):

    def __init__(self, pieces: list):
        super().__init__(pieces)
        self.geomteric_feature_extractor = GeometricFeatureExtractor()
        self.geometric_pairwiser = GeometricPairwiseMatcher()
        self.edges_mating_graph = None
        self.zero_loops = []
        

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
    

    def _loops_to_union(self,loops,num_mut_edges):
        pairs_indexes = []

        for loop_i in range(len(loops)):
            for loop_j in range(loop_i+1,len(loops)):
                mut_edges = loops[loop_i].mutual_mating_rels(loops[loop_j])
                # if len(mut_edges) <= num_mut_edges*2 and len(mut_edges) > 0: # *2 because the edges are nodes and we looking for a link betwween two nodes
                if len(mut_edges) >0 and len(mut_edges)%2==0: # *2 because the edges are nodes and we looking for a link betwween two nodes
                    pairs_indexes.append((loop_i,loop_j))
                    #print(f"Union {loops[loop_i]} and {loops[loop_j]}")        
        
        return pairs_indexes
    
    def _load_zero_loops(self,cycles_list):
        zero_loops = []

        for cycle in cycles_list:
            try:
                loop = ZeroLoop(cycle)
                #print(loop.pieces_involved)
                zero_loops.append(loop)
            except ValueError as ve:
                pass
        
        return zero_loops

    def global_optimize(self):
        self._compute_edges_mating_graph()
        cycles = nx.simple_cycles(self.edges_mating_graph)
        list_cycles = list(cycles)
        loops = []
        
        # for cycle in list_cycles:
        #     rels_cy = [e for e in cycle if "RELS" in e]
        #     # if rels
        #     print(rels_cy)


        for cycle in list_cycles:
            try:
                loop = Loop()
                loop.load(cycle)
                #print(loop.pieces_involved)
                loops.append(loop)
            except ValueError as ve:
                pass
        
        err_angle = 2
        CIRCLE_DEGREES = 360
        valid_loops = []
        for loop in loops:
            accumulated_angle = loop.get_accumulated_angle(self.edges_mating_graph)
            if abs(CIRCLE_DEGREES-accumulated_angle) < err_angle:
                valid_loops.append(loop)
        
        for loop_i in range(len(valid_loops)):
            for loop_j in range(loop_i+1,len(valid_loops)):
                mut_edges = valid_loops[loop_i].mutual_mating_rels(valid_loops[loop_j])
                if len(mut_edges) > 0:
                    print(f"Union {valid_loops[loop_i]} and {valid_loops[loop_j]}")
            
        

                
        
            
        
      
                
                
            


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

