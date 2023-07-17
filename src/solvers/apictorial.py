from src.puzzle import Puzzle
from src.feature_extraction import geometric as geo_extractor 


class FirstSolver():
    def __init__(self,puzzle_image,puzzle_num,puzzle_noise_level) -> None:
        self.puzzle_image = puzzle_image
        self.puzzle_num = puzzle_num
        self.puzzle_noise_level = puzzle_noise_level

    def run(self):
        puzzle_directory = f"data/ofir/{self.puzzle_image}/Puzzle{self.puzzle_num}/{self.puzzle_noise_level}"
        loader = Puzzle(puzzle_directory)
        loader.load()
        bag_of_pieces = loader.get_bag_of_pieces()

        length_extractor = geo_extractor.EdgeLengthExtractor(bag_of_pieces)
        length_extractor.run()
        
        angles_extractor = geo_extractor.AngleLengthExtractor(bag_of_pieces)
        angles_extractor.run()


        