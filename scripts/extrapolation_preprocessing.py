import os
import sys
sys.path.append("./")

import argparse
# from ..src.puzzle import Puzzle
from src.data_types.puzzle import Puzzle
from PIL import Image
from PIL import ImageDraw
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("--DB")
parser.add_argument("--puzzle_num")
parser.add_argument("--noise_level")
parser.add_argument("--line_width",default=10)
args = parser.parse_args()
wsl_directory  = "\\\\wsl.localhost\\Ubuntu-22.04\\home\\yanivoha\\lama\\LaMa_test_images"
directory = f"../ConvexDrawingDataset/DB{args.DB}/Puzzle{args.puzzle_num}/noise_{args.noise_level}"
output_directory = f"{directory}/for_extrapolation"

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

extrapolated_image_directory = f"{directory}/extrapolated"
if not os.path.exists(extrapolated_image_directory):
    os.makedirs(extrapolated_image_directory)

with open(f"{output_directory}/params.txt","w") as f:
    f.write(f"line_width {args.line_width}")

puzzle = Puzzle(directory)
puzzle.load()
bag_of_pieces = puzzle.get_bag_of_pieces()

for piece in bag_of_pieces:
    file_name = f"DB-{args.DB}-puzzle-{args.puzzle_num}-noise-{args.noise_level}-{piece.id}"
    output_image_path = f"{output_directory}/{file_name}.png"
    try:
        rgba_image = Image.open(piece.img_path)
        rgb_image = rgba_image.convert("RGB")

        padding_width = args.line_width
        padding_height = args.line_width
        width_offset = padding_width//2
        height_offset = padding_height//2

        final_rgb_img = Image.new("RGB",(rgb_image.width+padding_width,rgb_image.height+padding_height),color=0)
        final_rgb_img.paste(rgb_image,box=(width_offset,height_offset))
        final_rgb_img.save(output_image_path,"PNG")
        print(f"Piece {piece.id}: RGB image saved successfully in {output_directory}.")

        # coords = piece.coordinates + [piece.coordinates[0]]
        polygon = piece.push_original_coordinates(args.line_width)
        coords = [(coord[0]+width_offset,coord[1]+height_offset) for coord in polygon.exterior.coords]


        mask_image = Image.new("RGB",final_rgb_img.size,0)
        drawer = ImageDraw.Draw(mask_image)
        drawer.line(coords,fill=(255,255,255),width=args.line_width)
        
        output_mask_path = f"{output_directory}/{file_name}_mask.png"
        mask_image.save(output_mask_path)
        print(f"Piece {piece.id}: edge mask saved successfully.")

        shutil.copy(output_image_path,wsl_directory)
        shutil.copy(output_mask_path,wsl_directory)
        print(f"Piece {piece.id}: copied to extrapolation model successfully.")

       

    except Exception as e:
        print("error:",e)
    