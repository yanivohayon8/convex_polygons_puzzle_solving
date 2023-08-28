from src.puzzle import Puzzle
from src.feature_extraction import geometric as geo_extractor 
from src.pairwise_matchers import geometric as geo_pairwiser
from src.mating_graphs.matching_graph import MatchingGraphWrapper,get_piece_name,get_edge_name
from src.mating import Mating,convert_mating_to_vertex_mating
from src.data_structures.zero_loops import ZeroLoopTwoEdgesPerPiece,ZeroLoopAroundVertexLoader
from src.data_structures.loop_merger import BasicLoopMerger,LoopMutualPiecesMergeError,LoopMergeError
from src.my_http_client import HTTPClient
from src.data_structures.physical_assember import PhysicalAssembler
from src.data_structures.hierarchical_loops import get_loop_matings_as_csv
from src.assembly import Assembly
from functools import reduce
from src.mating_graphs.cycle import Cycle
from src.feature_extraction.extrapolator.lama_masking import LamaEdgeExtrapolator
from src.pairwise_matchers.pictorial import NaiveExtrapolatorMatcher



class ZeroLoops360Solver():
    def __init__(self,puzzle:Puzzle,db,puzzle_num,puzzle_noise_level) -> None:
        self.puzzle = puzzle
        self.db = db
        self.puzzle_num = puzzle_num
        self.puzzle_noise_level = puzzle_noise_level
        self.bag_of_pieces = None
        self.pictorial_matcher = None
        self.mating_graph_wrapper = None
        self.http = HTTPClient(self.db,self.puzzle_num,self.puzzle_noise_level)
        self.physical_assembler = PhysicalAssembler(self.http)
        self.id2piece = {}
        self.piece2potential_matings = {}
        self.merger = BasicLoopMerger()
    
    def load_bag_of_pieces(self):
        self.puzzle.load()
        self.bag_of_pieces = self.puzzle.get_bag_of_pieces()

        for piece in self.bag_of_pieces:
            self.id2piece[piece.id] = piece
            piece.load_extrapolated_image()

    def extract_features(self):
        edge_length_extractor = geo_extractor.EdgeLengthExtractor(self.bag_of_pieces)
        edge_length_extractor.run()

        angles_extractor = geo_extractor.AngleLengthExtractor(self.bag_of_pieces)
        angles_extractor.run()

        lama_extractor = LamaEdgeExtrapolator(self.bag_of_pieces)
        lama_extractor.run()

    def pairwise(self):
        self.edge_length_pairwiser = geo_pairwiser.EdgeMatcher(self.bag_of_pieces)
        self.edge_length_pairwiser.pairwise(self.puzzle.matings_max_difference+1e-3)

        self.pictorial_matcher = NaiveExtrapolatorMatcher(self.bag_of_pieces)
        self.pictorial_matcher.pairwise()
    
    def build_mating_graph(self):
        self.mating_graph_wrapper = MatchingGraphWrapper(self.bag_of_pieces,self.id2piece,
                                                self.edge_length_pairwiser.match_edges,
                                                self.edge_length_pairwiser.match_pieces_score,
                                                pictorial_matcher=self.pictorial_matcher)
        self.mating_graph_wrapper.build_graph()
    
    def build_zero_loops(self):
        loop_angle_error = self.puzzle_noise_level *  1.5 #1#1.5 # this is not a good heuristic

        graph_cycles = self.mating_graph_wrapper.compute_red_blue_360_loops(loop_angle_error=loop_angle_error)
        self.cycles = [Cycle(debug_graph_cycle=graph_cycle) for graph_cycle in graph_cycles]

        self.piece2potential_matings = self.mating_graph_wrapper.compute_piece2potential_matings_dict()
        zero_loops_loader = ZeroLoopTwoEdgesPerPiece(self.id2piece,self.cycles,self.piece2potential_matings)
        self.zero_loops = zero_loops_loader.load(None)# 

        return self.zero_loops

    def global_optimize(self,is_debug_loops=False):
        loops_scores = []

        for i,zero_loop in enumerate(self.zero_loops):
            # matings_csv = get_loop_matings_as_csv(zero_loop,self.id2piece)
            matings = zero_loop.get_as_mating_list()
            matings_csv = reduce(lambda acc,mat: acc+convert_mating_to_vertex_mating(mat,self.id2piece[mat.piece_1],self.id2piece[mat.piece_2]),matings,"")
            zero_loop.set_matings_as_csv(matings_csv)
            screenhost_name = ""#f"level_{0}_loop_{i}" # ""
            response = self.physical_assembler.run(matings_csv,screenshot_name=screenhost_name)
            score = self.physical_assembler.score_assembly(response)
            zero_loop.set_score(score)
            loops_scores.append(score)

        loops = self.zero_loops 

        # TODO: implement wrapping mechanism here to union loops (When we will have larger puzzles)

        loops_ranked = [loop for _,loop in sorted(zip(loops_scores,loops))]

        if is_debug_loops:
            for i,curr_loop in enumerate(loops_ranked):
                matings = curr_loop.get_as_mating_list()
                matings_csv = reduce(lambda acc,mat: acc+convert_mating_to_vertex_mating(mat,self.id2piece[mat.piece_1],self.id2piece[mat.piece_2]),matings,"")
                screenhost_name = f"rank_{i+1}"#f"level_{0}_loop_{i}" # ""
                self.physical_assembler.run(matings_csv,screenshot_name=screenhost_name)

        # merged_loop = loops_ranked[0]
        merged_loops = [loops_ranked[0]]
        first_detected_solution = None

        for i,curr_loop in enumerate(loops_ranked[1:]):
            print(f"Try to merge the {i+2}-th loop")
            is_merged = False
            loops_merge_with_curr_loop = []

            for i,mer_lop in enumerate(merged_loops):
                try:
                    print(f"Try to Merge {curr_loop} into {mer_lop}")
                    merged_res = self.merger.merge(mer_lop,curr_loop)
                    print(f"Suceed")
                    is_merged = True
                    loops_merge_with_curr_loop.append(merged_res)

                except LoopMutualPiecesMergeError as e:
                    # This loop doesnot have a common pieces with other loops
                    # so, merge it for later...
                    pass
                except LoopMergeError as e:
                    # print(e)
                    pass
            
            if is_merged:
                merged_loops_tmp = []
                for lop1 in loops_merge_with_curr_loop:
                    
                    for lop2 in merged_loops:
                        if not lop2.is_contained(lop1):
                            merged_loops_tmp.append(lop2)

                    merged_loops_tmp.append(lop1)

                merged_loops = merged_loops_tmp

                merged_loops_tmp = []
                for lop1 in merged_loops:
                    for lop2 in merged_loops:
                        if lop1 != lop2:
                            try:
                                result = self.merger.merge(lop1,lop2)
                                merged_loops_tmp.append(result)
                            except LoopMutualPiecesMergeError as e:
                                if lop2 not in merged_loops_tmp:
                                    merged_loops_tmp.append(lop2)
                            except LoopMergeError as e:
                                if lop2 not in merged_loops_tmp:
                                    merged_loops_tmp.append(lop2)
                merged_loops = merged_loops_tmp   
            else:
                merged_loops.append(curr_loop)

            for lop in merged_loops:
                if len(lop.get_pieces_invovled()) == len(self.bag_of_pieces):
                    first_detected_solution = lop
                    break
            

        screenshot_name = f"Solution {self.__class__.__name__}"
        matings = first_detected_solution.get_as_mating_list()
        matings_csv = reduce(lambda acc,mat: acc+convert_mating_to_vertex_mating(mat,self.id2piece[mat.piece_1],self.id2piece[mat.piece_2]),matings,"")
        response = self.physical_assembler.run(matings_csv,screenshot_name=screenshot_name)
        score = self.physical_assembler.score_assembly(response)
        print("Final merged loop scoring.....",score)
        solution_polygons = self.physical_assembler.get_final_coordinates_as_polygons(response)

        return Assembly(solution_polygons,matings)
