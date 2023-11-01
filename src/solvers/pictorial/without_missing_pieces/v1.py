from src.recipes import factory as recipes_factory
from src.physics import assembler
from src.data_types.assembly import Assembly

class LoopMergerSolver():

    def __init__(self,db,puzzle_num,puzzle_noise_level,
                 pairwise_recipe="SD1Pairwise") -> None:
        self.db = db
        self.puzzle_num = puzzle_num
        self.puzzle_noise_level = puzzle_noise_level
        self.pairwise_recipe = pairwise_recipe
    
    def solve(self,**zero_loops_config):
        config = {
            "db":self.db,
            "puzzle_num":self.puzzle_num,
            "puzzle_noise_level":self.puzzle_noise_level,
            "pairwise_recipe_name": self.pairwise_recipe
        }
        
        config.update()

        zero_loop_recipe = recipes_factory.create("ZeroLoopsAroundVertex",**config)
        zero_loops = zero_loop_recipe.cook(**zero_loops_config)

        # TODO: implement wrapping mechanism here to union loops (When we will have larger puzzles)
        loops = zero_loops

        total_num_pieces = zero_loop_recipe.get_num_piece_in_puzzle()
        merger = recipes_factory.create("ZeroLoopsMerge",ranked_loops=loops,puzzle_num_pieces=total_num_pieces)
        loop_solution = merger.cook()

        response = assembler.simulate(loop_solution.get_matings_as_csv())
        physical_score = assembler.score(response)
        solution_polygons = assembler.get_final_coordinates_as_polygons(response)
        matings = loop_solution.get_as_mating_list()
        
        return Assembly(solution_polygons,matings,physical_score=physical_score)

