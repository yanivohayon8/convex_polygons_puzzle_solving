from src.solvers import Assembly,Solver
from src.feature_extraction.geometric import GeometricFeatureExtractor
from src.pairwise_matchers.geometric import GeometricPairwiseMatcher
import numpy as np
import networkx as nx
from src.data_structures.hierarchical_loops import Loop,ZeroLoopError,LoopUnionConflictError
from src.data_structures import Mating

CIRCLE_DEGREES = 360

class GeometricNoiselessSolver(Solver):

    def __init__(self, pieces: list):
        super().__init__(pieces)
        self.geomteric_feature_extractor = GeometricFeatureExtractor()
        self.geometric_pairwiser = GeometricPairwiseMatcher()
        self.edges_mating_graph = None
        self.piece2matings = {}
        self.cycles = []  # For debug (For questioning when testing)
        self.zero_loops = [] # For debug (For questioning when testing)

    def extract_features(self):
        super().extract_features()
        self.features["edges_lengths"] = []
        self.features["pieces_degree"] = []

        for piece in self.pieces:
            coords = piece.get_coords() 
            piece.features["edges_lengths"] = self.geomteric_feature_extractor.get_polygon_edges_lengths(coords)
            piece.features["poly_degree"] = len(coords)-1
            piece.features["angles"] = self.geomteric_feature_extractor.get_polygon_angles(np.array(coords))
            
    def pairwise(self):        
        edges_lengths = [piece.features["edges_lengths"] for piece in self.pieces]
        self.geometric_pairwiser.pairwise_edges_lengths(edges_lengths,confidence_interval=1)
        pass

    def _compute_edges_mating_graph(self):
        '''
            Computes the mating graph (direct graph) between edges. 
            It was design in the following way to allow the nx package to find zero loops.
            Each edge has the following nodes in the graphs:
            1. Relationships node. P_{piece.id}_RELS_E_{edge_index}: a node that represents the pairwise matching of the edge.
                 It has links (edges in the mating graph) to other edges that pairwise it
            2. P_{piece.id}_ENV_{edge_index}: it has in a in-link to relationship node and out link to two nodes that represent adjacent edge to it.
            3. P_{piece.id}_ENV_{edge_index}_ADJ_{adj_edge_index}: represent an edge that adjacent to another edge. the link from the type 2 to this type has weight with the value of the angle.        
        '''

        if self.edges_mating_graph is not None:
            return

        self.edges_mating_graph = nx.DiGraph()

        for piece in self.pieces:
            coords = piece.get_coords()
            
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
                    for mat_edge in mating_edges:
                        new_links = [
                            (f"P_{self.pieces[piece_i].id}_RELS_E_{mating[0]}",f"P_{self.pieces[piece_j].id}_RELS_E_{mating[1]}") \
                                    for mating in mat_edge]
                        self.edges_mating_graph.add_edges_from(new_links)
    
    def _load_pieces_matings(self):
        '''
            This function load the data to the dict from self.piece2matingsfrom the pairwiser object
            It maps between pieces id to a list of its pairwise...
        '''
        num_pieces = len(self.pieces)

        for piece_i in range(num_pieces):
            piece_i_id = self.pieces[piece_i].id
            self.piece2matings.setdefault(piece_i_id,[])
            for piece_j in range(piece_i+1,num_pieces):
                mating_edges = self.geometric_pairwiser.match_edges[piece_i,piece_j]
                if len(mating_edges)>0:
                    piece_j_id = self.pieces[piece_j].id
                    self.piece2matings.setdefault(piece_j_id,[])
                    for mat_edge in mating_edges:
                        for mating in mat_edge:
                            new_mate = Mating(piece_1=piece_i_id,piece_2=piece_j_id,edge_1=mating[0],edge_2=mating[1])
                            self.piece2matings[piece_i_id].append(new_mate)
                            self.piece2matings[piece_j_id].append(new_mate)

    def _load_single_zeroloop(self,cycle:list,accumulated_angle_err=0.5):
        '''
            Construct a zero loop. 
            cycle: list that describe a cycle in the edge_mating_graph
            accumulated_angle_err: the loop must close a circle of 360 of mating pieces. 
                if a noise is implemented than it will close it with an error.
            The method checks if it can initialize a valid loop at first. 
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

        nodes_adj = [edge for edge in cycle if "_ADJ_" in edge]
        accumulated_angle = sum([self.edges_mating_graph.nodes[node]["angle"] for node in nodes_adj])
        
        if abs(CIRCLE_DEGREES-accumulated_angle) > accumulated_angle_err:
                raise ZeroLoopError(f"Zero loop must close a circle with at most {accumulated_angle_err} error")

        occupied_matings = []
        new_loop = Loop(piece2edge2matings={},availiable_matings=[])

        for edge_prev,edge_next in zip(edge_rels,edge_rels[1:] + [edge_rels[0]]):
            '''The convention of node of edge rels in the mating graph is the following:
            f"P_{piece.id}_RELS_E_{edge_index}"'''
            split_prev = edge_prev.split("_")
            piece_1 = split_prev[1]
            edge_1 = eval(split_prev[-1])
            split_next = edge_next.split("_")
            piece_2 = split_next[1]
            edge_2 = eval(split_next[-1])

            if piece_1 == piece_2:
                continue

            mating = Mating(piece_1=piece_1,edge_1=edge_1,piece_2=piece_2,edge_2=edge_2)
            new_loop.insert_mating(mating)
            occupied_matings.append(mating)

        # availiable_matings = []

        for piece in new_loop.get_pieces_invovled():
            for mat in self.piece2matings[piece]:

                if mat not in occupied_matings:
                    new_loop.insert_availiable_mating(mat)
                    #availiable_matings.append(mat)
            
        # new_loop.set_availiable_matings(availiable_matings)

        return new_loop

    def _load_zero_loops(self):
        '''
            cycles: a list of cycles that computed from self.edge_mating_graph
                a cycle is a list of strings (each represent a node in the graph)

            It loads to self.zero_loops the zero loops

            First, make sure you run self._compute_cycles
        '''
        self.zero_loops = []

        for cycle in self.cycles:
            try:
                loop = self._load_single_zeroloop(cycle)
                self.zero_loops.append(loop)
            except ZeroLoopError as ve:
                pass
        
        pieces_zero_looped = [piece_id for loop in self.zero_loops for piece_id in loop.get_pieces_invovled()]
        pieces_not_zero_looped = [piece.id for piece in self.pieces if piece.id not in pieces_zero_looped]
        
        for piece_id in pieces_not_zero_looped:
            new_loop = Loop(piece2edge2matings={piece_id:{}},availiable_matings=[])
            [new_loop.insert_availiable_mating(mat) for mat in self.piece2matings[piece_id]]
            self.zero_loops.append(new_loop)
    
    def _compute_next_level_loops(self,loops:list):
        next_level_loops = []

        for i in range(len(loops)):
            loop_i = loops[i]
            for j in range(i+1,len(loops)):
                loop_j = loops[j]

                try:
                    new_loop = loop_i.union(loop_j)
                    next_level_loops.append(new_loop)
                except LoopUnionConflictError:
                    pass

        return next_level_loops
    
    def _compute_cycles(self,cycles=None):
        if cycles is None:
            self._compute_edges_mating_graph()
            self.cycles = list(nx.simple_cycles(self.edges_mating_graph))
        else:
            self.cycles = cycles

    def global_optimize(self,cycles=None):
        self._load_pieces_matings()
        self._compute_cycles(cycles)
        self._load_zero_loops()
        
        previous_level_loops = self.zero_loops
        level = 1
        solutions = []
        loop_history_debug = [] # for debug

        while True:
            next_level_loops_raw = self._compute_next_level_loops(previous_level_loops)
            next_level_loops = []

            for lop in next_level_loops_raw:

                if len(lop.get_pieces_invovled())==len(self.pieces):
                    if len(solutions) == 0:
                        solutions.append(lop)
                    else:
                        tmp = []
                        [tmp.append(lop) for lop in solutions if lop not in solutions]
                        solutions = solutions+tmp
                    continue
                
                if lop not in next_level_loops:
                    next_level_loops.append(lop)

            
            if len(next_level_loops) == 0:
                break
            
            loop_history_debug.append(next_level_loops)
            previous_level_loops = next_level_loops
            level+=1
            # print(end="\n\n\n\n")
        
        solutions_as_mating = [loop.get_as_mating_list() for loop in solutions]

        return solutions_as_mating
        
        
        

            
        

                
        
            
        
      
                
                
            


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

