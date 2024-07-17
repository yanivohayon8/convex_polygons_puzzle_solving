import argparse
from src.solvers import v2 as solverV2
from src.recipes import factory as recipes_factory
from src.evaluator import AreaOverlappingEvaluator,Qpos
from src.physics import restore_assembly_img 
import glob
import os
import re
import datetime
import random
import matplotlib.pyplot as plt
from src import shared_variables

parser = argparse.ArgumentParser()
parser.add_argument("--db", default="1")
parser.add_argument("--puzzle_num", default="")
parser.add_argument("--puzzle_noise_level", default="0")
parser.add_argument("--pairwise_recipe_name", default="SD1Pairwise")#SyntheticPairwise
parser.add_argument('--debug', action='store_true')
parser.add_argument('--no-debug', dest='debug', action='store_false')
parser.set_defaults(debug=False)
args = parser.parse_args()


if __name__ == "__main__":

    def plot_final_polygons(polygons, ax = None,seed = 10):

        if ax is None:
            _,ax = plt.subplots()
        
        random.seed(seed)

        for poly in polygons:
            xs,ys = poly.exterior.xy
            ax.fill(xs,ys, alpha=0.5,fc=(random.random(),random.random(),random.random()),ec="black")

        ax.set_aspect("equal")

    def solve_puzzle(puzzle_num):
        shared_variables.reset()
        solution,puzzle = solverV2.run(args.db,puzzle_num,args.puzzle_noise_level,
                                       pairwise_recipe_name=args.pairwise_recipe_name,is_debug_solver=args.debug)
        precision = puzzle.evaluate_precision(solution.get_matings())
        print("\tmatings precision is ",precision)
        recall = puzzle.evaluate_recall(solution.get_matings())
        print("\tmatings recall is ",recall)
        overlapping_score  = 0 
        ground_truth_polygons = puzzle.get_ground_truth_puzzle()
        evaluator = Qpos(ground_truth_polygons,solution.simulation_response)
        overlapping_score = evaluator.evaluate()
        print("\tOverlapping with GT score is ", overlapping_score)


        # if True:
        if args.debug:
            print("restore final assembly image")
            _, axs = plt.subplots()
            plot_final_polygons(evaluator.translated_solution_polygons,axs)
            plot_final_polygons(ground_truth_polygons,axs)
            # [piece.load_image() for piece in puzzle.bag_of_pieces]
            # final_img,_ = restore_assembly_img.restore_final_assembly_image(solution.simulation_response,puzzle.bag_of_pieces,
            #                                                                 background_size=(7000,7000))
            # axs.imshow(final_img)
            plt.show()

        return precision, recall,overlapping_score

    if args.puzzle_num != "":
        precision, recall,overlapping_score = solve_puzzle(args.puzzle_num)
        exit()

    puzzles_dir = f"../ConvexDrawingDataset/DB{args.db}"
    puzzles_paths = glob.glob(puzzles_dir+f"/*/noise_{args.puzzle_noise_level}")
    precisions = []
    recalls = []
    overlapps = []
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
            precision, recall,overlapping_score = solve_puzzle(puzzle_num)
            counted_puzzles +=1
            precisions.append(precision)
            recalls.append(recall)
            overlapps.append(overlapping_score)


        except Exception as e:
            print(f"error: could not complete solving puzzle {args.db}/{puzzle_num}: {e}")
            problematic_puzzles.append(puzzle_num)
    
    print(f"Succeed to run on ({counted_puzzles}/{len(puzzles_paths)})puzzles")
    expected_num_puzzles = 20
    # print(f"Calculate the mean of the first {expected_num_puzzles} puzzles as guaranteed")

    if counted_puzzles<= expected_num_puzzles:
        print(f"Precision Mean: {sum(precisions)/(counted_puzzles+1e-5)}")
        print(f"Recall Mean: {sum(recalls)/(counted_puzzles+1e-5)}")
        print(f"Overlapping Mean: {sum(overlapps)/(counted_puzzles+1e-5)}")
    else:
        # TODO:take the excellent in precision
        print(f"Precision Mean: {sum(precisions)/(counted_puzzles+1e-5)}")
        print(f"Recall Mean: {sum(recalls)/(counted_puzzles+1e-5)}")
        print(f"Overlapping Mean: {sum(overlapps)/(counted_puzzles+1e-5)}")