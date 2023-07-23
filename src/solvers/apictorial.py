from src.puzzle import Puzzle
from src.feature_extraction import geometric as geo_extractor 
from src.pairwise_matchers import geometric as geo_pairwiser
from src.edge_mating_graph import EdgeMatingGraph
from src.data_structures import Mating
from src.data_structures.zero_loops import ZeroLoopAroundVertexLoader
from src.data_structures.loop_merger import BasicLoopMerger
from src.my_http_client import HTTPClient
from src.data_structures.physical_assember import PhysicalAssembler
from src.data_structures.hierarchical_loops import get_loop_matings_as_csv


class FirstSolver():
    def __init__(self,puzzle:Puzzle,puzzle_image,puzzle_num,puzzle_noise_level) -> None:
        self.puzzle = puzzle
        self.puzzle_image = puzzle_image
        self.puzzle_num = puzzle_num
        self.puzzle_noise_level = puzzle_noise_level
        self.bag_of_pieces = None
        self.id2piece = {}
        #self.puzzle_directory = None
        self.mating_graph = None
        self.cycles = None
        self.piece2potential_matings = {}
        self.http = None
        self.physical_assembler = None

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
        self.edge_length_pairwiser.pairwise(self.puzzle.noise+1e-3)
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
        self.mating_graph = EdgeMatingGraph(self.bag_of_pieces)
        self.mating_graph.load_raw_cycles(self.puzzle.puzzle_directory+"/cycles.txt")
        self.cycles = self.mating_graph.find_cycles()
    
    def compute_cycles(self,is_save_cycles=True):
        self.mating_graph = EdgeMatingGraph(self.bag_of_pieces,
                                            self.edge_length_pairwiser.match_edges,
                                            self.edge_length_pairwiser.match_pieces_score)
        self.mating_graph.build_graph()
        self.mating_graph.compute_raw_cycles()

        if is_save_cycles:
            self.mating_graph.save_raw_cycles(self.puzzle.puzzle_directory+"/cycles.txt")
        
        self.cycles = self.mating_graph.find_cycles()

    def build_zero_loops(self):
        zero_loops_loader = ZeroLoopAroundVertexLoader(self.id2piece,self.cycles,self.piece2potential_matings)
        self.zero_loops = zero_loops_loader.load(0.5)

    def global_optimize(self):
        self.http = HTTPClient(self.puzzle_image,self.puzzle_num,self.puzzle_noise_level)
        self.physical_assembler = PhysicalAssembler(self.http, self.id2piece)
        merger = BasicLoopMerger()

        previous_loops = self.zero_loops   
        solutions = []
        
        while True:
            potential_next_level_loops = []
            debug_num_of_redundant_potential = 0

            for i in range(len(previous_loops)):
                loop_i = previous_loops[i]

                for j in range(i+1,len(previous_loops)):
                    loop_j = previous_loops[j]
                    new_loop = merger.merge(loop_i,loop_j)

                    if new_loop is not None:
                        if new_loop not in potential_next_level_loops:
                            matings_csv = get_loop_matings_as_csv(new_loop,self.id2piece)
                            new_loop.set_matings_as_csv(matings_csv)
                            response = self.physical_assembler.run(matings_csv)
                            new_loop.set_score(self.physical_assembler.score_assembly(response))
                            potential_next_level_loops.append(new_loop)
                        else:
                            debug_num_of_redundant_potential+=1
                    
            next_level_loops = []
            debug_total_num_potential_loops = len(previous_loops) * (len(previous_loops) - 1)/2 + 1e-5
            debug_percent_redundant = 100 * debug_num_of_redundant_potential/debug_total_num_potential_loops
            print(f"Found redundant potential loops {debug_percent_redundant}%")

            for loop in potential_next_level_loops:
                if len(loop.get_pieces_invovled())==len(self.bag_of_pieces):
                    if len(solutions) == 0:
                        solutions.append(loop)
                    else:
                        tmp = []
                        [tmp.append(lop) for lop in solutions if lop not in solutions]
                        solutions = solutions+tmp
                    continue
                
                if loop not in next_level_loops:
                    next_level_loops.append(loop)
            
            if len(next_level_loops) == 0:
                break

            previous_loops = next_level_loops

        solutions_as_mating = []
        for i,loop in enumerate(solutions):
            self.physical_assembler.run(loop.get_matings_as_csv(),screenshot_name=f"sol_{i}")
            solutions_as_mating.append(loop.get_as_mating_list())
         
        return solutions_as_mating
