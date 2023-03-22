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

    def test_plot_mating_graph(self):
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


    def _run(self,puzzle_directory:str,expected_solution_accuracy:float,expected_num_cycles=-1,
             expected_num_zero_loops=-1,expected_num_solutions=-1):
        # direrctory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/"
        # puzzle_directory = direrctory + "0"
        loader = Puzzle(puzzle_directory + "/ground_truth_puzzle.csv",
                        puzzle_directory + "/ground_truth_rels.csv", 
                        puzzle_directory + "/pieces.csv")
        loader.load()
        bag_of_pieces = loader.get_bag_of_pieces() #loader.get_final_puzzle()
        
        solver = solvers.GeometricNoiselessSolver(bag_of_pieces)
        solver.extract_features()
        solver.pairwise()
        solver._compute_edges_mating_graph()
        
        # # For Debug puzzle 1:
        # Because the nx package would brings random results, make the test deterministic
        # with open(puzzle_directory + "/cycles.txt", 'r') as f:
        #     cycles = [eval(line.rstrip('\n')) for line in f]

        # solutions = solver.global_optimize(cycles)
        
        solutions = solver.global_optimize()
        
        assert len(solver.cycles)== expected_num_cycles or expected_num_cycles==-1
        assert len(solver.zero_loops) == expected_num_zero_loops or expected_num_zero_loops==-1
        assert len(solutions)==expected_num_solutions or len(solutions)>0
        assert loader.evaluate_rels(solutions[0])==expected_solution_accuracy

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
    
    def test_image_Inv9084_puzzle_2_noise_0(self):
        direrctory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle2/"
        puzzle_directory = direrctory + "0"
        expected_solution_accuracy = 1.0
        expected_num_solutions = 1 
        self._run(puzzle_directory,
                  expected_solution_accuracy,
                  expected_num_solutions=expected_num_solutions)
    
    def test_image_Inv9084_puzzle_3_noise_0(self):
        direrctory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle3/"
        puzzle_directory = direrctory + "0"
        expected_solution_accuracy = 1.0
        expected_num_solutions = 1 
        self._run(puzzle_directory,
                  expected_solution_accuracy,
                  expected_num_solutions=expected_num_solutions)
  

        
if __name__ == "__main__":
    unittest.main()