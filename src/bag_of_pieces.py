import pandas as pd

class bag_of_pieces():

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