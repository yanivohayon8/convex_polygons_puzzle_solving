import pandas as pd
from src.piece import Piece

class Puzzle():

    def __init__(self,location_path,rels_path,pieces_path) -> None:
        '''
            df_locations - the file path of the csv file ground_truth_puzzle.csv
            rels_path - the file path of the csv file ground_truth_rels.csv
            pieces_path - the file path of the csv file pieces.csv
        '''
        self.groundtruth_location_path = location_path
        self.groundtruth_rels_path = rels_path
        self.pieces_path = pieces_path
        self.df_solution_locations = None
        self.df_solution_rels = None
        self.df_pieces = None

    def load(self):
        self.df_solution_locations = pd.read_csv(self.groundtruth_location_path)
        self.df_solution_rels = pd.read_csv(self.groundtruth_rels_path)
        self.df_pieces = pd.read_csv(self.pieces_path)

    def get_bag_of_pieces(self,csv_conv="Ofir"):
        return self.pieces_pd2list(self.df_pieces,csv_conv=csv_conv)

    def get_final_puzzle(self,csv_conv="Ofir"):
        return self.pieces_pd2list(self.df_solution_locations,csv_conv=csv_conv)

    def pieces_pd2list(self,df:pd.DataFrame,csv_conv="Ofir"):
        if csv_conv!="Ofir":
            raise NotImplementedError("Currently we support only Ofir puzzle style")

        pieces_ids = df["piece"].unique()
        pieces = []
        for _id in pieces_ids:
            vertices = df[df["piece"] == _id]
            coordinates = [(_x,_y) for _x,_y in zip(vertices["x"].values.tolist(),vertices["y"].values.tolist())]
            pieces.append(Piece(coordinates))

        return pieces

