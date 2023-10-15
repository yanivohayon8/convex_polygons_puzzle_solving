from src.piece import Piece
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
