from src.puzzle import Puzzle
from src.solvers.apictorial import GraphMatchingSolver
from src.puzzle import Puzzle
from src.evaluator import AreaOverlappingEvaluator
import matplotlib.pyplot as plt
import glob
import argparse
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument("--puzzles_dir", default="")
parser.add_argument("--noise_level", default=0)
parser.add_argument("--is_interactive",default=True)
args = parser.parse_args()


def run_solver(puzzle_image,puzzle_num,puzzle_noise_level,is_interactive):
    # puzzle_directory = f"data/ofir/{puzzle_image}/Puzzle{puzzle_num}/{puzzle_noise_level}"
    print("****************************")
    print(f"\tSolve {puzzle_image}/Puzzle{puzzle_num}/{puzzle_noise_level}")
    print("****************************")
    puzzle_directory = f"../ConvexDrawingDataset/{puzzle_image}/Puzzle{puzzle_num}/{puzzle_noise_level}"

    puzzle = Puzzle(puzzle_directory)
    solver = GraphMatchingSolver(puzzle,puzzle_image,puzzle_num,puzzle_noise_level)

    solution = solver.run()

    ground_truth_polygons = puzzle.get_ground_truth_puzzle()
    evaluator = AreaOverlappingEvaluator(ground_truth_polygons)
    
    overlapping_score = evaluator.evaluate(solution.get_polygons())
    matings_accuracy = puzzle.evaluate_rels(solution.get_matings())
    print("\tSolution overlapping score is ",overlapping_score)
    print("\tSolution matings correct score is ",matings_accuracy)

    if is_interactive:
        answer = input("\ttype y to see the results of the physical engine:\t")
        if answer == "y":
            fig ,ax = plt.subplots(1,2)
            result_cpp = glob.glob(puzzle_directory+"/screenshots/*.png")[0]
            ax[0].imshow(plt.imread(result_cpp))
            ax[0].set_title("Results CPP")
            ground_truth_image = glob.glob(puzzle_directory+"/ground_truth.*")[0]
            ax[1].imshow(plt.imread(ground_truth_image))
            ax[1].set_title("ground_truth_image")
            plt.show()
            plt.waitforbuttonpress()
        

if __name__ == "__main__":
    puzzles_paths = glob.glob(args.puzzles_dir+"/*/Puzzle*")

    for puzzle_path in puzzles_paths:
        name = os.path.basename(puzzle_path)
        image_name = puzzle_path.split("\\")[-2]
        puzzle_num = re.search("\d+$",name).group(0)
        
        run_solver(image_name,int(puzzle_num),int(args.noise_level),bool(args.is_interactive))




    