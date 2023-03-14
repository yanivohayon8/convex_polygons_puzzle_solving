import unittest

from src.puzzle import Puzzle
import src.solvers.naive as solvers
from src.visualizers.cv2_wrapper import Frame
import matplotlib.pyplot as plt
import networkx as nx


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
        direrctory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/"
        puzzle_directory = direrctory + "0"
        #puzzle_directory = direrctory + "simplest_puzzle"
        #puzzle_directory = direrctory + "simplest_puzzle_v2"
        loader = Puzzle(puzzle_directory + "/ground_truth_puzzle.csv",
                        puzzle_directory + "/ground_truth_rels.csv", 
                        puzzle_directory + "/pieces.csv")
        loader.load()
        bag_of_pieces = loader.get_bag_of_pieces() #loader.get_final_puzzle()
        solver = solvers.GeometricNoiselessSolver(bag_of_pieces)
        solver.extract_features()
        solver.pairwise()
        solver.global_optimize()
        #solver.compute_edges_mating_graph()

        #print(solver.edges_mating_graph.edges)
        
        # #ax = plt.subplot(121)
        # fig = plt.figure(figsize=(20,20))
        # #nx.draw(solver.edges_mating_graph,with_labels=True,font_weight='bold')
        # nodes = solver.edges_mating_graph.nodes
        # edges = solver.edges_mating_graph.edges
        # #print(nodes)
        # #pos = nx.spring_layout(solver.edges_mating_graph,k=1)
        
        # pos = nx.spring_layout(solver.edges_mating_graph,k=1)
        # nx.draw_networkx_nodes(solver.edges_mating_graph, pos,nodelist=[n for n in nodes if "P_5" in n],node_color="red", node_size=50) #,cmap=plt.get_cmap('jet'), node_size = 500)
        # nx.draw_networkx_nodes(solver.edges_mating_graph, pos,nodelist=[n for n in nodes if "P_3" in n],node_color="blue",node_size=50) #,cmap=plt.get_cmap('jet'), node_size = 500)
        # nx.draw_networkx_nodes(solver.edges_mating_graph, pos,nodelist=[n for n in nodes if "P_2" in n],node_color="green",node_size=50) #,cmap=plt.get_cmap('jet'), node_size = 500)

        # nx.draw_networkx_labels(solver.edges_mating_graph, pos,font_size=6)
        # nx.draw_networkx_edges(solver.edges_mating_graph, pos, arrows=True)
        # #nx.draw_networkx_edges([e for e in edges if "RELS" in e], pos, arrows=True)
        # plt.plot()
        # keyboardClick=False
        # while keyboardClick != True:
        #     keyboardClick=plt.waitforbuttonpress()

    def test_zero_loops(self):
        direrctory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/"
        puzzle_directory = direrctory + "0"
        loader = Puzzle(puzzle_directory + "/ground_truth_puzzle.csv",
                        puzzle_directory + "/ground_truth_rels.csv", 
                        puzzle_directory + "/pieces.csv")
        loader.load()
        bag_of_pieces = loader.get_bag_of_pieces() #loader.get_final_puzzle()
        
        solver = solvers.GeometricNoiselessSolver(bag_of_pieces)
        solver.extract_features()
        solver.pairwise()
        solver._compute_edges_mating_graph()
        
        # # Because the nx package would brings random results, make the test deterministic
        with open(puzzle_directory + "/cycles.txt", 'r') as f:
            cycles_list = [eval(line.rstrip('\n')) for line in f]
        #cycles_list = solver._compute_cycles()
        
        solver._load_zero_loops(cycles_list)


    def test_union_loops(self):
        '''Start testing'''
        #print(cycles_list)

        '''
            You need to delete all the aboved code and write here hard coded 
            the zero loops.
        '''

        zero_loops = [] #'''Fill me hardcoded'''

        assert len(zero_loops) == 5
        expected_loops = ["P_5_P_3_P_2", "P_5_P_6_P_4_P_3", "P_8_P_7_P_9", "P_5_P_0_P_8_P_9_P_6", "P_0_P_5_P_2_P_1"]
        
        for expected,res in zip(expected_loops,zero_loops):
            assert expected == repr(res) 
        
        loop_level = 0
        zero_loops_pairs = solver._loops_to_union(zero_loops,loop_level+1)
        # assert zero_loops_pairs == [(0, 1), (0, 4), (1, 3), (2, 3), (3, 4)]
        one_loops = [zero_loops[pair[0]].union(zero_loops[pair[1]]) for pair in zero_loops_pairs]
        assert len(one_loops) == 7 #5 
        expected_loops = ["P_6_P_4_P_5_P_3_P_2", "P_5_P_6_P_4_P_3", "P_8_P_7_P_9", "P_5_P_0_P_8_P_9_P_6", "P_0_P_5_P_2_P_1"]
        for expected,res in zip(expected_loops,zero_loops):
            assert expected == repr(res) 

        print("zero_loops:")
        print(zero_loops)
        # print(zero_loops_pairs)
        print("one_loops:")
        print(one_loops)
        #expected_one_loops = ["P5_"]
        loop_level+=1
        one_loops_pairs = solver._loops_to_union(one_loops,loop_level+1)
        # assert len(one_loops_pairs)<len(zero_loops_pairs)
        two_loops = [one_loops[pair[0]].union(one_loops[pair[1]]) for pair in one_loops_pairs]
        assert len(two_loops) == 6 # from counting by hand
        print("one_loops_pairs:")
        print(one_loops_pairs)
        print("two_loops:")
        print(two_loops)
        loop_level+=1
        two_loops_pairs = solver._loops_to_union(two_loops,loop_level+1)
        print("two_loops_pairs")
        print(two_loops_pairs)

        

        
if __name__ == "__main__":
    unittest.main()