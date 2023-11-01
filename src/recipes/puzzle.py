from src.recipes import Recipe,factory
from src.data_types.puzzle import Puzzle
from src.physics import assembler
from src import shared_variables

class loadRegularPuzzle(Recipe):

    def __init__(self,db,puzzle_num,noise_level) -> None:
        self.db = db
        self.puzzle_num = puzzle_num
        self.noise_level = noise_level
        self.puzzle = None
    
    def cook(self,is_override_shared_vars=True):
        puzzle_directory = f"../ConvexDrawingDataset/DB{self.db}/Puzzle{self.puzzle_num}/noise_{self.noise_level}"
        self.puzzle = Puzzle(puzzle_directory)
        self.puzzle.load()

        if is_override_shared_vars:
            assembler.init(self.db,self.puzzle_num,self.noise_level)
            shared_variables.puzzle = self.puzzle
            
        return self.puzzle.get_bag_of_pieces()


factory.register_builder(loadRegularPuzzle.__name__,
                         lambda db,puzzle_num,noise_level:loadRegularPuzzle(db,puzzle_num,noise_level))

# TODO: a recipe for puzzles with missing pieces?
