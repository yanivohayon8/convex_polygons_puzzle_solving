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
parser.add_argument("--is_interactive",default=False)
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

    # ground_truth_polygons = puzzle.get_ground_truth_puzzle()
    # evaluator = AreaOverlappingEvaluator(ground_truth_polygons)
    # overlapping_score = evaluator.evaluate(solution.get_polygons())
    # print("\tSolution overlapping score is ",overlapping_score)

    precision = puzzle.evaluate_precision(solution.get_matings())
    print("\tmatings precision is ",precision)
    recall = puzzle.evaluate_recall(solution.get_matings())
    print("\tmatings recall is ",recall)

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
    
    return precision,recall

if __name__ == "__main__":
    puzzles_paths = glob.glob(args.puzzles_dir+"/*/Puzzle*")
    sum_precision = 0
    sum_recall = 0
    counted_puzzles = 0

    for puzzle_path in puzzles_paths:
        name = os.path.basename(puzzle_path)
        image_name = puzzle_path.split("\\")[-2]
        puzzle_num = re.search("\d+$",name).group(0)
        try:
            precision, recall = run_solver(image_name,int(puzzle_num),int(args.noise_level),bool(args.is_interactive))
            counted_puzzles +=1
            sum_precision +=precision
            sum_recall +=recall

        except Exception as e:
            print(f"error: could not complete solving puzzle {image_name}/Puzzle{puzzle_num}: {e}")
    
    print(f"Succeed to run on {counted_puzzles} puzzles")
    print(f"Precision Mean: {sum_precision/counted_puzzles}")
    print(f"Recall Mean: {sum_recall/counted_puzzles}")



    