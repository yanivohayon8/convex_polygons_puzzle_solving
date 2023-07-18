import unittest
from src.solvers.apictorial import FirstSolver

class TestIntegration(unittest.TestCase):
    
    def _run(self,puzzle_image,puzzle_num,puzzle_noise_level, is_load_cycles=True):
        solver = FirstSolver(puzzle_image,puzzle_num,puzzle_noise_level)

        solver.load_bag_of_pieces()
        solver.extract_features()
        solver.pairwise()

        if is_load_cycles:
            try:
                solver.load_cycles()
            except OSError:
                solver.compute_cycles(True)
        else:
            solver.compute_cycles(True)
        
        solver.build_zero_loops()
        solver.global_optimize()
        


    def test_Inv9084_puzzle_1_noise_0(self):
        image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise_level = 0

        self._run(image,puzzle_num,puzzle_noise_level)

        



        


if __name__ == "__main__":
    unittest.main()