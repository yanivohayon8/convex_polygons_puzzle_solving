import sys
sys.path.append("./")

import os
import shutil

from src.recipes.puzzle import loadRegularPuzzle
from src.data_types.mating import Mating,convert_mating_to_vertex_mating
from src.physics import assembler
from PIL import Image

import argparse
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument("--DB",default="1_excluded") #"1_excluded" # 1
parser.add_argument("--puzzle_num",default="2") # 19
parser.add_argument("--noise_level",default=1)
parser.add_argument("--is_stage",action=argparse.BooleanOptionalAction)
parser.add_argument("--is_no_erased_pieces_by_noise",action=argparse.BooleanOptionalAction)
args = parser.parse_args()

try:
    db = args.DB 
    # db = "1"
    puzzle_num  = args.puzzle_num #3
    puzzle_noise_level = args.noise_level# 0

    recipe = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level,is_load_extrapolation_data=False)

    bag_of_pieces = recipe.cook()
except Exception as inalAbuk:
    print(inalAbuk)
    print("In inalAbuk")

if args.is_no_erased_pieces_by_noise:
    puzzle_details = recipe.puzzle.get_puzzle_json_details()

    if puzzle_details["n_erased_pieces"] > 0:
        print("Moving and checking puzzles without pieces that were deleted by the noise (the flag was raised)")
        print("Exiting......")
        exit()


gd_matings = recipe.puzzle.get_final_rels()
gd_matings_as_preprocessed_edges = []

csv = ""

for mating in gd_matings:
    piece1 = recipe.puzzle.id2piece[mating.piece_1]
    edge1 = piece1.origin_edge2ccw_edge[mating.edge_1]
    piece2 = recipe.puzzle.id2piece[mating.piece_2]
    edge2 = piece2.origin_edge2ccw_edge[mating.edge_2]
    
    mating = Mating(piece_1=piece1.id,edge_1=edge1,piece_2=piece2.id,edge_2=edge2)
    # gd_matings_as_preprocessed_edges.append(mating)

    try:
        vertex_mating = convert_mating_to_vertex_mating(mating,piece1,piece2)
        csv = csv + vertex_mating
    except Exception as e:
        print("load mating failed (convert_mating_to_vertex_mating)")
        print(mating)
        print("exit")
        exit()


sim_res = None
try:
    sim_res = assembler.simulate(csv,screenshot_name="test_loading_solution")
    print(csv)
except Exception as e:
    print("assembler.simulate failed")

try:
    # sampling a coordinate and hope it is not none
    assert sim_res["piecesFinalCoords"][0]["coordinates"][0] != [None,None], "sampled a coordinate and it is none"
    # print(sim_res)

    postfix = f"Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
    src_directory = f"../ConvexDrawingDataset/DB{db}/{postfix}"

    print("check the simulation had some result and not a black screen")
    screenshot = Image.open(src_directory+f"/screenshots/test_loading_solution_after_collide.png")
    screenshot_gray = screenshot.convert("L")

    is_blackscreen = all(pixel == 0 for pixel in screenshot.getdata())

    if args.is_stage:

        if is_blackscreen:
            print("got black screen of the simulation.....")
            print("Exiting......")
            exit()

        # fig ,ax = plt.subplots()
        # ax.imshow(screenshot)
        # ax.set_title("press a or r")
        # plt.draw()
        # plt.pause(1) # <-------
        # answer = input("type a to accept or r to reject:\t")
        # plt.close(fig)


        
        print("staging...")
        dst_directory = f"../ConvexDrawingDataset/DB{db.split('_')[0]}_staged/{postfix}"

        os.makedirs(dst_directory)

        for item in os.listdir(src_directory):
            src_item_path = os.path.join(src_directory, item)
            dest_item_path = os.path.join(dst_directory, item)

            # Move the item to the destination folder
            shutil.move(src_item_path, dest_item_path)
        
        os.removedirs(src_directory)


except Exception as e:
    print(e)
    print("Post checking failed")
    # print(csv)
