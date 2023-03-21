import unittest

from src.puzzle import Puzzle
import src.solvers.naive as solvers
from src.visualizers.cv2_wrapper import Frame
import matplotlib.pyplot as plt
import networkx as nx


class TestNaiveSolverPuzzle1(unittest.TestCase):

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




    def test_0_noise(self):
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
        
        # # For Debug puzzle 1:
        # Because the nx package would brings random results, make the test deterministic
        # with open(puzzle_directory + "/cycles.txt", 'r') as f:
        #     cycles = [eval(line.rstrip('\n')) for line in f]

        # solutions = solver.global_optimize(cycles)
        
        solutions = solver.global_optimize()
        
        expected_num_cycles = 69
        assert len(solver.cycles)==expected_num_cycles
        expected_num_zero_loops = 5
        assert len(solver.zero_loops) == expected_num_zero_loops
        assert len(solutions)==1
        assert loader.evaluate_rels(solutions[0])==1
        
  

        
if __name__ == "__main__":
    unittest.main()