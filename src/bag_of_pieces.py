import pandas as pd

'''Maybe bag of pieces is not a reperesenting name'''


class puzzle():

    def __init__(self,puzzle_path,rels_path,pieces_path) -> None:
        '''
            df_locations - the file path of the csv file ground_truth_puzzle.csv
            rels_path - the file path of the csv file ground_truth_rels.csv
            pieces_path - the file path of the csv file pieces.csv
        '''
        self.puzzle_path = puzzle_path
        self.rels_path = rels_path
        self.pieces_path = pieces_path
        self.df_locations = None
        self.df_rels = None
        self.df_pieces = None

    def load(self):
        self.df_locations = pd.read_csv(self.puzzle_path)
        self.df_rels = pd.read_csv(self.rels_path)
        self.df_pieces = pd.read_csv(self.pieces_path)

    def get_chaos_pieces(self,csv_conv="Ofir"):
        return self.pieces_pd2list(self.df_pieces,csv_conv=csv_conv)

    def pieces_pd2list(self,df:pd.DataFrame,csv_conv="Ofir"):
        if csv_conv!="Ofir":
            raise NotImplementedError("Currently we support only Ofir puzzle style")

        pieces_ids = df["piece"].unique()
        pieces = []
        for _id in pieces_ids:
            vertices = self.df_pieces[df["piece"] == _id]
            coordinates = [(_x,_y) for _x,_y in zip(vertices["x"].values.tolist(),vertices["y"].values.tolist())]
            pieces.append(coordinates)#''' Import Shapely as pieces?'''

        return pieces

