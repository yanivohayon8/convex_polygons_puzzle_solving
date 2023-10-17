import unittest
from src.solvers.apictorial import FirstSolver
from src.recipes.puzzle import loadRegularPuzzle
from src.data_structures.zero_loops import ZeroLoopKeepCycleAsIs
from src.data_structures.hierarchical_loops import get_loop_matings_as_csv
from src.feature_extraction import geometric as geo_extractor 

class TestZeroLoopKeepCycleAsIs(unittest.TestCase):
    
    def test_Inv9084_puzzle_1_noise_0_deprecated(self):
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
        
class TestAngleSum(unittest.TestCase):

    def test_Inv9084_noise_1zero_loops(self):

        
        db = "1"
        puzzle_num = 19

        for puzzle_noise_level in range(4):
            print(f"Running on noise {puzzle_noise_level}")
            bag_of_pieces = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level).cook()
            
            angles_extractor = geo_extractor.AngleLengthExtractor(bag_of_pieces)
            angles_extractor.run()
            piece_edge_loop = [(3,1), (3,0), (2,2), (2,1), (5,3), (5,2)]

            accumulated_loop_angle = 0

            for edge1,edge2 in zip(piece_edge_loop[:-1:2],piece_edge_loop[1::2]):
                piece = bag_of_pieces[edge1[0]]
                inner_angle =  piece.get_inner_angle(edge1[1],edge2[1])
                print("\tinner_angle",inner_angle)
                accumulated_loop_angle += inner_angle

            print("\taccumulated_loop_angle",accumulated_loop_angle)
            print("\t360 - accumulated_loop_angle",360 - accumulated_loop_angle)



        


if __name__ == "__main__":
    unittest.main()