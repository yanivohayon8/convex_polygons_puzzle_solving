import unittest
import src.solvers.naive as naive_solvers
from src.puzzle import Puzzle
import matplotlib.pyplot as plt


class TestPictorialNaiveSolver(unittest.TestCase):
    
    def _run(self,puzzle_directory:str,expected_solution_accuracy:float,expected_num_cycles=-1,
             expected_num_zero_loops=-1,expected_num_solutions=-1,is_save_cycles=False):
        # direrctory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/"
        # puzzle_directory = direrctory + "0"
        loader = Puzzle(puzzle_directory)
        loader.load()
        bag_of_pieces = loader.get_bag_of_pieces() #loader.get_final_puzzle()
        [piece.load_image() for piece in bag_of_pieces]

        #loader.load_images()
        solver = naive_solvers.PictorialSolver(bag_of_pieces)
        
        # plt.imshow(loader.pieces_images["0"])
        # plt.close()

        solver.extract_features()
        solver.pairwise()
        solver._compute_edges_mating_graph()
        solutions = solver.global_optimize()
        

        # assert len(solver.cycles)== expected_num_cycles or expected_num_cycles==-1
        # assert len(solver.zero_loops) == expected_num_zero_loops or expected_num_zero_loops==-1
        # assert len(solutions)==expected_num_solutions or len(solutions)>0
        # assert loader.evaluate_rels(solutions[0])==expected_solution_accuracy

    def test_image_Inv9084_puzzle_1_noise_0(self):
        direrctory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/"
        puzzle_directory = direrctory + "0"
        expected_num_cycles = 69
        expected_num_zero_loops = 5
        expected_num_solutions = 1 
        expected_solution_accuracy = 1.0
        self._run(puzzle_directory,
                  expected_solution_accuracy,
                  expected_num_cycles=expected_num_cycles,
                  expected_num_zero_loops=expected_num_zero_loops,
                  expected_num_solutions=expected_num_solutions)

if __name__ == "__main__":
    unittest.main()