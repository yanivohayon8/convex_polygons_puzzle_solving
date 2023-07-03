# import unittest
# from src.visualizers import cv2_wrapper 
# import numpy as np
# from src.solvers import Assembly
# from src import puzzle 


# class TestFrame(unittest.TestCase):

#     def test_simple_rect(self):
#         frame = cv2_wrapper.Frame(size=(1080,1920,3))
#         square_length = 200
#         simple_square = np.array([
#             (0,0),(square_length*2,0),(square_length*2,square_length),(0,square_length)
#         ])

#         frame.draw_polygons([simple_square],[(255,0,0)])
#         frame.show()
#         frame.wait()
#         frame.destroy()

#     def test_final_assembly_nonpictorial(self):
#         puzzle_directory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0"
#         loader = puzzle.puzzle(puzzle_directory + "/ground_truth_puzzle.csv",
#                         puzzle_directory + "/ground_truth_rels.csv", 
#                         puzzle_directory + "/pieces.csv")
#         loader.load()
#         pieces = loader.pieces_pd2list(loader.df_locations)
#         assembly = Assembly(None,pieces)
#         frame = cv2_wrapper.Frame(size=(3000,3000,3)) # 
#         assembly.draw(frame)
#         frame.show()
#         frame.wait()
#         frame.destroy()

#     def test_load_assmebly_nonpictorial(self):
#         puzzle_directory = "data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0"
#         loader = puzzle.puzzle(puzzle_directory + "/ground_truth_puzzle.csv",
#                         puzzle_directory + "/ground_truth_rels.csv", 
#                         puzzle_directory + "/pieces.csv")
#         loader.load()
#         pieces = loader.get_chaos_pieces()
#         assembly = Assembly(None,pieces)
#         sz = (3000,3000,3) #(1080,1920,3)
#         frame = cv2_wrapper.Frame(size=sz) # 
#         assembly.draw(frame)
#         frame.show()
#         frame.wait()
#         frame.destroy()



# if __name__ == "__main__":
#     unittest.main()