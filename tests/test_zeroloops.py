import unittest
from src.solvers.apictorial import FirstSolver
from src.recipes.puzzle import loadRegularPuzzle
from src.recipes import factory as recipes_factory
from src.mating_graphs import factory as graph_factory
from src.data_structures.zero_loops import ZeroLoopKeepCycleAsIs
from src.data_structures.loop_merger import BasicLoopMerger
from src.mating import Mating
from src.data_structures.hierarchical_loops import get_loop_matings_as_csv
from src.feature_extraction import geometric as geo_extractor 

# class TestZeroLoopKeepCycleAsIs(unittest.TestCase):
    
#     def test_Inv9084_puzzle_1_noise_0_deprecated(self):
#         db = "Pseudo-Sappho_MAN_Napoli_Inv9084"
#         puzzle_num = 1
#         puzzle_noise_level = 2#0

#         puzzle_directory = f"data/ofir/{db}/Puzzle{puzzle_num}/{puzzle_noise_level}"
#         puzzle = Puzzle(puzzle_directory)
#         solver = FirstSolver(puzzle,db,puzzle_num,puzzle_noise_level)

#         solver.load_bag_of_pieces()
#         solver.extract_features()
#         solver.pairwise()

#         solver.load_cycles()

#         # Todo - convert the cycles to loops
#         zero_loops_loader = ZeroLoopKeepCycleAsIs(solver.bag_of_pieces,solver.cycles,solver.piece2potential_matings)
#         zero_loops = zero_loops_loader.load(99999999)

#         for i,zero_loop in enumerate(zero_loops):
#             matings_csv = get_loop_matings_as_csv(zero_loop,solver.id2piece)
#             # zero_loop.set_matings_as_csv(matings_csv)
#             response = solver.physical_assembler.run(matings_csv,screenshot_name=f"cycle_{i}")
    


class TestBasicLoopMerger(unittest.TestCase):
    def test_loop_merging(self):
        graph_cycles = [
            ['P_2_E_1', 'P_2_E_2', 'P_3_E_0', 'P_3_E_1', 'P_5_E_2', 'P_5_E_3'],
            ['P_3_E_1', 'P_3_E_2', 'P_4_E_0', 'P_4_E_1', 'P_6_E_2', 'P_6_E_0', 'P_5_E_1', 'P_5_E_2'],
            ['P_7_E_1', 'P_7_E_2', 'P_8_E_0', 'P_8_E_1', 'P_9_E_3', 'P_9_E_0'],
            ['P_0_E_2', 'P_0_E_3', 'P_1_E_0', 'P_1_E_1', 'P_2_E_0', 'P_2_E_1', 'P_5_E_3', 'P_5_E_0'],
            ['P_0_E_1', 'P_0_E_2', 'P_5_E_0', 'P_5_E_1', 'P_6_E_0', 'P_6_E_1', 'P_9_E_2', 'P_9_E_3', 'P_8_E_1', 'P_8_E_2']
        ]

        cycles = [graph_factory.create("Cycle",debug_graph_cycle=graph_cy) for graph_cy in graph_cycles]

        # Beware of side affects
        pairwise_recipe = recipes_factory.create("SD1Pairwise",db=1,puzzle_num=19,
                                                 puzzle_noise_level=1)
        graph_wrapper = pairwise_recipe.cook()
        piece2potential_matings = graph_wrapper.get_piece2filtered_potential_matings()
        bag_of_pieces = pairwise_recipe.puzzle_recipe.puzzle.bag_of_pieces
        zero_loops_loader = ZeroLoopKeepCycleAsIs(bag_of_pieces,cycles,piece2potential_matings)
        zero_loops = zero_loops_loader.load()
        merger = BasicLoopMerger()

        expected_mating = Mating(piece_1="5",edge_1=2,
                                 piece_2="3",edge_2=1)
        loop_2_3_5,loop_3_4_5_6 =  zero_loops[0],zero_loops[1]
        assert expected_mating in loop_2_3_5.get_as_mating_list()
        assert expected_mating in loop_3_4_5_6.get_as_mating_list()
        loop_2_3_4_5_6 = merger.merge(loop_2_3_5,loop_3_4_5_6)
        assert expected_mating in loop_2_3_4_5_6.get_as_mating_list()
        assert loop_2_3_4_5_6.level == 1

        loop_0_1_2_5 = zero_loops[3]
        loop_0_1_2_3_4_5_6 = merger.merge(loop_2_3_4_5_6,loop_0_1_2_5)
        mating_2_6 = Mating(piece_1="2",edge_1=0,piece_2="6",edge_2=1)
        assert mating_2_6 not in loop_0_1_2_3_4_5_6.get_as_mating_list()






class TestAngleSum(unittest.TestCase):

    def test_Inv9084_noise_1zero_loops(self):

        
        db = "1"
        puzzle_num = 19

        for puzzle_noise_level in range(4):
            print(f"Running on noise {puzzle_noise_level}")
            bag_of_pieces = recipes_factory.create("loadRegularPuzzle",
                                                db=db,puzzle_num=puzzle_num,noise_level=puzzle_noise_level).cook()

            
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