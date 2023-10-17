from typing import Any
from src.puzzle import Puzzle
from src.feature_extraction import extract_features
from src.pairwise_matchers import pairwise_pieces
from src.recipes import Recipe,factory


class GeometricPairwise(Recipe):

    def __init__(self,puzzle:Puzzle,add_geo_features=[]) -> None:
        self.puzzle = puzzle
        self.geo_features = ["EdgeLengthExtractor"] + add_geo_features
        self.matchers_keys = ["EdgeMatcher"]
        self.matchers = {}

    def cook(self, **kwargs):
        bag_of_pieces = self.puzzle.bag_of_pieces
        extract_features(bag_of_pieces,self.geo_features,**kwargs)
        self.matchers = pairwise_pieces(bag_of_pieces,self.matchers_keys,
                                   confidence_interval=self.puzzle.matings_max_difference+1e-3,**kwargs)

        return self.matchers

class GeometricPairwiseBuilder():

    def __call__(self, puzzle:Puzzle,add_geo_features=[],**_ignored) -> Any:
        return GeometricPairwise(puzzle,add_geo_features=add_geo_features)


factory.register_builder(GeometricPairwise.__name__,GeometricPairwiseBuilder())