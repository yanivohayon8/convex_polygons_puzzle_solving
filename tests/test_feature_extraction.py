import unittest 
import cv2
from src.piece import Piece
import matplotlib.pyplot as plt
from src.feature_extraction.pictorial import trans_image,image_edge,EdgePictorialExtractor
import numpy as np
from src.feature_extraction import geometric as geo_extractor 
from src.puzzle import Puzzle
from src.feature_extraction.extrapolator.lama_masking import LamaEdgeExtrapolator,reshape_line_to_image#,OriginalImgExtractor
from PIL import Image

class TestLamaExtrapolation(unittest.TestCase):


    def test_toy_example(self):
        pieces = [
            Piece("0",
                  [
                      (279.26156414925936,0.0),
                        (0.0,400.418000125509),
                        (325.5645334835908,1962.0680983081097),
                        (1260.6015084925616,1329.154326230219)
                      ])
        ]

        pieces[0].extrapolated_img_path = '../ConvexDrawingDataset/DB1/Puzzle19/noise_0\\extrapolated\\rgb-0_mask.png'
        pieces[0].load_extrapolated_image()

        feature_extractor = LamaEdgeExtrapolator(pieces)
        feature_extractor.run()
        assert len(pieces[0].features["edges_extrapolated_lama"]) == 4

        axs_zoomed = plt.subplot()
        jj = 2
        width_extrapolation = 10
        edge_pixels = pieces[0].features["edges_extrapolated_lama"][jj]
        edge_img = reshape_line_to_image(edge_pixels,width_extrapolation)
        axs_zoomed.imshow(edge_img)
        plt.show()


    def test_edge_vs_edge_display(self):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()
        piece_ii = 8
        edge_ii = 0
        piece_jj = 7
        edge_jj = 2
        pieces = [bag_of_pieces[piece_ii],bag_of_pieces[piece_jj]]

        for piece in pieces:
            piece.load_extrapolated_image()

        feature_extractor = LamaEdgeExtrapolator(pieces)
        feature_extractor.run()

        fig,axs = plt.subplots(1,2)
        width_extrapolation = 10 # as preproceessed beforehand
        edges_indices = [edge_ii,edge_jj]
        pieces_indecies = [piece_ii,piece_jj]
        edges_names = [f"P_{pieces_indecies[0]}_E_{edges_indices[0]}",f"P_{pieces_indecies[1]}_E_{edges_indices[1]}"]

        for k in range(2):
            edge_pixels = pieces[k].features["edges_extrapolated_lama"][edges_indices[k]]
            edge_img = reshape_line_to_image(edge_pixels,width_extrapolation) 
            axs[k].imshow(edge_img)
            axs[k].set_title(edges_names[k])

        plt.show()
        edge_ii_length = pieces[0].features["edges_extrapolated_lama"][edges_indices[0]].shape[0]
        edge_jj_length = pieces[1].features["edges_extrapolated_lama"][edges_indices[1]].shape[0]
        assert abs(edge_ii_length -  edge_jj_length) < width_extrapolation, f"{edges_names[0]} length is {edge_ii_length} and {edges_names[1]} length is {edge_jj_length}. The diffrence is too big "



# class TestOriginalImageExtractor(unittest.TestCase):

#     def test_poc(self):
#         db = 1
#         puzzle_num = 19
#         puzzle_noise_level = 0
#         puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
#         puzzle.load()
#         bag_of_pieces = puzzle.get_bag_of_pieces()

#         piece_index = 0
#         edge_index = 1
#         chosen_piece = bag_of_pieces[piece_index]
#         chosen_piece.load_image()
#         width_extrapolation = 50#10

#         curr_coord = chosen_piece.coordinates[edge_index]
#         start_point = (int(curr_coord[0]),int(curr_coord[1]))
#         next_coord = chosen_piece.coordinates[(edge_index+1)%chosen_piece.get_num_coords()]
#         end_point = (int(next_coord[0]),int(next_coord[1]))
        
#         img_rgb = cv2.cvtColor(chosen_piece.img,cv2.COLOR_RGBA2RGB)
#         mask = np.zeros_like(img_rgb)
#         cv2.line(mask,start_point,end_point,(1,1,1),width_extrapolation)
#         masked_image = img_rgb.copy() * mask
#         edge_pixels = masked_image[np.any(mask!=0,axis=2)]
#         # edge_pixels_indices = np.argwhere(np.any(mask!=0,axis=2))
#         edge_pixels_indices = np.argwhere(np.any(masked_image!=0,axis=2))

#         min_row,min_col = np.min(edge_pixels_indices,axis=0)
#         max_row,max_col = np.max(edge_pixels_indices,axis=0)
#         cropped_img = masked_image[min_row:max_row,min_col:max_col,:]
        
#         axs = plt.subplot()
#         axs.imshow(cropped_img)

#         cropped_indices = np.argwhere(np.any(cropped_img!=0,axis=2))
#         # index_center_x,index_center_y = np.mean(cropped_indices,axis=0)
#         # centered_cropped_indices = cropped_indices - np.array([index_center_x,index_center_y],dtype=np.int)
#         # min_x, min_y = np.min(centered_cropped_indices,axis=0)
        

#         min_row_cropped,min_col_cropped = np.min(cropped_indices,axis=0)
#         max_row_cropped,max_col_cropped = np.max(cropped_indices,axis=0)

       

#         # fig,axs_zoomed = plt.subplots(1,2)
#         # edge_img = reshape_line_to_image(edge_pixels,width_extrapolation)
#         # axs_zoomed[0].imshow(np.transpose(edge_img,axes=(1,0,2)))
        
#         # fig,axs = plt.subplots(1,2)
#         # axs[0].imshow(cropped_img)
        

#         # angles_extractor = geo_extractor.AngleLengthExtractor([chosen_piece])
#         # angles_extractor.run()
#         # prev_edge_index = (edge_index-1)%chosen_piece.get_num_coords()
#         # inner_angle = chosen_piece.get_inner_angle(prev_edge_index,edge_index)
#         # inner_angle/=2
#         # img = Image.fromarray(masked_image).rotate(-inner_angle,center=end_point)
#         # axs[1].imshow(img)

#         plt.show()

#     def test_plot_two_edges(self):
#         db = 1
#         puzzle_num = 19
#         puzzle_noise_level = 0
#         puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
#         puzzle.load()
#         bag_of_pieces = puzzle.get_bag_of_pieces()
#         piece_ii = 8
#         edge_ii = 0
#         piece_jj = 7
#         edge_jj = 2
#         pieces = [bag_of_pieces[piece_ii],bag_of_pieces[piece_jj]]

#         for piece in pieces:
#             piece.load_image()

#         feature_extractor = OriginalImgExtractor(pieces)
#         feature_extractor.run()

#         fig,axs = plt.subplots(1,2)
#         width_extrapolation = 10 # as preproceessed beforehand
#         edges_indices = [edge_ii,edge_jj]
#         pieces_indecies = [piece_ii,piece_jj]
#         edges_names = [f"P_{pieces_indecies[0]}_E_{edges_indices[0]}",f"P_{pieces_indecies[1]}_E_{edges_indices[1]}"]

#         for k in range(2):
#             edge_pixels = pieces[k].features["edges_pictorial_content"][edges_indices[k]]
#             edge_img = reshape_line_to_image(edge_pixels,width_extrapolation) 
#             axs[k].imshow(edge_img)
#             axs[k].set_title(edges_names[k])

#         plt.show()



class TestEdgePictorialExtractor(unittest.TestCase):
    
    def test_single_edge(self):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()

        # PARAMS
        piece_index = 0
        edge_index = 1
        sampling_height = 100

        chosen_piece = bag_of_pieces[piece_index]
        chosen_piece.load_image()
        feature_extractor = EdgePictorialExtractor([chosen_piece],sampling_height=sampling_height)
        feature_extractor.run()

        edge_image_ = chosen_piece.features["original_edges_image"][edge_index]["original"]
        plt.imshow(edge_image_)
        plt.show()

    def test_side_by_side(self):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()

        # PARAMS
        sampling_height = 100
        piece_ii = 3
        edge_ii = 0
        piece_jj = 4
        edge_jj = 2
        
        chosen_pieces = [bag_of_pieces[piece_ii],bag_of_pieces[piece_jj]]
        chosen_edges = [edge_ii,edge_jj]
        
        for edge,piece in zip(chosen_edges,chosen_pieces):
            piece.load_image()

            #marking the edge
            coord1 = piece.coordinates[edge]
            vertex1 = (int(coord1[0]),int(coord1[1]))
            coord2 = piece.coordinates[(edge+1)%piece.get_num_coords()]
            vertex2 = (int(coord2[0]),int(coord2[1]))
            piece.img = piece.img.astype(np.uint8) # THIS COULD HAVE SIDE EFFECTS
            cv2.line(piece.img,vertex1,vertex2,(0,255,0),1)

        feature_extractor = EdgePictorialExtractor(chosen_pieces,sampling_height=sampling_height)
        feature_extractor.run()

        edge_image_ii = chosen_pieces[0].features["original_edges_image"][edge_ii]["original"]
        edge_image_jj = chosen_pieces[1].features["original_edges_image"][edge_jj]["original"]
        flipped_edge_image_jj = chosen_pieces[1].features["original_edges_image"][edge_jj]["flipped"]
        
        fig, axs = plt.subplots(2,2)
        axs[0,0].imshow(edge_image_ii)
        axs[0,0].set_title(f"P_{piece_ii}_E_{edge_ii}")
        axs[1,0].imshow(edge_image_jj)
        axs[1,0].set_title(f"P_{piece_jj}_E_{edge_jj}")
        axs[1,1].imshow(flipped_edge_image_jj)
        axs[1,1].set_title(f"P_{piece_jj}_E_{edge_jj} (FLIPPED)")
        axs[0,1].imshow(edge_image_ii)
        axs[0,1].set_title(f"P_{piece_ii}_E_{edge_ii} (SAME)")


        plt.show()




class TestPocPictorial(unittest.TestCase):
    
    def test_sample_edge_quick_dirty_piece_0(self):
        puzzleDirectory = "../ConvexDrawingDataset/DB1/Puzzle19/noise_0"
        piece_id = "0"
        img_path = puzzleDirectory+f"/images/{piece_id}.png"
        # coordinates = [
        #     (0,1144),
        #     (433,1369),
        #     (1939,845),
        #     (1191,0)
        # ]

        coordinates = [
            (279,0),
            (0,400),
            (325,1962),
            (1260,1329)
        ]

        piece = Piece(piece_id,coordinates,img_path)
        piece.load_image()

        curr_index = 3
        next_index = 0

        curr_row = coordinates[curr_index][1]
        curr_col = coordinates[curr_index][0]
        next_row = coordinates[next_index][1]
        next_col = coordinates[next_index][0]

        #plt.imshow(piece.img)
        center_x = int((curr_col+next_col)/2)#piece.img.shape[0]/2 #216
        center_y = int((curr_row+next_row)/2)
        width = int(np.sqrt((curr_col-next_col)**2 + (curr_row-next_row)**2)) #abs(curr_col-next_col)
        #height = abs(next_row-curr_row)
        height_sampling = 500
        
        angle = np.arctan((next_row-curr_row)/(next_col-curr_col))*180/np.pi

        if next_col-curr_col < 0:
            angle +=180

        img_only_rotate_from_center = trans_image(piece.img,center_x,center_y,angle,0,0) # 
        img_only_rotate = trans_image(piece.img,curr_col,curr_row,angle,0,0) # center_x,center_y

        img_rot_and_trans = trans_image(piece.img,curr_col,curr_row,angle,curr_row,curr_col) # this should result as the image is hidding right above the top left corner
        img_height_as_param = trans_image(piece.img,curr_col,curr_row,angle,curr_row-height_sampling,curr_col)
        
        content = img_height_as_param[:height_sampling,:width]

        fig, axs = plt.subplots(2,3)
        axs[0,0].set_title("piece.img")
        axs[0,0].imshow(piece.img)
        axs[0,1].set_title("results")
        axs[0,1].imshow(content)
        axs[0,2].set_title("img_only_rotate_from_center")
        axs[0,2].imshow(img_only_rotate_from_center)
        axs[1,0].set_title("img_only_rotate_from_vertex")
        axs[1,0].imshow(img_only_rotate)
        axs[1,1].set_title("img_rot_and_trans")
        axs[1,1].imshow(img_rot_and_trans)
        axs[1,2].set_title("img_height_as_param")
        axs[1,2].imshow(img_height_as_param)
        
        plt.show()
        pass
    
    def test_sample_edge_quick_dirty(self):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()

        # PARAMS
        piece_index = 2
        edge_index = 1
        width_extrapolation = 100 #10 # for visualization I used 100. note that the extrapolation have width 10

        chosen_piece = bag_of_pieces[piece_index]
        chosen_piece.load_image()
        chosen_piece.load_extrapolated_image()
        next_edge_index = (edge_index+1)%chosen_piece.get_num_coords()

        edge_row = chosen_piece.coordinates[edge_index][1]
        edge_col = chosen_piece.coordinates[edge_index][0]
        next_edge_row = chosen_piece.coordinates[next_edge_index][1]
        next_edge_col = chosen_piece.coordinates[next_edge_index][0]
        angle = np.arctan((next_edge_row-edge_row)/(next_edge_col-edge_col))*180/np.pi

        if next_edge_col-edge_col < 0:
            angle +=180
        
        edge_width = int(np.sqrt((edge_col-next_edge_col)**2 + (edge_row-next_edge_row)**2)) #abs(curr_col-next_col)
        img = chosen_piece.img.copy()
        # img = chosen_piece.extrapolated_img.copy()
        # img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        num_row_padded = 0
        
        if edge_width>img.shape[0]:
            num_row_padded = edge_width - img.shape[0]
        
        num_col_padded = 0
        
        if edge_width>img.shape[1]:
            num_col_padded = edge_width - img.shape[1]

        img = np.pad(img,((0,num_row_padded),(0,num_col_padded),(0,0)),constant_values=0)

        # this should result as the image is hidding right above the top left corner
        img_rotated = trans_image(img,edge_col,edge_row,angle,0,0) 
        img_translated_shift_down = trans_image(img,edge_col,edge_row,angle,edge_row-width_extrapolation,edge_col)
        result = img_translated_shift_down[:width_extrapolation,:edge_width]

        fig, axs = plt.subplots(2,2)
        axs[0,0].set_title("piece")
        axs[0,0].imshow(img)
        axs[0,1].set_title("rotated")
        axs[0,1].imshow(img_rotated)
        axs[1,0].set_title("rotated,translate, shift down")
        axs[1,0].imshow(img_translated_shift_down)
        axs[1,1].set_title("result")
        axs[1,1].imshow(result)

        # ax = plt.subplot()
        # ax.imshow(result)
        
        plt.show()

    def test_image_edge(self):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()

        # PARAMS
        piece_index = 0
        edge_index = 1
        sampling_height = 100

        bag_of_pieces[piece_index].load_image()
        img = bag_of_pieces[piece_index].img#.copy()
        result = image_edge(img,bag_of_pieces[piece_index].coordinates,edge_index,sampling_height)
        plt.imshow(result)
        plt.show()

class TestGeometric(unittest.TestCase):


    def test_edge_length(self):
        pieces = [
            Piece("0",[(-847.4256148049196,409.07035256641507),(-390.6580493044287,580.180048490992),(1039.668350940752,-119.88084521481937),(198.41531316859664,-869.3695558425879)])
        ]

        length_extractor = geo_extractor.EdgeLengthExtractor(pieces)
        length_extractor.run()
        print(pieces[0].features["edges_length"])
    
    def test_angle(self):
        pieces = [
            Piece("0",[(-847.4256148049196,409.07035256641507),(-390.6580493044287,580.180048490992),(1039.668350940752,-119.88084521481937),(198.41531316859664,-869.3695558425879)])
        ]

        angles_extractor = geo_extractor.AngleLengthExtractor(pieces)
        angles_extractor.run()

        print(pieces[0].features["angles"])
    



if __name__ == "__main__":
    unittest.main()