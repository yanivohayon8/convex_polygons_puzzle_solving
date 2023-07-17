import unittest
from src.solvers.apictorial import FirstSolver

class TestIntegration(unittest.TestCase):
    
    def _run(self,puzzle_image,puzzle_num,puzzle_noise_level):
        solver = FirstSolver(puzzle_image,puzzle_num,puzzle_noise_level)
        solver.run()

    def test_Inv9084_puzzle_1_noise_0(self):
        image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise_level = 0

        self._run(image,puzzle_num,puzzle_noise_level)

        



        


if __name__ == "__main__":
    unittest.main()