from src.solvers import Assembly,Solver
from src.feature_extraction.geometric import GeometricFeatureExtractor
from src.pairwise_matchers.geometric import GeometricPairwiseMatcher
import numpy as np
import networkx as nx
from src.data_structures.hierarchical_loops import ZeroLoop,Loop,Mating,ZeroLoopError


CIRCLE_DEGREES = 360

class GeometricNoiselessSolver(Solver):

    def __init__(self, pieces: list):
        super().__init__(pieces)
        self.geomteric_feature_extractor = GeometricFeatureExtractor()
        self.geometric_pairwiser = GeometricPairwiseMatcher()
        self.edges_mating_graph = None
        self.piece2matings = {}
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
    
    def _get_possible_matings(self):
        if self.edges_mating_graph is None:
            raise NotImplementedError("You need to call _compute_edges_mating_graph function first")
        
        edges_pairs = [ e for e in self.edges_mating_graph.edges if "RELS" in e[0] and "RELS" in e[1]]

        for pair in edges_pairs: #zip(edge_rels,edge_rels[1:] + [edge_rels[0]]):
            '''The convention of node of edge rels in the mating graph is the following:
            f"P_{piece.id}_RELS_E_{edge_index}"'''
            edge_prev,edge_next = pair[0],pair[1]
            split_prev = edge_prev.split("_")
            piece_1 = split_prev[1]
            edge_1 = split_prev[-1]
            split_next = edge_next.split("_")
            piece_2 = split_next[1]
            edge_2 = split_next[-1]

            if piece_1 == piece_2:
                continue

            mating = Mating(piece_1,edge_1,piece_2,edge_2)
            key_1 = f"P_{piece_1}"
            self.piece2matings.setdefault(key_1,[])
            
            if mating not in self.piece2matings[key_1]:
                self.piece2matings[key_1].append(mating) 
            
            key_2 = f"P_{piece_2}"
            self.piece2matings.setdefault(key_2,[])
            if mating not in self.piece2matings[key_2]:
                self.piece2matings[key_2].append(mating)


    def _loops_to_union(self,loops,num_mut_edges):
        
        # if not self.piece2matings:
        #     self.piece2matings = self._get_possible_matings()

        pairs_indexes = []

        for i in range(len(loops)):
            loop_i = loops[i]
            for j in range(i+1,len(loops)):
                loop_j = loops[j]

                if len(loop_i.get_mutual_pieces(loop_j)) == 0:
                    continue

                if loop_i.is_contained(loop_j) or loop_j.is_contained(loop_i):
                    continue

                '''Check here if the two loops have an availiable edge for match'''
                pass

                pairs_indexes.append((i,j))



                # mut_edges = loops[loop_i].mutual_mating_rels(loops[loop_j])
                # # if len(mut_edges) <= num_mut_edges*2 and len(mut_edges) > 0: # *2 because the edges are nodes and we looking for a link betwween two nodes
                # if len(mut_edges) >0 and len(mut_edges)%2==0: # *2 because the edges are nodes and we looking for a link betwween two nodes
                #     pairs_indexes.append((loop_i,loop_j))
                #     #print(f"Union {loops[loop_i]} and {loops[loop_j]}")        
        
        return pairs_indexes
    

    def _load_zeroloop(self,cycle:list,accumulated_angle_err=2):
        '''
        
        '''
        if self.edges_mating_graph is None:
            raise ValueError("You need to compute the edge mating graph first")

        edge_rels = [edge for edge in cycle if "RELS" in edge]
        pieces_involved_with_duplicates = [elm.split("_")[1] for elm in edge_rels] #P_<NUM_PIECE>_.....
        pieces_involved = []
        [pieces_involved.append(p) for p in pieces_involved_with_duplicates if p not in pieces_involved]
        
        if len(pieces_involved) <=2:
            raise ZeroLoopError("Loop must contain at least 3 pieces due to the convexity assumption")
        
        '''
            Since we assume the pieces are convex, in the hierchical loops they will appear only twice
        '''
        is_valid = True
        for piece_id in pieces_involved:
            if pieces_involved_with_duplicates.count(piece_id) != 2:
                is_valid = False
                break
        
        if not is_valid:
            raise ZeroLoopError("Loop is not valid, each piece must appear exactly twice. ")

        # self.mating_rels = edge_rels
        nodes_adj = [edge for edge in cycle if "_ADJ_" in edge]
        accumulated_angle = sum([self.edges_mating_graph.nodes[node]["angle"] for node in nodes_adj])
        
        if abs(CIRCLE_DEGREES-accumulated_angle) > accumulated_angle_err:
                raise ZeroLoopError(f"Zero loop must close a circle with at most {accumulated_angle_err} error")

        pieces_involved = pieces_involved # To save counter clockwise ordering
        piece2edge2matings = {}
        
        for edge_prev,edge_next in zip(edge_rels,edge_rels[1:] + [edge_rels[0]]):
            '''The convention of node of edge rels in the mating graph is the following:
            f"P_{piece.id}_RELS_E_{edge_index}"'''
            split_prev = edge_prev.split("_")
            piece_1 = split_prev[1]
            edge_1 = split_prev[-1]
            split_next = edge_next.split("_")
            piece_2 = split_next[1]
            edge_2 = split_next[-1]

            if piece_1 == piece_2:
                continue

            mating = Mating(piece_1=piece_1,edge_1=edge_1,piece_2=piece_2,edge_2=edge_2)
            key_p_1 = f"P_{piece_1}"
            piece2edge2matings.setdefault(key_p_1,{})
            piece2edge2matings[key_p_1][edge_1] = mating # Because each edge has only one mating in the loop

            key_p_2 = f"P_{piece_2}"
            piece2edge2matings.setdefault(key_p_2,{})
            piece2edge2matings[key_p_2][edge_2] = mating

        return Loop(piece2edge2matings)


    def _load_zero_loops(self,cycles_list):
        '''
            cycles_list
           
        '''
        zero_loops = []

        for cycle in cycles_list:
            try:
                loop = self._load_zeroloop(cycle)
                zero_loops.append(loop)
            except ZeroLoopError as ve:
                pass
        
        return zero_loops

    def _compute_cycles(self):
        #self._compute_edges_mating_graph()
        cycles = nx.simple_cycles(self.edges_mating_graph)
        return list(cycles)

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

