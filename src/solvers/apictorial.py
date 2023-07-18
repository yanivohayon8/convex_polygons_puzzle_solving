from src.puzzle import Puzzle
from src.feature_extraction import geometric as geo_extractor 
from src.pairwise_matchers import geometric as geo_pairwiser
from src.edge_mating_graph import EdgeMatingGraph


class FirstSolver():
    def __init__(self,puzzle_image,puzzle_num,puzzle_noise_level) -> None:
        self.puzzle_image = puzzle_image
        self.puzzle_num = puzzle_num
        self.puzzle_noise_level = puzzle_noise_level
        self.bag_of_pieces = None
        self.puzzle_directory = None
        self.mating_graph = None

    def load_bag_of_pieces(self):
        self.puzzle_directory = f"data/ofir/{self.puzzle_image}/Puzzle{self.puzzle_num}/{self.puzzle_noise_level}"
        self.loader = Puzzle(self.puzzle_directory)
        self.loader.load()

        self.bag_of_pieces = self.loader.get_bag_of_pieces()

    def extract_features(self):
        edge_length_extractor = geo_extractor.EdgeLengthExtractor(self.bag_of_pieces)
        edge_length_extractor.run()
        angles_extractor = geo_extractor.AngleLengthExtractor(self.bag_of_pieces)
        angles_extractor.run()

    def load_cycles(self):
        self.mating_graph = EdgeMatingGraph(self.bag_of_pieces)
        self.mating_graph.load_raw_cycles(self.puzzle_directory+"/cycles.txt")
        self.mating_graph.find_cycles()
    
    def compute_cycles(self,is_save_cycles=True):
        edge_length_pairwiser = geo_pairwiser.EdgeMatcher(self.bag_of_pieces)
        edge_length_pairwiser.pairwise(self.loader.noise+1e-3)
        
        self.mating_graph = EdgeMatingGraph(self.bag_of_pieces,edge_length_pairwiser.match_edges,edge_length_pairwiser.match_pieces_score)
        self.mating_graph.build_graph()
        self.mating_graph.compute_raw_cycles()

        if is_save_cycles:
            self.mating_graph.save_raw_cycles(self.puzzle_directory+"/cycles.txt")
        
        self.mating_graph.find_cycles()

    def build_zero_loops(self):
        pass





