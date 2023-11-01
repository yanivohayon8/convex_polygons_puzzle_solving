from src.data_types.piece import Piece
from src.factory import Factory

class Extractor():
    def __init__(self, pieces):
        self.pieces = pieces

    def extract_for_piece(self,piece:Piece):
        raise ("Implement Me")

    def run(self):
        for piece in self.pieces:
            self.extract_for_piece(piece)


factory = Factory()

def extract_features(bag_of_pieces:list,features:list,**kwargs):
    for feature in features:
        extractor = factory.create(feature,pieces=bag_of_pieces,**kwargs)
        extractor.run()