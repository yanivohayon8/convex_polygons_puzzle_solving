import pandas as pd
from src.data_types.piece import Piece,StableDiffusionExtrapolationDetails
from shapely.geometry.polygon import orient as orient_as_ccw
from src.data_types.mating import Mating
import glob
import json

class Puzzle():

    def __init__(self,puzzle_directory):#,location_path,rels_path,pieces_path) -> None:
        '''
            df_locations - the file path of the csv file ground_truth_puzzle.csv
            rels_path - the file path of the csv file ground_truth_rels.csv
            pieces_path - the file path of the csv file pieces.csv
        '''
        self.puzzle_directory = puzzle_directory
        self.groundtruth_location_path = puzzle_directory + "/ground_truth_puzzle.csv"
        self.groundtruth_rels_path = puzzle_directory + "/ground_truth_rels.csv"
        self.pieces_path = puzzle_directory + "/pieces.csv"
        self.stable_diffusion_extrapolation_path = puzzle_directory + "/Extrapolation"
        self.df_solution_locations = None
        self.df_solution_rels = None
        self.rels_as_mating = []
        self.df_pieces = None
        self.pieces_images = {}
        self.noise = None
        self.matings_max_difference = None
        self.df_raw_pieces = None
        self.ground_truth_matings = None


        # Because we give new edge numbers in ccw order for efficient code and debug, 
        # we maintain the original "messed order" of the indexing of the ground truth, for evaluation.
        # we have here implicit assumption that the edges ids are indexes..
        self.pieces2original_edges ={} # for example {P_0:[2,0,1]}
        self.bag_of_pieces = []
        self.id2piece = {}
        self.is_load_extrapolation_data = True

    
    def load(self):
        self.df_solution_locations = pd.read_csv(self.groundtruth_location_path)
        self.df_solution_rels = pd.read_csv(self.groundtruth_rels_path)
        self.df_pieces = pd.read_csv(self.pieces_path)

        if self.is_load_extrapolation_data:
            self.df_raw_pieces = pd.read_csv(self.stable_diffusion_extrapolation_path+"/raw_pieces.csv")

        self._get_noise_on_puzzle()
    
    def _get_pieces2img_path(self,pieces):
        extentions = ["png","jpg"]
        img_paths = []  
        # [img_paths.extend(glob.glob(self.puzzle_directory+"\\*."+ext)) for ext in extentions]
        [img_paths.extend(glob.glob(self.puzzle_directory+"\\images\\*."+ext)) for ext in extentions]

        for piece in pieces:
            #id_str = str(piece.id)
            id_str = str(int(float(piece.id))) # The id is int written as double in Ofir ground truth, but the image name is in int...
            for path in img_paths:
                file_name = path.split("\\")[-1].split(".")[0]
                if file_name == id_str:
                    piece.img_path = path
                    continue
    
    def _get_pieces2extrapolated_img_path_old(self,pieces):
        extentions = ["png","jpg"]
        img_paths = []  
        # [img_paths.extend(glob.glob(self.puzzle_directory+"\\*."+ext)) for ext in extentions]
        [img_paths.extend(glob.glob(self.puzzle_directory+"\\extrapolated\\*."+ext)) for ext in extentions]

        for piece in pieces:
            #id_str = str(piece.id)
            id_str = str(int(float(piece.id))) # The id is int written as double in Ofir ground truth, but the image name is in int...
            for path in img_paths:
                file_name = path.split("\\")[-1].split(".")[0]
                tmp = file_name.split("-")[-1]
                file_piece_id = tmp.split("_")[0]
                if file_piece_id == id_str:
                    piece.extrapolated_img_path = path
                    continue
    
    def _get_stabe_diffusion_extrapolation_img_path(self,pieces):
        extentions = ["png","jpg"]
        img_paths = []  
        path_to_search = self.stable_diffusion_extrapolation_path+"\\*_ext."
        [img_paths.extend(glob.glob(path_to_search+ext)) for ext in extentions]

        for piece in pieces:
            #id_str = str(piece.id)
            id_str = str(int(float(piece.id))) # The id is int written as double in Ofir ground truth, but the image name is in int...
            for path in img_paths:
                file_name = path.split("\\")[-1].split(".")[0]
                tmp = file_name.split("-")[-1]
                file_piece_id = tmp.split("_")[0]
                if file_piece_id == id_str:
                    piece.extrapolated_img_path = path
                    continue

    def _get_stabe_diffusion_original_img_path(self,pieces):
        extentions = ["png","jpg"]
        img_paths = []  
        # [img_paths.extend(glob.glob(self.puzzle_directory+"\\*."+ext)) for ext in extentions]
        [img_paths.extend(glob.glob(self.puzzle_directory+"\\Extrapolation\\*."+ext)) for ext in extentions]

        for piece in pieces:
            #id_str = str(piece.id)
            id_str = str(int(float(piece.id))) # The id is int written as double in Ofir ground truth, but the image name is in int...
            for path in img_paths:
                file_name = path.split("\\")[-1].split(".")[0]
                if file_name == id_str:
                    piece.stable_diffusion_original_img_path = path
                    continue
    
    def _get_noise_on_puzzle(self):
        try:
            with open(self.puzzle_directory+"/puzzle_details.json", "r") as file:
                    data = json.load(file)
                    # self.noise = float(data["xi"])
                    self.noise = float(data["epsilon"])
                    self.matings_max_difference = self.noise * 4 # Because of the theory - the two vertices pulled to the opposite sides
        except Exception as e:
            try:
                with open(self.puzzle_directory+"/puzzle_details.txt", "r") as file:
                    for line in file:
                        if line.startswith("Global noise level (Xi):"):
                            value = line.split(":")[1].strip()
                            self.noise = float(value)
                            return self.noise
            except FileNotFoundError:
                print("puzzle_details.txt not found.")    
            except Exception as e:
                print("An error occurred:", str(e))

    def get_puzzle_json_details(self):
        with open(self.puzzle_directory+"/puzzle_details.json", "r") as file:
            return json.load(file)     
     

    def get_bag_of_pieces(self,csv_conv="Ofir"):
        self.bag_of_pieces = self._pieces_pd2list(self.df_pieces,csv_conv=csv_conv)
        self._preprocess(self.bag_of_pieces)
        self._get_pieces2img_path(self.bag_of_pieces)

        if self.is_load_extrapolation_data:
            self._get_stabe_diffusion_extrapolation_img_path(self.bag_of_pieces)# self._get_pieces2extrapolated_img_path_old(pieces)
            self._get_stabe_diffusion_original_img_path(self.bag_of_pieces)
            self._get_raw_coordinates(self.bag_of_pieces)
            self._get_extrapolation_details(self.bag_of_pieces)

        self.id2piece = {}

        for piece in self.bag_of_pieces:
            self.id2piece[piece.id] = piece

        return self.bag_of_pieces

    # def load_images(self,img_type="stable_diffusion"):
    #     for piece in self.bag_of_pieces:

    #         if img_type == "original":
    #             piece.load_image()
    #         elif img_type == "extrapolated":
    #             piece.load_extrapolated_image()
    #         elif img_type == "stable_diffusion":
    #             piece.load_extrapolated_image()
    #             piece.load_stable_diffusion_original_image()

    def get_ground_truth_puzzle(self,csv_conv="Ofir"):
        self.df_solution_locations = pd.read_csv(self.groundtruth_location_path)
        pieces = self._pieces_pd2list(self.df_solution_locations,csv_conv=csv_conv)
        self._preprocess(pieces)
        #self._get_pieces2img_path(pieces)
        polygons = [piece.polygon for piece in pieces]
        return polygons


    def _get_extrapolation_details(self,pieces):
        with open(self.stable_diffusion_extrapolation_path+"/extrapolation_details.json", "r") as file:
            data = json.load(file)
            for piece in pieces:
                x_offset = data[f"{piece.id}_x_offset"]
                y_offset = data[f"{piece.id}_y_offset"]
                scale_factor = data["scale_factor"]
                height = data["pixels_extrapolated"]
                piece.extrapolation_details = StableDiffusionExtrapolationDetails(x_offset,y_offset,scale_factor,height)

    def _get_raw_coordinates(self,pieces):
        '''
            This function is used to load the raw pieces - a csv file directly from Ofir input without changes
            These coordinates are used to extract the pictorial content of the extrapolated edges using diffusion model...
        '''
        raw_pieces =  self._pieces_pd2list(self.df_raw_pieces)

        for raw_piece,piece in zip (raw_pieces,pieces):
            piece.raw_coordinates = raw_piece.coordinates
    

    def _pieces_pd2list(self,df:pd.DataFrame,csv_conv="Ofir"):
        if csv_conv!="Ofir":
            raise NotImplementedError("Currently we support only Ofir puzzle style")

        pieces_ids = df["piece"].unique()
        pieces = []
        for _id in pieces_ids:
            vertices = df[df["piece"] == _id]
            coordinates = [(_x,_y) for _x,_y in zip(vertices["x"].values.tolist(),vertices["y"].values.tolist())]
            #pieces.append(Piece(str(int(_id)),coordinates)) # The id is int written as double in Ofir ground truth
            pieces.append(Piece(str(_id),coordinates)) # The id is int written as double in Ofir ground truth

        return pieces

    def _preprocess(self,pieces):
        for i_debug,piece in enumerate(pieces):
            orignial_polygon = piece.polygon
            piece.polygon = orient_as_ccw(orignial_polygon)
            current_coords = piece.get_coords()[:-1]
            org_coords = list(orignial_polygon.exterior.coords)[:-1]
            # org_indexes = [org_coords.index(org_index) for org_index in current_coords]
            curr_i2org_i = {}
            org_i2curr_i = {}

            for i,curr in enumerate(current_coords):
                # curr_i2org_i[i] = org_coords.index(curr)
                curr_i2org_i[(i-1)%len(current_coords)] = org_coords.index(curr) # Tfira: I don't know why it is working
                
                org_i2curr_i[org_coords.index(curr)] = (i-1)%len(current_coords)
            
            self.pieces2original_edges[piece.id] = curr_i2org_i
            piece.ccw_edge2origin_edge = curr_i2org_i
            
            piece.origin_edge2ccw_edge = org_i2curr_i

            
    def get_final_rels(self,csv_conv="Ofir"):
        ''' 
            Load to self.rels_as_mating the rels as list of Mating class instances
            The convention of the csv file should be:
            piece1,edge1,piece2,edge2
        '''
        if len(self.rels_as_mating) > 0:
            return self.rels_as_mating
        
        gd_rels = self.df_solution_rels.values.tolist()
        for rel in gd_rels:
            piece_1 = str(rel[0]) # Because we assume a piece's id is str
            piece_2 = str(rel[2]) # Because we assume a piece's id is str
            self.rels_as_mating.append(
                Mating(piece_1=piece_1,piece_2=piece_2,edge_1=rel[1],edge_2=rel[3])
            )

        return self.rels_as_mating 
    
    def reverse_edge_ids(self,solver_matings):
        return [
            Mating(
                piece_1=mate.piece_1,
                piece_2=mate.piece_2,
                edge_1=self.pieces2original_edges[mate.piece_1][int(mate.edge_1)],
                edge_2=self.pieces2original_edges[mate.piece_2][int(mate.edge_2)]
            ) 
            for mate in solver_matings
            ]

    # def evaluate_rels(self,solver_matings:list):
    #     '''
    #         solver_matings : list of matings (Mating classes instances)
    #     '''
    #     ground_truth_matings = self.get_final_rels()
    #     count_wrong=0

    #     if len(solver_matings)!=len(ground_truth_matings):
    #         print(f"The solver has {len(solver_matings)} matings while the ground truth has {len(ground_truth_matings)} matings")
    #         # return 0
 
    #     for mate in solver_matings:
    #         # new_mate = Mating(piece_1=mate.piece_1,piece_2=mate.piece_2,
    #         #                   edge_1=self.pieces2original_edges[mate.piece_1][int(mate.edge_1)],
    #         #                   edge_2=self.pieces2original_edges[mate.piece_2][int(mate.edge_2)])

    #         if mate not in ground_truth_matings:
    #             count_wrong+=1
        
    #     return 1-count_wrong/len(ground_truth_matings)
    
    def evaluate_precision(self,solver_matings:list):
        '''
            solver_matings : list of matings (Mating classes instances)
        '''
        ground_truth_matings = self.get_final_rels()
        count_correct=0

        for mate in solver_matings:
            new_mate = Mating(piece_1=mate.piece_1,piece_2=mate.piece_2,
                              edge_1=self.pieces2original_edges[mate.piece_1][int(mate.edge_1)],
                              edge_2=self.pieces2original_edges[mate.piece_2][int(mate.edge_2)])

            if new_mate in ground_truth_matings:
                count_correct+=1
        
        
        return count_correct/len(solver_matings)

    def evaluate_recall(self,solver_matings:list):
        '''
            solver_matings : list of matings (Mating classes instances)
        '''
        ground_truth_matings = self.get_final_rels()
        count_correct=0

        for mate in solver_matings:
            new_mate = Mating(piece_1=mate.piece_1,piece_2=mate.piece_2,
                              edge_1=self.pieces2original_edges[mate.piece_1][int(mate.edge_1)],
                              edge_2=self.pieces2original_edges[mate.piece_2][int(mate.edge_2)])

            if new_mate in ground_truth_matings:
                count_correct+=1
        
        
        return count_correct/len(ground_truth_matings)

    def is_ground_truth_mating(self,mating):
        
        if self.ground_truth_matings is None:
            self.ground_truth_matings = self.get_final_rels()
        
        new_mate = Mating(piece_1=mating.piece_1,piece_2=mating.piece_2,
                              edge_1=self.pieces2original_edges[mating.piece_1][int(mating.edge_1)],
                              edge_2=self.pieces2original_edges[mating.piece_2][int(mating.edge_2)])
        
        return new_mate in self.ground_truth_matings

