import unittest
from src.solvers.apictorial import FirstSolver
from src.puzzle import Puzzle
from src.data_structures.zero_loops import ZeroLoopKeepCycleAsIs
from src.data_structures.hierarchical_loops import get_loop_matings_as_csv


class TestZeroLoopKeepCycleAsIs(unittest.TestCase):
    
    def test_Inv9084_puzzle_1_noise_0(self):
        db = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise_level = 2#0

        puzzle_directory = f"data/ofir/{db}/Puzzle{puzzle_num}/{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        solver = FirstSolver(puzzle,db,puzzle_num,puzzle_noise_level)

        solver.load_bag_of_pieces()
        solver.extract_features()
        solver.pairwise()

        solver.load_cycles()

        # Todo - convert the cycles to loops
        zero_loops_loader = ZeroLoopKeepCycleAsIs(solver.bag_of_pieces,solver.cycles,solver.piece2potential_matings)
        zero_loops = zero_loops_loader.load(99999999)

        for i,zero_loop in enumerate(zero_loops):
            matings_csv = get_loop_matings_as_csv(zero_loop,solver.id2piece)
            # zero_loop.set_matings_as_csv(matings_csv)
            response = solver.physical_assembler.run(matings_csv,screenshot_name=f"cycle_{i}")
        


if __name__ == "__main__":
    unittest.main()