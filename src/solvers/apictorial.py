from src.puzzle import Puzzle
from src.feature_extraction import geometric as geo_extractor 
from src.pairwise_matchers import geometric as geo_pairwiser
from src.mating_graphs.inter_env_graph import InterEnvGraph
from src.mating_graphs.matching_graph import MatchingGraphWrapper
from src.mating import Mating,convert_mating_to_vertex_mating
from src.data_structures.zero_loops import ZeroLoopAroundVertexLoader
from src.data_structures.loop_merger import BasicLoopMerger,LoopMergeError
from src.my_http_client import HTTPClient
from src.data_structures.physical_assember import PhysicalAssembler
from src.data_structures.hierarchical_loops import get_loop_matings_as_csv
from src.assembly import Assembly
from functools import reduce

class FirstSolver():
    def __init__(self,puzzle:Puzzle,db,puzzle_num,puzzle_noise_level) -> None:
        self.puzzle = puzzle
        self.db = db
        self.puzzle_num = puzzle_num
        self.puzzle_noise_level = puzzle_noise_level
        self.bag_of_pieces = None
        self.id2piece = {}
        #self.puzzle_directory = None
        self.mating_graph = None
        self.cycles = None
        self.piece2potential_matings = {}
        # self.http = None
        # self.physical_assembler = None

        self.http = HTTPClient(self.db,self.puzzle_num,self.puzzle_noise_level)
        self.physical_assembler = PhysicalAssembler(self.http)#PhysicalAssembler(self.http, self.id2piece)
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
        num_pieces = len(self.bag_of_pieces)

        for piece_i in range(num_pieces):
            piece_i_id = self.bag_of_pieces[piece_i].id
            self.piece2potential_matings.setdefault(piece_i_id,[])
            for piece_j in range(piece_i+1,num_pieces):
                mating_edges = self.edge_length_pairwiser.match_edges[piece_i,piece_j]
                if len(mating_edges)>0:
                    piece_j_id = self.bag_of_pieces[piece_j].id
                    self.piece2potential_matings.setdefault(piece_j_id,[])
                    for mat_edge in mating_edges:
                        for mating in mat_edge:
                            new_mate = Mating(piece_1=piece_i_id,piece_2=piece_j_id,edge_1=mating[0],edge_2=mating[1])
                            self.piece2potential_matings[piece_i_id].append(new_mate)
                            self.piece2potential_matings[piece_j_id].append(new_mate)

    def load_cycles(self):
        '''
            For deterministric runs...
        '''
        self.mating_graph = InterEnvGraph(self.bag_of_pieces)
        self.mating_graph.load_raw_cycles(self.puzzle.puzzle_directory+"/cycles.txt")
        self.cycles = self.mating_graph.find_cycles()
    
    def build_mating_graph(self):
        self.mating_graph = InterEnvGraph(self.bag_of_pieces,
                                    self.edge_length_pairwiser.match_edges,
                                    self.edge_length_pairwiser.match_pieces_score)
        self.mating_graph.build_graph()

    def compute_cycles(self,is_save_cycles=True):
        self.mating_graph.compute_raw_cycles(max_length_cycle=2*len(self.bag_of_pieces)) #

        if is_save_cycles:
            self.mating_graph.save_raw_cycles(self.puzzle.puzzle_directory+"/cycles.txt")
        
        self.cycles = self.mating_graph.find_cycles()

    def build_zero_loops(self):
        zero_loops_loader = ZeroLoopAroundVertexLoader(self.id2piece,self.cycles,self.piece2potential_matings)
        self.zero_loops = zero_loops_loader.load(0.5)

    def global_optimize(self):
        previous_loops = self.zero_loops   
        solutions_loops = []
        loop_level = 0
        
        for i,zero_loop in enumerate(self.zero_loops):
            matings_csv = get_loop_matings_as_csv(zero_loop,self.id2piece)
            zero_loop.set_matings_as_csv(matings_csv)
            screenhost_name = ""#f"level_{loop_level}_loop_{i}"
            response = self.physical_assembler.run(matings_csv,screenshot_name=screenhost_name)
            zero_loop.set_score(self.physical_assembler.score_assembly(response))


        while True:
            loop_level+=1
            print(f"Start computing {loop_level}-loops")
            potential_next_level_loops = []
            debug_num_of_redundant_potential = 0

            for i in range(len(previous_loops)):
                loop_i = previous_loops[i]

                for j in range(i+1,len(previous_loops)):
                    loop_j = previous_loops[j]
                    try:
                        new_loop = self.merger.merge(loop_i,loop_j)

                        if new_loop is not None:
                            if new_loop not in potential_next_level_loops:
                                matings_csv = get_loop_matings_as_csv(new_loop,self.id2piece)
                                new_loop.set_matings_as_csv(matings_csv)
                                screenshot_name=""#f"level_{loop_level}_loop_{i}_loop_{j}"
                                response = self.physical_assembler.run(matings_csv,screenshot_name=screenshot_name)
                                new_loop.set_score(self.physical_assembler.score_assembly(response))
                                potential_next_level_loops.append(new_loop)
                            else:
                                debug_num_of_redundant_potential+=1
                    except LoopMergeError:
                        pass
                    
            next_level_loops = []
            debug_total_num_potential_loops = len(previous_loops) * (len(previous_loops) - 1)/2 + 1e-5
            debug_percent_redundant = 100 * debug_num_of_redundant_potential/debug_total_num_potential_loops
            print(f"Found redundant potential loops {debug_percent_redundant}%")

            for loop in potential_next_level_loops:
                if len(loop.get_pieces_invovled())==len(self.bag_of_pieces):
                    if len(solutions_loops) == 0:
                        solutions_loops.append(loop)
                    else:
                        tmp = []
                        [tmp.append(lop) for lop in solutions_loops if lop not in solutions_loops]
                        solutions_loops = solutions_loops+tmp
                    continue
                
                if loop not in next_level_loops:
                    next_level_loops.append(loop)
            
            if len(next_level_loops) == 0:
                break

            previous_loops = next_level_loops

        final_solutions = []
        for i,loop in enumerate(solutions_loops):
            res = self.physical_assembler.run(loop.get_matings_as_csv(),screenshot_name=f"sol_{i}")
            polygons = self.physical_assembler.get_final_coordinates_as_polygons(res)
            final_solutions.append(Assembly(polygons,loop.get_as_mating_list()))
         
        return final_solutions




class GraphMatchingSolver():

    def __init__(self,puzzle:Puzzle,db,puzzle_num,puzzle_noise_level) -> None:
        self.puzzle = puzzle
        self.db = db
        self.puzzle_num = puzzle_num
        self.puzzle_noise_level = puzzle_noise_level
        self.bag_of_pieces = None
        self.mating_graph = None
        self.http = HTTPClient(self.db,self.puzzle_num,self.puzzle_noise_level)
        self.physical_assembler = PhysicalAssembler(self.http)
        self.id2piece = {}
        #self.piece2potential_matings = {}
    
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
        self.mating_graph = MatchingGraphWrapper(self.bag_of_pieces,self.id2piece,
                                                self.edge_length_pairwiser.match_edges,
                                                self.edge_length_pairwiser.match_pieces_score)
        
        self.mating_graph.build_graph()

    def global_optimize(self):
        
        matings = self.mating_graph.find_matching()
        matings_csv = reduce(lambda acc,mat: acc+convert_mating_to_vertex_mating(mat,self.id2piece[mat.piece_1],self.id2piece[mat.piece_2]),matings,"")

        screenshot_name = "Matching_1"
        response = self.physical_assembler.run(matings_csv,screenshot_name=screenshot_name)
        score = self.physical_assembler.score_assembly(response)
        print("Loop scoring.....",score)

        solution_polygons = self.physical_assembler.get_final_coordinates_as_polygons(response)
        solution = Assembly(solution_polygons,matings)
        
        return solution
        

    def run(self,is_debug=False):
        self.load_bag_of_pieces()
        self.extract_features()
        self.pairwise()
        self.build_mating_graph()
        
        solution = self.global_optimize()
        
        return solution

        
        
