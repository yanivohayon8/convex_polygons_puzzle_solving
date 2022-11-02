import pandas as pd

'''Maybe bag of pieces is not a reperesenting name'''


class puzzle():

    def __init__(self,puzzle_path,rels_path,pieces_path) -> None:
        '''
            puzzle_path - the file path of the csv file ground_truth_puzzle.csv
            rels_path - the file path of the csv file ground_truth_rels.csv
            pieces_path - the file path of the csv file pieces.csv
        '''
        self.puzzle_path = puzzle_path
        self.rels_path = rels_path
        self.pieces_path = pieces_path
        self.df_puzzle = None
        self.df_rels = None
        self.df_pieces = None

    def load(self):
        self.df_puzzle = pd.read_csv(self.puzzle_path)
        self.df_rels = pd.read_csv(self.rels_path)
        self.df_pieces = pd.read_csv(self.pieces_path)

    def get_bag_of_pieces(self,csv_conv="Ofir"):
        if csv_conv!="Ofir":
            raise NotImplementedError("Currently we support only Ofir puzzle style")
        
        pieces_ids = self.df_pieces["piece"].unique()
        pieces = []
        for _id in pieces_ids:
            vertices = self.df_pieces[self.df_pieces["piece"] == _id]
            coordinates = [(_x,_y) for _x,_y in zip(vertices["x"].values.tolist(),vertices["y"].values.tolist())]
            pieces.append(coordinates)#''' Import Shapely as pieces?'''

        return pieces

