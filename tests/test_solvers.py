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

    def test_union_0_loops(self):
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
        solver._compute_edges_mating_graph()
        
        
        super_pieces = [            
            solvers.SuperPiece({8: [1, 0], 9: [3, 0], 7: [1, 2]},{8: [2], 9: [1, 2], 7: [0]}),
            solvers.SuperPiece({3: [0, 1], 5: [2, 3], 2: [1, 2]},{3: [2], 5: [0, 1], 2: [0]}),
            solvers.SuperPiece({0: [2, 1], 5: [0, 1], 6: [0, 1], 9: [2, 3], 8: [1, 2]},{0: [0, 3], 5: [2, 3], 6: [2], 9: [0, 1], 8: [0]}),
            solvers.SuperPiece({2: [1, 0], 5: [3, 0], 0: [2, 3], 1: [0, 1]},{2: [2], 5: [1, 2], 0: [0, 1], 1: [2]}),
            solvers.SuperPiece({6: [0, 2], 5: [1, 2], 3: [1, 2], 4: [0, 1]},{6: [1], 5: [0, 3], 3: [0], 4: [2]})
        ]

        merges=[(3,2),(3,4),(3,1),(0,2),(2,4),(2,1),(4,1)]

        expected_piece2numedges = [
            {1:1,2:1,5:1,6:1,9:2,8:1,0:1},
            {0:2,1:1,4:1,6:1},
            {1:1,3:1,5:1,0:2},
            {7:1,0:2,5:2,6:1,9:1},
            {3:1,4:1,9:2,8:1,0:2,5:1},
            {2:1,3:1,6:1,9:2,8:1,0:2},
            {2:1,4:1,6:1,5:1}
        ]

        for expected_numedges, merge in zip(expected_piece2numedges,merges):
            super_1 = super_pieces[merge[0]]
            super_2 = super_pieces[merge[1]]
            print("Union pieces:")
            print(super_1)
            print("AND")
            print(super_2)
            super_new = solver._union(super_1,super_2)
            print(f"result:{super_new}")
            print(f"Expected: ",expected_numedges)
            print
            #print(super_new.inner_edges_indexes)
            #print(super_new.outer_edges_indexes)
            print()

            count_edges = {}
            next_key = None
            splitted_repr = repr(super_new).split("_")

            for token in splitted_repr:
                if token.startswith("P"):
                    next_key = int(token[1:])
                    count_edges[next_key] = 0
                else:
                    count_edges[next_key]+=1
            
            exp_sub_real = list(set(expected_numedges.keys()) - set(count_edges.keys()))
            assert len(exp_sub_real) == 0, f"False Negative piece as outter: {exp_sub_real}"
            
            real_sub_exp = list(set(count_edges.keys()) - set(expected_numedges.keys()))
            assert len(real_sub_exp) == 0, f"False Positive piece as outter: {real_sub_exp}"
            
            for piece in count_edges.keys():
                err_msg = f"Expected num edge at piece {piece} is {expected_numedges[piece]}. Recieve {count_edges[piece]}"
                assert (count_edges[piece] == expected_numedges[piece]), err_msg

    def test_merge_1_loops(self):

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
        solver._compute_edges_mating_graph()

        super_pieces = [
            solvers.SuperPiece({3: [0, 1], 0: [2, 3], 1: [0, 1]},{3: [2], 0: [0, 1], 1: [2], 5: [1]}),
            solvers.SuperPiece({2: [2, 1], 3: [0, 1], 0: [2, 1], 6: [0, 1], 9: [2, 3], 8: [1, 2]},{2: [0], 3: [2], 0: [0, 3], 6: [2], 9: [0, 1], 8: [0]}),
            solvers.SuperPiece({2: [2, 1], 4: [1, 0], 6: [2, 0]},{2: [0], 4: [2], 6: [1], 5: [0]}),
            solvers.SuperPiece({1: [0, 1], 2: [0, 1], 6: [0, 1], 9: [2, 3], 8: [1, 2]},{1: [2], 2: [2], 6: [2], 9: [0, 1], 8: [0], 0: [0], 5: [2]}),
            solvers.SuperPiece({0: [2, 3], 1: [0, 1], 2: [0, 1], 4: [1, 0], 6: [2, 0], 3: [1, 2]},{0: [0, 1], 1: [2], 4: [2], 6: [1]}),
            solvers.SuperPiece({0: [2, 1], 9: [2, 3], 8: [1, 2], 4: [1, 0], 3: [1, 2]},{0: [0, 3], 9: [0, 1], 8: [0], 4: [2], 3: [0], 5: [3]}),
            solvers.SuperPiece({0: [2, 1], 5: [0, 1], 6: [0, 1], 7: [2, 1]},{0: [0, 3], 5: [2, 3], 6: [2], 7: [0], 9: [1]})
        ]

        res = solver._union(super_pieces[2],super_pieces[4])
        print(res)
        res = solver._union(super_pieces[2],super_pieces[0])
        print(res)


        
if __name__ == "__main__":
    unittest.main()