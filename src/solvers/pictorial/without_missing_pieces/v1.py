from src.recipes import factory as recipes_factory


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
        
        config.update(zero_loops_config)

        zero_loop_recipe = recipes_factory.create("ZeroLoopsAroundVertex",**config)
        zero_loops = zero_loop_recipe.cook()

        # TODO: implement wrapping mechanism here to union loops (When we will have larger puzzles)
        loops = zero_loops

        total_num_pieces = zero_loop_recipe.get_num_piece_in_puzzle()
        merger = recipes_factory.create("LoopsMerge",ranked_loops=loops,puzzle_num_pieces=total_num_pieces)
        solution = merger.cook()

        return solution

