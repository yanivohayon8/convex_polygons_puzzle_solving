import pandas as pd
import cv2
from src import RGB_COLORS
import numpy as np
from src.data_types.piece import Piece


class Solver():

    def __init__(self,pieces:list[Piece]):
        self.pieces = pieces
        self.features = {}
        self.pairwise_matching = {}

    def extract_features(self):
        pass

    def pairwise(self):
        assert "Implement me"
    
    def global_optimize(self):
        assert "Implement me"



