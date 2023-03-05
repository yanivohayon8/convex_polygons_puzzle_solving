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
        self.nodes_rels = edge_rels
        self.nodes_adj = [edge for edge in traversal if "_ADJ_" in edge]
        self.pieces_involved = pieces_involved_set
        
    
    def get_accumulated_angle(self,edges_mating_graph):
        return sum([edges_mating_graph.nodes[node]["angle"] for node in self.nodes_adj])


class SuperPiece():
    
    def __init__(self,inner_edges_indexes:dict,outer_edges_indexes:dict) -> None:
        self.inner_edges_indexes = inner_edges_indexes
        self.outer_edges_indexes = outer_edges_indexes
        pass

    def __repr__(self) -> str:
        _repr = ""
        for piece in self.outer_edges_indexes.keys():
            _repr = _repr + f"P{piece}_"
            for edge_index in self.outer_edges_indexes[piece]:
                _repr = _repr + f"e{edge_index}_"
        
        return _repr[:-1]
    
    def get_pieces_involved(self):
        return [int(_[1:]) for _ in self.__repr__().split("_") if _.startswith("P")]

    
    def get_mutual_pieces(self,super_piece):
        self_pieces = self.get_pieces_involved()
        super_piece_pieces = super_piece.get_pieces_involved()
        return list(set(self_pieces) & set(super_piece_pieces))

    # def union(self,super_piece,edges_mating,mutual_pieces=None):
    #     union_outer_edges = {}
    #     union_inner_edges = {}
         
    #     # Because we already computed it in the outer loop
    #     if mutual_pieces is None:
    #         mutual_pieces = self.get_mutual_pieces(super_piece)
        
    #     if len(mutual_pieces) == 0:
    #         raise ValueError("To union super pieces, they must have mutual elementary pieces")
   
    #     for basic_piece in self.inner_edges_indexes.keys():
    #         if basic_piece not in mutual_pieces:
    #             union_inner_edges[basic_piece] = self.inner_edges_indexes[basic_piece]

    #     for basic_piece in super_piece.inner_edges_indexes.keys():
    #         if basic_piece not in mutual_pieces:
    #             union_inner_edges[basic_piece] = super_piece.inner_edges_indexes[basic_piece]
        
    #     for basic_piece in self.outer_edges_indexes.keys():
    #         if basic_piece not in mutual_pieces:
    #             union_outer_edges[basic_piece] = self.outer_edges_indexes[basic_piece]
    #         # else:
    #         #     #union_outer_edges[basic_piece] = list(set(self.outer_edges_indexes[basic_piece])-set(union_inner_edges[basic_piece]))
    #         #     union_outer_edges[basic_piece] = list(set(self.outer_edges_indexes[basic_piece])-set(union_inner_edges[basic_piece]))

    #     for basic_piece in super_piece.outer_edges_indexes.keys():
    #         if basic_piece not in mutual_pieces:
    #             union_outer_edges[basic_piece] = super_piece.outer_edges_indexes[basic_piece]
    #         # else:
    #         #     union_outer_edges[basic_piece] = list(set(super_piece.outer_edges_indexes[basic_piece])-set(union_inner_edges[basic_piece]))
        
    #     for mut_piece in mutual_pieces:
    #         union_outer_edges[mut_piece] = list(set(super_piece.outer_edges_indexes[mut_piece]) & set(self.outer_edges_indexes[mut_piece]))

    #         if mut_piece in union_inner_edges.keys():
    #             union_outer_edges[mut_piece] = list(set(union_outer_edges[mut_piece])-set(union_inner_edges[mut_piece]))

    #     pieces_to_clean = [piece for piece in union_outer_edges.keys() if len(union_outer_edges[piece]) == 0]
    #     [union_outer_edges.pop(piece) for piece in pieces_to_clean]
        
    #     pieces_to_clean = [piece for piece in union_inner_edges.keys() if len(union_inner_edges[piece]) == 0]
    #     [union_inner_edges.pop(piece) for piece in pieces_to_clean]

    #     return SuperPiece(union_inner_edges,union_outer_edges)
        


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

    def _union(self,super_piece_1:SuperPiece,super_piece_2:SuperPiece):
        union_outer_edges = {}
        union_inner_edges = {}
         
        # Because we already computed it in the outer loop
        #if mutual_pieces is None:
        mutual_pieces = super_piece_1.get_mutual_pieces(super_piece_2)
        
        if len(mutual_pieces) == 0:
            raise ValueError("To union super pieces, they must have mutual elementary pieces")
   
        for basic_piece in super_piece_1.inner_edges_indexes.keys():
            if basic_piece not in mutual_pieces:
                union_inner_edges[basic_piece] = super_piece_1.inner_edges_indexes[basic_piece].copy()

        for basic_piece in super_piece_2.inner_edges_indexes.keys():
            if basic_piece not in mutual_pieces:
                union_inner_edges[basic_piece] = super_piece_2.inner_edges_indexes[basic_piece].copy()
        
        for basic_piece in super_piece_1.outer_edges_indexes.keys():
            if basic_piece not in mutual_pieces:
                union_outer_edges[basic_piece] = super_piece_1.outer_edges_indexes[basic_piece].copy()

        for basic_piece in super_piece_2.outer_edges_indexes.keys():
            if basic_piece not in mutual_pieces:
                union_outer_edges[basic_piece] = super_piece_2.outer_edges_indexes[basic_piece].copy()
        
        for mut_piece in mutual_pieces:
            union_outer_edges[mut_piece] = list(set(super_piece_2.outer_edges_indexes[mut_piece]) & set(super_piece_1.outer_edges_indexes[mut_piece])).copy()

            if mut_piece in union_inner_edges.keys():
                union_outer_edges[mut_piece] = list(set(union_outer_edges[mut_piece])-set(union_inner_edges[mut_piece])).copy()


        ''' Detecting False positive in the outer ring of the new piece'''
        # This might be calculated beforehand when loading the superpieces
        edges_mating = [mate for mate in self.edges_mating_graph.edges if "ENV" not in mate[0] and "ENV" not in mate[1]]
        union_outer_edges_copy = union_outer_edges.copy()

        for mate in edges_mating:
            mate_1_splitted = mate[0].split("_")
            piece_1 = int(mate_1_splitted[1])
            mate_2_splitted = mate[1].split("_")
            piece_2 = int(mate_2_splitted[1])

            if piece_1 in union_outer_edges.keys() and piece_2 in union_outer_edges.keys():
                for e1 in union_outer_edges[piece_1]:
                    for e2 in union_outer_edges[piece_2]:
                        if (f"P_{piece_1}_RELS_E_{e1}",f"P_{piece_2}_RELS_E_{e2}") in edges_mating or \
                            (f"P_{piece_2}_RELS_E_{e2}",f"P_{piece_1}_RELS_E_{e1}") in edges_mating:
                            union_outer_edges_copy[piece_1].remove(e1)
                            union_outer_edges_copy[piece_2].remove(e2)
                

        union_outer_edges = union_outer_edges_copy
        
        pieces_to_clean = [piece for piece in union_outer_edges.keys() if len(union_outer_edges[piece]) == 0]
        [union_outer_edges.pop(piece) for piece in pieces_to_clean]
        
        pieces_to_clean = [piece for piece in union_inner_edges.keys() if len(union_inner_edges[piece]) == 0]
        [union_inner_edges.pop(piece) for piece in pieces_to_clean]
        
        return SuperPiece(union_inner_edges,union_outer_edges)
    
    def _union_super_piece(self,super_pieces):
        new_pieces = []
        for i in range(len(super_pieces)-1):
            super_1 = super_pieces[i]
            for j in range(i+1,len(super_pieces)):
                super_2 = super_pieces[j]
                if j == i:
                    continue
                
                try:
                    new_piece = self._union(super_1,super_2)
                    new_pieces.append(new_piece)
                    print("Union pieces:")
                    print(super_1)
                    print("AND")
                    print(super_2)
                    print("result:")
                    print(new_piece)
                    print()
                except ValueError as ve:
                    pass
        return new_pieces

    def global_optimize(self):
        self._compute_edges_mating_graph()
        cycles = nx.simple_cycles(self.edges_mating_graph)
        list_cycle = list(cycles)
        loops = []

        for cycle in list_cycle:
            try:
                loop = Loop(cycle)
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
        
        super_pieces = []

        for loop in valid_loops:
            pieces2edges_not_looped = {}
            pieces2edges_looped = {}

            for edge_rel in loop.nodes_rels:
                _ = edge_rel.split("_") #"P_<PIECE_INDEX>_RELS_E_<EDGE_INDEX>"
                piece_index = int(_[1])
                piece_key = piece_index #f"P_{piece_index}"
                edge_index = int(_[4])

                if piece_key not in pieces2edges_not_looped.keys():
                    pieces2edges_not_looped[piece_key] = list(range(len(self.pieces[piece_index].coordinates)))
                    pieces2edges_looped[piece_key] = []

                pieces2edges_not_looped[piece_key].remove(edge_index)
                pieces2edges_looped[piece_key].append(edge_index)

            super_pieces.append(SuperPiece(pieces2edges_looped,pieces2edges_not_looped))
            
        
        #print("Super pieces:")
        #print(super_pieces,sep="\n")
        #print()

        phase1_pieces = self._union_super_piece(super_pieces)
        phase2 = self._union_super_piece(phase1_pieces)
        print(phase2)
        # new_pieces = []
        # for i in range(len(super_pieces)-1):
        #     super_1 = super_pieces[i]
        #     for j in range(i+1,len(super_pieces)):
        #         super_2 = super_pieces[j]
        #         if j == i:
        #             continue
                
        #         try:
        #             new_piece = self._union(super_1,super_2)
        #             new_pieces.append(new_piece)
        #             print("Union pieces:")
        #             print(super_1)
        #             print("AND")
        #             print(super_2)
        #             print("result:")
        #             print(new_piece)
        #             print()
        #         except ValueError as ve:
        #             pass

                
        
            
        
      
                
                
            


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

