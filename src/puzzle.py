import pandas as pd
from src.piece import Piece
from shapely.geometry.polygon import orient as orient_as_ccw
from src.data_structures import Mating

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
        self.rels_as_mating = []
        self.df_pieces = None

        # Because we give new edge numbers in ccw order for efficient code and debug, 
        # we maintain the original "messed order" of the indexing of the ground truth, for evaluation.
        # we have here implicit assumption that the edges ids are indexes..
        self.pieces2original_edges ={} # for example {P_0:[2,0,1]}

    def load(self):
        self.df_solution_locations = pd.read_csv(self.groundtruth_location_path)
        self.df_solution_rels = pd.read_csv(self.groundtruth_rels_path)
        self.df_pieces = pd.read_csv(self.pieces_path)

    def get_bag_of_pieces(self,csv_conv="Ofir"):
        pieces = self._pieces_pd2list(self.df_pieces,csv_conv=csv_conv)
        self._preprocess(pieces)
        return pieces

    def get_final_puzzle(self,csv_conv="Ofir"):
        pieces = self._pieces_pd2list(self.df_solution_locations,csv_conv=csv_conv)
        self._preprocess(pieces)
        return pieces

    def _pieces_pd2list(self,df:pd.DataFrame,csv_conv="Ofir"):
        if csv_conv!="Ofir":
            raise NotImplementedError("Currently we support only Ofir puzzle style")

        pieces_ids = df["piece"].unique()
        pieces = []
        for _id in pieces_ids:
            vertices = df[df["piece"] == _id]
            coordinates = [(_x,_y) for _x,_y in zip(vertices["x"].values.tolist(),vertices["y"].values.tolist())]
            pieces.append(Piece(str(int(_id)),coordinates))

        return pieces

    def _preprocess(self,pieces):
        for piece in pieces:
            orignial_polygon = piece.polygon
            piece.polygon = orient_as_ccw(orignial_polygon)
            current_coords = piece.get_coords()[:-1] # the last coordinate is duplicated
            org_coords = orignial_polygon.exterior.coords[:-1]
            org_indexes = [current_coords.index(org_index) for org_index in org_coords]
            self.pieces2original_edges[piece.id] = org_indexes
            
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
            self.rels_as_mating.append(
                Mating(piece_1=rel[0],piece_2=rel[2],edge_1=rel[1],edge_2=rel[3])
            )

        return self.rels_as_mating 
    
    def evaluate_rels(self,solver_matings:list):
        '''
            solver_matings : list of matings (Mating classes instances)
        '''
        ground_truth_matings = self.get_final_rels()

        if len(solver_matings)!=len(ground_truth_matings):
            print(f"The solver has {len(solver_matings)} matings while the ground truth has {len(ground_truth_matings)} matings")
            return False
 
        for mate in solver_matings:
            new_mate = Mating(piece_1=mate.piece_1,piece_2=mate.piece_2,
                              edge_1=self.pieces2original_edges[mate.piece_1][int(mate.edge_1)],
                              edge_2=self.pieces2original_edges[mate.piece_2][int(mate.edge_2)])

            if new_mate not in ground_truth_matings:
                print(f"The ground truth does not have the mating {mate}")
                return False
        
        return True
