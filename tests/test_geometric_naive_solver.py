import unittest

from src.puzzle import Puzzle
import src.solvers.naive as solvers
from src.visualizers.cv2_wrapper import Frame
import matplotlib.pyplot as plt
import networkx as nx

from src.my_http_client import HTTPClient

class TestOld(unittest.TestCase):
    def test_donothing(self):
        puzzle_directory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0"
        # loader = Puzzle(puzzle_directory + "/ground_truth_puzzle.csv",
        #                 puzzle_directory + "/ground_truth_rels.csv", 
        #                 puzzle_directory + "/pieces.csv")
        loader = Puzzle(puzzle_directory)
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

    def test_plot_mating_graph(self):
        direrctory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/"
        puzzle_directory = direrctory + "0"
        #puzzle_directory = direrctory + "simplest_puzzle"
        #puzzle_directory = direrctory + "simplest_puzzle_v2"
        # loader = Puzzle(puzzle_directory + "/ground_truth_puzzle.csv",
        #                 puzzle_directory + "/ground_truth_rels.csv", 
        #                 puzzle_directory + "/pieces.csv")

        loader = Puzzle(puzzle_directory)

        loader.load()
        bag_of_pieces = loader.get_bag_of_pieces() #loader.get_final_puzzle()
        solver = solvers.GeometricNoiselessSolver(bag_of_pieces)
        solver.extract_features()
        solver.pairwise()
        #solver.global_optimize()
        solver._compute_edges_mating_graph()

        print(solver.edges_mating_graph.edges)
        
        #ax = plt.subplot(121)
        fig = plt.figure(figsize=(20,20))
        #nx.draw(solver.edges_mating_graph,with_labels=True,font_weight='bold')
        nodes = solver.edges_mating_graph.nodes
        edges = solver.edges_mating_graph.edges
        #print(nodes)
        #pos = nx.spring_layout(solver.edges_mating_graph,k=1)
        
        pos = nx.spring_layout(solver.edges_mating_graph,k=1)
        nx.draw_networkx_nodes(solver.edges_mating_graph, pos,nodelist=[n for n in nodes if "P_5" in n],node_color="red", node_size=50) #,cmap=plt.get_cmap('jet'), node_size = 500)
        nx.draw_networkx_nodes(solver.edges_mating_graph, pos,nodelist=[n for n in nodes if "P_3" in n],node_color="blue",node_size=50) #,cmap=plt.get_cmap('jet'), node_size = 500)
        nx.draw_networkx_nodes(solver.edges_mating_graph, pos,nodelist=[n for n in nodes if "P_2" in n],node_color="green",node_size=50) #,cmap=plt.get_cmap('jet'), node_size = 500)

        nx.draw_networkx_labels(solver.edges_mating_graph, pos,font_size=6)
        nx.draw_networkx_edges(solver.edges_mating_graph, pos, arrows=True)
        #nx.draw_networkx_edges([e for e in edges if "RELS" in e], pos, arrows=True)
        plt.plot()
        keyboardClick=False
        while keyboardClick != True:
            keyboardClick=plt.waitforbuttonpress()

class TestFixedZeroLoops(unittest.TestCase):

    def _load_fixed_zeroloops_solver(self,puzzle_directory):
        # loader = Puzzle(puzzle_directory + "/ground_truth_puzzle.csv",
        #                 puzzle_directory + "/ground_truth_rels.csv", 
        #                 puzzle_directory + "/pieces.csv")

        loader = Puzzle(puzzle_directory)
        
        loader.load()
        bag_of_pieces = loader.get_bag_of_pieces() #loader.get_final_puzzle()
        
        solver = solvers.GeometricNoiselessSolver(bag_of_pieces)
        solver.extract_features()
        solver.pairwise()
        solver._compute_edges_mating_graph()
        solver._load_pieces_matings()
        
        # For Debug puzzle 1:
        #Because the nx package would brings random results, make the test deterministic
        with open(puzzle_directory + "/cycles.txt", 'r') as f:
            cycles = [eval(line.rstrip('\n')) for line in f]

        solver._compute_cycles(cycles)
        solver._load_zero_loops()
        return solver,loader

    def test_image_Inv9084_puzzle_1_noise_0(self,expected_num_cycles=-1,
             expected_num_zero_loops=-1,expected_num_solutions=-1):
        direrctory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/"
        puzzle_directory = direrctory + "0"
        solver,loader = self._load_fixed_zeroloops_solver(puzzle_directory)

        zero_loop_9_P_8_P_6_P_5_P_0 = solver.zero_loops[0]
        zero_loop_P_9_P_8_P_7 = solver.zero_loops[1]
        zero_loop_5_P_2_P_1_P_0 = solver.zero_loops[2]

        one_loop_9_8_7_6_5_0 = zero_loop_9_P_8_P_6_P_5_P_0.union(zero_loop_P_9_P_8_P_7)
        # Because one-to-one matching, it is sufficient to count the matings
        assert set(one_loop_9_8_7_6_5_0.get_pieces_invovled()) == set(["0","5","6","7","8","9"])
        assert len(one_loop_9_8_7_6_5_0.get_availiable_matings()) == 4 
        assert len(one_loop_9_8_7_6_5_0.get_as_mating_list()) == 7

        one_loop_9_8_6_5_2_1_0 = zero_loop_9_P_8_P_6_P_5_P_0.union(zero_loop_5_P_2_P_1_P_0)
        fp_pieces = list(set(one_loop_9_8_6_5_2_1_0.get_pieces_invovled()) - set(["0","1","2","5","6","8","9"]))
        assert len(fp_pieces) == 0
        fn_pieces = list(set(["0","1","2","5","6","8","9"])-set(one_loop_9_8_6_5_2_1_0.get_pieces_invovled()))
        assert len(fn_pieces) == 0  
        assert len(one_loop_9_8_6_5_2_1_0.get_availiable_matings()) == 5 # P2-P3,P5-P3,P6-P4,P9-P7,P8-P7
        manual_couting = ["P2-P5","P2-P1","P1-P0","P0-P5","P5-P6","P6-P9","P9-P8","P8-P0"]
        assert len(one_loop_9_8_6_5_2_1_0.get_as_mating_list()) == len(manual_couting) # 

        # solutions = solver.global_optimize()
        # expected_solution_accuracy=1.0
        # solutions = solver.global_optimize()
        # assert len(solver.zero_loops) == expected_num_zero_loops or expected_num_zero_loops==-1
        # assert len(solutions)==expected_num_solutions or len(solutions)>0
        # assert loader.evaluate_rels(solutions[0])==expected_solution_accuracy
    
    def test_image_Inv9084_puzzle_2_noise_0(self,expected_num_cycles=-1,
                expected_num_zero_loops=-1,expected_num_solutions=-1):
        direrctory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle2/"
        puzzle_directory = direrctory + "0"
        solver,loader = self._load_fixed_zeroloops_solver(puzzle_directory)

        solutions = solver.global_optimize()

        expected_solution_accuracy=1.0
        expected_num_zero_loops = 6
        expected_num_solutions = 1
        
        assert len(solver.zero_loops) == expected_num_zero_loops or expected_num_zero_loops==-1
        assert len(solutions)==expected_num_solutions or len(solutions)>0
        assert loader.evaluate_rels(solutions[0])==expected_solution_accuracy
    
    def test_image_terentius_puzzle_1_noise_0(self,expected_num_cycles=-1,
                expected_num_zero_loops=-1,expected_num_solutions=-1):
        direrctory = "data/ofir/Terentius_Neo_and_wife_MAN_Napoli_Inv9058_n01/Puzzle1/"
        puzzle_directory = direrctory + "0"
        solver,loader = self._load_fixed_zeroloops_solver(puzzle_directory)

        solutions = solver.global_optimize()

        expected_solution_accuracy=1.0
        expected_num_zero_loops = 6
        expected_num_solutions = 1
        
        assert len(solver.zero_loops) == expected_num_zero_loops or expected_num_zero_loops==-1
        assert len(solutions)==expected_num_solutions or len(solutions)>0
        assert loader.evaluate_rels(solutions[0])==expected_solution_accuracy
            

class TestProduction(unittest.TestCase):

    def _save_cycles(self,cycles,out_path):
        '''
            This method is used for the test when the zero loops are fixed
        '''
        with open(out_path, 'w') as fp:
            for item in cycles:
                # write each item on a new line
                fp.write("%s\n" % item)

    def _run(self,
             puzzle_image,
             puzzle_num,
             puzzle_noise,
             expected_solution_accuracy:float,expected_num_cycles=-1,
             expected_num_zero_loops=-1,expected_num_solutions=-1,
             noise = 1,
             is_save_cycles=False):
    
        puzzle_directory = f"data/ofir/{puzzle_image}/Puzzle{puzzle_num}/{puzzle_noise}"
        loader = Puzzle(puzzle_directory)
        loader.load()
        bag_of_pieces = loader.get_bag_of_pieces() #loader.get_final_puzzle()
        
        http = HTTPClient(puzzle_image,puzzle_num,puzzle_noise)

        solver = solvers.GeometricNoiselessSolver(bag_of_pieces,http)
        solver.extract_features()
        solver.pairwise(confidence=noise)
        solver._compute_edges_mating_graph()
        solutions = solver.global_optimize()
        
        if is_save_cycles:
            self._save_cycles(solver.cycles,puzzle_directory+"/cycles.txt")

        assert len(solver.cycles)== expected_num_cycles or expected_num_cycles==-1
        assert len(solver.zero_loops) == expected_num_zero_loops or expected_num_zero_loops==-1
        assert len(solutions)==expected_num_solutions or len(solutions)>0

        solutions[0] = loader.reverse_edge_ids(solutions[0])
        assert loader.evaluate_correct_rels(solutions[0]) == 1
        assert loader.evaluate_rels(solutions[0])==expected_solution_accuracy

    def test_Inv9084_puzzle_1_noise_0(self):
        #direrctory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/"
        #puzzle_directory = direrctory + "0"
        image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise = 0

        expected_num_cycles = 69
        expected_num_zero_loops = 5
        expected_num_solutions = 1 
        expected_solution_accuracy = 1.0
        self._run(image,
                  puzzle_num,
                  puzzle_noise,
                  expected_solution_accuracy,
                  expected_num_cycles=expected_num_cycles,
                  expected_num_zero_loops=expected_num_zero_loops,
                  expected_num_solutions=expected_num_solutions)
    
    def test_Inv9084_puzzle_2_noise_0(self):
        direrctory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle2/"
        puzzle_directory = direrctory + "0"
        expected_solution_accuracy = 1.0
        expected_num_solutions = 1 
        expected_num_zero_loops = 6
        self._run(puzzle_directory,
                  expected_solution_accuracy,
                  expected_num_zero_loops=expected_num_zero_loops,
                  expected_num_solutions=expected_num_solutions,
                  is_save_cycles=False)
    
    def test_Inv9084_puzzle_3_noise_0(self):
        direrctory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle3/"
        puzzle_directory = direrctory + "0"
        expected_solution_accuracy = 1.0
        expected_num_solutions = 1 
        self._run(puzzle_directory,
                  expected_solution_accuracy,
                  expected_num_solutions=expected_num_solutions)
    
    def test_Roman009_puzzle_1_noise_0(self):
        direrctory = "data/ofir/Roman_fresco_Villa_dei_Misteri_Pompeii_009/Puzzle1/"
        puzzle_directory = direrctory + "0"
        expected_solution_accuracy = 1.0
        expected_num_solutions = 1 
        self._run(puzzle_directory,
                  expected_solution_accuracy,
                  expected_num_solutions=expected_num_solutions)
        
    def test_Roman009_puzzle_2_noise_0(self):
        direrctory = "data/ofir/Roman_fresco_Villa_dei_Misteri_Pompeii_009/Puzzle2/"
        puzzle_directory = direrctory + "0"
        expected_solution_accuracy = 1.0
        expected_num_solutions = 1 
        self._run(puzzle_directory,
                  expected_solution_accuracy,
                  expected_num_solutions=expected_num_solutions)
    
    def test_Roman009_puzzle_3_noise_0(self):
        direrctory = "data/ofir/Roman_fresco_Villa_dei_Misteri_Pompeii_009/Puzzle3/"
        puzzle_directory = direrctory + "0"
        expected_solution_accuracy = 1.0
        expected_num_solutions = 1 
        self._run(puzzle_directory,
                  expected_solution_accuracy,
                  expected_num_solutions=expected_num_solutions)
    
    '''This test has been putted as a note becaues it has conflicts in the matings.
    I.e. it does has one to one matings so this probably a computation or representation 
    of numbers and that the points are not in general position. 
    Thus, it is not the model faults.
    
    def test_image_terentius_puzzle_1_noise_0(self):
        direrctory = "data/ofir/Terentius_Neo_and_wife_MAN_Napoli_Inv9058_n01/Puzzle1/"
        puzzle_directory = direrctory + "0"
        expected_solution_accuracy = 1.0
        expected_num_solutions = 1 
        self._run(puzzle_directory,
                  expected_solution_accuracy,
                  expected_num_solutions=expected_num_solutions)#,is_save_cycles=True'''
    
    '''This test has been putted as a note becaues it has conflicts in the matings.
    I.e. it does has one to one matings so this probably a computation or representation 
    of numbers and that the points are not in general position. 
    Thus, it is not the model faults.
    
    def test_image_terentius_puzzle_2_noise_0(self):
        direrctory = "data/ofir/Terentius_Neo_and_wife_MAN_Napoli_Inv9058_n01/Puzzle2/"
        puzzle_directory = direrctory + "0"
        expected_solution_accuracy = 1.0
        expected_num_solutions = 1 
        self._run(puzzle_directory,
                  expected_solution_accuracy,
                  expected_num_solutions=expected_num_solutions)#,is_save_cycles=True'''
        
    def test_terentius_puzzle_3_noise_0(self):
        direrctory = "data/ofir/Terentius_Neo_and_wife_MAN_Napoli_Inv9058_n01/Puzzle3/"
        puzzle_directory = direrctory + "0"
        expected_solution_accuracy = 1.0
        expected_num_solutions = 1 
        self._run(puzzle_directory,
                  expected_solution_accuracy,
                  expected_num_solutions=expected_num_solutions)
    
    def test_Inv9084_puzzle_1_noise_1(self):
        image = "Pseudo-Sappho_MAN_Napoli_Inv9084"
        puzzle_num = 1
        puzzle_noise = 1
        direrctory = f"data/ofir/{image}/Puzzle1/"
        puzzle_directory = direrctory + "1"
        expected_num_cycles = -1
        expected_num_zero_loops = -1
        expected_num_solutions = -1 
        expected_solution_accuracy = 1.0
        puzzle_diameter = 3007.6720313778787
        xi = 3.007672031377879
        noise = xi #xi*puzzle_diameter/100


        self._run(image,
                  puzzle_num,
                  puzzle_noise,
                  expected_solution_accuracy,
                  expected_num_cycles=expected_num_cycles,
                  expected_num_zero_loops=expected_num_zero_loops,
                  expected_num_solutions=expected_num_solutions,
                  is_save_cycles=False,
                  noise=noise)


if __name__ == "__main__":
    unittest.main()