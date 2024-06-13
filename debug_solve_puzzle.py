import argparse
from src.solvers.pictorial.without_missing_pieces import v2 as solverV2
from src.recipes import factory as recipes_factory
from src.evaluator import AreaOverlappingEvaluator
import glob
import os
import re
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--db", default="1")
parser.add_argument("--puzzle_num", default="")
parser.add_argument("--puzzle_noise_level", default="0")
parser.add_argument("--pairwise_recipe_name", default="SyntheticPairwise")
parser.add_argument('--debug', action='store_true')
parser.add_argument('--no-debug', dest='debug', action='store_false')
parser.set_defaults(debug=False)
args = parser.parse_args()


if __name__ == "__main__":

    if args.puzzle_num != "":
        solution,puzzle = solverV2.run(args.db,args.puzzle_num,args.puzzle_noise_level,
                                       pairwise_recipe_name=args.pairwise_recipe_name,is_debug_solver=args.debug)
        precision = puzzle.evaluate_precision(solution.get_matings())
        print("\tmatings precision is ",precision)
        recall = puzzle.evaluate_recall(solution.get_matings())
        print("\tmatings recall is ",recall)
        ground_truth_polygons = puzzle.get_ground_truth_puzzle()
        evaluator = AreaOverlappingEvaluator(ground_truth_polygons)
        overlapping_score = evaluator.evaluate(solution.get_polygons())
        print("\tOverlapping with GT score is ", overlapping_score)
        exit()

    puzzles_dir = f"../ConvexDrawingDataset/DB{args.db}"
    puzzles_paths = glob.glob(puzzles_dir+f"/*/noise_{args.puzzle_noise_level}")
    sum_precision = 0
    sum_recall = 0
    sum_overlapping = 0
    counted_puzzles = 0
    problematic_puzzles = []

    for puzzle_i,puzzle_path in enumerate(puzzles_paths):
        name = os.path.basename(puzzle_path)
        puzzle_num = puzzle_path.split("\\")[-2]
        # expected_path_with_noise = os.path.join(puzzle_path,f"noise_{args.puzzle_noise_level}")

        # # if not os.path.exists(expected_path_with_noise):
        # #     continue

        puzzle_num = puzzle_num[len("Puzzle"):]

        try:
            print("****************************")
            print(f"Solve {args.db}/{puzzle_num}/{args.puzzle_noise_level} ({puzzle_i+1}/{len(puzzles_paths)}) {datetime.datetime.now().time()}") 
            print("****************************")
            solution,puzzle = solverV2.run(args.db,puzzle_num,args.puzzle_noise_level,pairwise_recipe_name=args.pairwise_recipe_name,is_debug_solver=args.debug)
            precision = puzzle.evaluate_precision(solution.get_matings())
            print("\tmatings precision is ",precision)
            recall = puzzle.evaluate_recall(solution.get_matings())
            print("\tmatings recall is ",recall)   

            ground_truth_polygons = puzzle.get_ground_truth_puzzle()
            evaluator = AreaOverlappingEvaluator(ground_truth_polygons)
            overlapping_score = evaluator.evaluate(solution.get_polygons())
            print("\tOverlapping with GT score is ", overlapping_score)

            counted_puzzles +=1
            sum_precision +=precision
            sum_recall +=recall
            sum_overlapping+=overlapping_score


        except Exception as e:
            print(f"error: could not complete solving puzzle {args.db}/{puzzle_num}: {e}")
            problematic_puzzles.append(puzzle_num)
    
    print(f"Succeed to run on ({counted_puzzles}/{len(puzzles_paths)})puzzles")
    print(f"Precision Mean: {sum_precision/(counted_puzzles+1e-5)}")
    print(f"Recall Mean: {sum_recall/(counted_puzzles+1e-5)}")
    print(f"Overlapping Mean: {sum_overlapping/(counted_puzzles+1e-5)}")