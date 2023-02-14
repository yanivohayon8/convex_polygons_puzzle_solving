import unittest

from src.puzzle import Puzzle
import src.solvers.naive as solvers
from src.visualizers.cv2_wrapper import Frame

class TestNaiveSolver(unittest.TestCase):

    def test_donothing(self):
        puzzle_directory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0"
        loader = Puzzle(puzzle_directory + "/ground_truth_puzzle.csv",
                        puzzle_directory + "/ground_truth_rels.csv", 
                        puzzle_directory + "/pieces.csv")
        loader.load()

        # pieces = loader.get_chaos_pieces()        
        pieces = loader.get_complete_puzzle()        
        naive = solvers.DoNothing(pieces)
        assembly = naive.run()

        # frame = Frame(size=(1080,1920,3)) # 
        frame = Frame(size=(2500,3000,3)) # 
        assembly.draw(frame)
        frame.show()
        frame.wait()
        frame.destroy()        

    def test_geometric_solver(self):
        puzzle_directory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0"
        loader = Puzzle(puzzle_directory + "/ground_truth_puzzle.csv",
                        puzzle_directory + "/ground_truth_rels.csv", 
                        puzzle_directory + "/pieces.csv")
        loader.load()
        bag_of_pieces = loader.get_final_puzzle()
        solver = solvers.GeometricSolver(bag_of_pieces)
        solver.extract_features()
        solver.pairwise()
        solver.global_optimize()

if __name__ == "__main__":
    unittest.main()