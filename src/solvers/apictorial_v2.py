from src.puzzle import Puzzle
from src.feature_extraction import geometric as geo_extractor 
from src.pairwise_matchers import geometric as geo_pairwiser
from src.mating_graphs.matching_graph import MatchingGraphWrapper,get_piece_name,get_edge_name
from src.mating import Mating,convert_mating_to_vertex_mating
from src.data_structures.zero_loops import ZeroLoopAroundVertexLoader
from src.data_structures.loop_merger import BasicLoopMerger,LoopMutualPiecesMergeError,LoopMergeError
from src.my_http_client import HTTPClient
from src.data_structures.physical_assember import PhysicalAssembler
from src.data_structures.hierarchical_loops import get_loop_matings_as_csv
from src.assembly import Assembly
from functools import reduce
from src.mating_graphs.cycle import Cycle


class ZeroLoops360Solver():
    def __init__(self,puzzle:Puzzle,puzzle_image,puzzle_num,puzzle_noise_level) -> None:
        self.puzzle = puzzle
        self.puzzle_image = puzzle_image
        self.puzzle_num = puzzle_num
        self.puzzle_noise_level = puzzle_noise_level
        self.bag_of_pieces = None
        self.mating_graph_wrapper = None
        self.http = HTTPClient(self.puzzle_image,self.puzzle_num,self.puzzle_noise_level)
        self.physical_assembler = PhysicalAssembler(self.http)
        self.id2piece = {}
        self.piece2potential_matings = {}
        self.merger = BasicLoopMerger()
    
    def load_bag_of_pieces(self):
        self.puzzle.load()
        self.bag_of_pieces = self.puzzle.get_bag_of_pieces()

        for piece in self.bag_of_pieces:
            self.id2piece[piece.id] = piece

    def extract_features(self):
        edge_length_extractor = geo_extractor.EdgeLengthExtractor(self.bag_of_pieces)
        edge_length_extractor.run()

        angles_extractor = geo_extractor.AngleLengthExtractor(self.bag_of_pieces)
        angles_extractor.run()

    def pairwise(self):
        self.edge_length_pairwiser = geo_pairwiser.EdgeMatcher(self.bag_of_pieces)
        self.edge_length_pairwiser.pairwise(self.puzzle.matings_max_difference+1e-3)
    
    def build_mating_graph(self):
        self.mating_graph_wrapper = MatchingGraphWrapper(self.bag_of_pieces,self.id2piece,
                                                self.edge_length_pairwiser.match_edges,
                                                self.edge_length_pairwiser.match_pieces_score)
        self.mating_graph_wrapper.build_graph()
    
    def build_zero_loops(self):
        loop_angle_error= self.puzzle_noise_level * 2.5

        graph_cycles = self.mating_graph_wrapper.compute_red_blue_360_loops(loop_angle_error=loop_angle_error)
        self.cycles = []

        def insert_mating_to_cycle(prev_node,next_node,piece2occurence:dict,matings_chain:list):
            mating = self.mating_graph_wrapper._link_to_mating((prev_node,next_node))
            matings_chain.append(mating)

            prev_piece = get_piece_name(prev_node)
            piece2occurence.setdefault(prev_piece,0)
            piece2occurence[prev_piece]+=1
            next_piece = get_piece_name(next_node)
            piece2occurence.setdefault(next_piece,0)
            piece2occurence[next_piece]+=1

        for graph_cycle in graph_cycles:
            piece2occurence = {}
            matings_chain = []
            for prev_node,next_node in zip(graph_cycle[1:-1:2],graph_cycle[2::2]):
                insert_mating_to_cycle(prev_node,next_node,piece2occurence,matings_chain)
            
            insert_mating_to_cycle(graph_cycle[-1],graph_cycle[0],piece2occurence,matings_chain)
            self.cycles.append(Cycle(matings_chain,piece2occurence,graph_cycle))

        self.piece2potential_matings = self.mating_graph_wrapper.compute_piece2potential_matings_dict()
        zero_loops_loader = ZeroLoopAroundVertexLoader(self.id2piece,self.cycles,self.piece2potential_matings)
        self.zero_loops = zero_loops_loader.load(loop_angle_error) 

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
            for i,loop in enumerate(loops_ranked):
                matings = loop.get_as_mating_list()
                matings_csv = reduce(lambda acc,mat: acc+convert_mating_to_vertex_mating(mat,self.id2piece[mat.piece_1],self.id2piece[mat.piece_2]),matings,"")
                screenhost_name = f"loop_ranked_{i+1}"#f"level_{0}_loop_{i}" # ""
                self.physical_assembler.run(matings_csv,screenshot_name=screenhost_name)

        merged_loop = loops_ranked[0]
        queued_loops = []
        queued_loops_tmp = []

        for i,loop in enumerate(loops_ranked[1:]):
            print(f"Try to merge loop {i+2}")
            try:
                queued_loops_tmp = []
                for qued_loop in queued_loops:
                    try:
                        print(f"Try to Merge {loop} into {merged_loop}")
                        self.merger.merge(merged_loop,qued_loop)
                        print(f"Suceed")
                    except LoopMutualPiecesMergeError as e:
                        queued_loops_tmp.append(qued_loop)
                    except LoopMergeError as e:
                        print(e)
                        pass
                
                queued_loops = queued_loops_tmp
                queued_loops_tmp.clear()

                print(f"Try to Merge {loop} into {merged_loop}")
                merged_loop = self.merger.merge(merged_loop,loop)
                print(f"Suceed")

            except LoopMutualPiecesMergeError as e:
                # This loop doesnot have a common pieces with other loops
                # so, merge it for later...
                queued_loops.append(loop)
            except LoopMergeError as e:
                print(e)
                pass

        screenshot_name = f"Solution {self.__class__.__name__}"
        matings = merged_loop.get_as_mating_list()
        matings_csv = reduce(lambda acc,mat: acc+convert_mating_to_vertex_mating(mat,self.id2piece[mat.piece_1],self.id2piece[mat.piece_2]),matings,"")
        response = self.physical_assembler.run(matings_csv,screenshot_name=screenshot_name)
        score = self.physical_assembler.score_assembly(response)
        print("Final merged loop scoring.....",score)
        solution_polygons = self.physical_assembler.get_final_coordinates_as_polygons(response)

        return Assembly(solution_polygons,matings)
