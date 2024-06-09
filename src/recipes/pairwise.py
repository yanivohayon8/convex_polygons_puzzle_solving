from typing import Any
from src.data_types.puzzle import Puzzle
from src.feature_extraction import extract_features
from src.pairwise_matchers import pairwise_pieces
from src.recipes import Recipe,factory as recipes_factory
from src.feature_extraction import factory as features_factory
from src.mating_graphs import factory as graphs_factory
from src import shared_variables

DEFAULT_NUM_ROWS_CROP = 5
DEFAULT_COMPATIBILITY_THRESHOLD = 0.4

class GeometricPairwise(Recipe):

    def __init__(self,db,puzzle_num,puzzle_noise_level,puzzle_recipe_name="loadRegularPuzzle",
                 add_geo_features=[],is_load_extrapolation_data=True) -> None:
        self.db = db
        self.puzzle_num = puzzle_num
        self.puzzle_noise_level = puzzle_noise_level
        self.puzzle_recipe_name = puzzle_recipe_name
        self.geo_features = ["EdgeLengthExtractor"] + add_geo_features
        self.matchers_keys = ["EdgeMatcher"]
        self.matchers = {}
        self.graph_wrapper = None
        self.is_load_extrapolation_data=is_load_extrapolation_data

    def cook(self, **kwargs):
        self.puzzle_recipe = recipes_factory.create(self.puzzle_recipe_name,db=self.db,
                                               puzzle_num=self.puzzle_num,noise_level=self.puzzle_noise_level,
                                               is_load_extrapolation_data=self.is_load_extrapolation_data)
        self.puzzle_recipe.cook()
        puzzle = self.puzzle_recipe.puzzle
        bag_of_pieces = puzzle.bag_of_pieces
        extract_features(bag_of_pieces,self.geo_features,**kwargs)
        # features_factory.create("EdgeLengthExtractor",pieces=bag_of_pieces).run()


        self.matchers = pairwise_pieces(bag_of_pieces,self.matchers_keys,
                                   confidence_interval=puzzle.matings_max_difference+1e-3,**kwargs)

        self.graph_wrapper = graphs_factory.create("MatchingGraphWrapper",
                                                   pieces=bag_of_pieces,id2piece=puzzle.id2piece,
                                                   geometric_match_edges=self.matchers["EdgeMatcher"].match_edges)
        self.graph_wrapper.build_graph()

        return self.graph_wrapper

class GeometricPairwiseBuilder():

    def __call__(self, db,puzzle_num,puzzle_noise_level,puzzle_recipe_name="loadRegularPuzzle",add_geo_features=[],
                 is_load_extrapolation_data=True,**_ignored) -> Any:
        return GeometricPairwise(db,puzzle_num,puzzle_noise_level,
                                 puzzle_recipe_name=puzzle_recipe_name,add_geo_features=add_geo_features,is_load_extrapolation_data=is_load_extrapolation_data)



class SD1Pairwise(GeometricPairwise):

    def __init__(self, db,puzzle_num,puzzle_noise_level,
                 puzzle_recipe_name="loadRegularPuzzle",crop_num_rows=DEFAULT_NUM_ROWS_CROP,
                 add_geo_features=[],compatibility_threshold=DEFAULT_COMPATIBILITY_THRESHOLD) -> None:
        super().__init__(db,puzzle_num,puzzle_noise_level,
                         puzzle_recipe_name=puzzle_recipe_name, add_geo_features=add_geo_features)
        self.crop_num_rows = crop_num_rows
        self.extrap = "NormalizeSDExtrapolatorExtractor"
        self.origin = "NormalizeSDOriginalExtractor"
        self.pictorial_pairwisers = ["DotProductExtraToOriginalMatcher"]
        self.compatibility_threshold = compatibility_threshold
    
    def cook(self,is_override_shared_vars=True, **kwargs):
        super().cook(**kwargs)
        puzzle = self.puzzle_recipe.puzzle
        pieces = puzzle.bag_of_pieces

        original_extractor = features_factory.create(self.origin,pieces = pieces,
                                                     crop_num_rows = self.crop_num_rows)
        original_extractor.run()
        extrapolation_extractor = features_factory.create(self.extrap,pieces=pieces,
                                                 channels_mean = original_extractor.channels_mean,crop_num_rows = self.crop_num_rows)
        extrapolation_extractor.run()

        pictorial_matchers = pairwise_pieces(pieces,self.pictorial_pairwisers,
                                            feature_extrapolator=self.extrap,
                                            feature_original=self.origin)
        self.matchers.update(pictorial_matchers)

        self.graph_wrapper = graphs_factory.create("MatchingGraphWrapper",
                                                   pieces=puzzle.bag_of_pieces,id2piece=puzzle.id2piece,
                                                   geometric_match_edges=self.matchers["EdgeMatcher"].match_edges,
                                                   pictorial_matcher = self.matchers[self.pictorial_pairwisers[0]],
                                                   compatibility_threshold=self.compatibility_threshold)
        self.graph_wrapper.build_graph()

        if is_override_shared_vars:
            shared_variables.graph_wrapper = self.graph_wrapper

        return self.graph_wrapper
    

class SD1PairwiseBuilder():

    def __call__(self, db,puzzle_num,puzzle_noise_level,
                 puzzle_recipe_name="loadRegularPuzzle",crop_num_rows=DEFAULT_NUM_ROWS_CROP,
                   add_geo_features=[],compatibility_threshold=DEFAULT_COMPATIBILITY_THRESHOLD,
                     **_ignored) -> Any:
        return SD1Pairwise(db,puzzle_num,puzzle_noise_level,
                            puzzle_recipe_name=puzzle_recipe_name,
                            crop_num_rows=crop_num_rows,add_geo_features=add_geo_features,
                            compatibility_threshold=compatibility_threshold)





class SyntheticPairwise(GeometricPairwise):

    DEFAULT_PERCENTANGE_FALSE_POSITIVES = 0.8 #0.5 #0.65#0.5 #0.8#0.35

    def __init__(self, db, puzzle_num, puzzle_noise_level, 
                 puzzle_recipe_name="loadRegularPuzzle", add_geo_features=[],
                 compatibility_threshold=DEFAULT_COMPATIBILITY_THRESHOLD) -> None:
        super().__init__(db, puzzle_num, puzzle_noise_level, puzzle_recipe_name, add_geo_features)
        self.compatibility_threshold = compatibility_threshold
        self.is_load_extrapolation_data = False

    def cook(self,is_override_shared_vars=True, **kwargs):
        super().cook(**kwargs)

        puzzle = self.puzzle_recipe.puzzle
        pieces = puzzle.bag_of_pieces

        synthesis_matchers = pairwise_pieces(pieces,["SynthesisMatcher"],puzzle=puzzle,
                                             min_positive_score=DEFAULT_COMPATIBILITY_THRESHOLD,
                                             percentage_false_positives=self.DEFAULT_PERCENTANGE_FALSE_POSITIVES)
        self.matchers.update(synthesis_matchers)

        self.graph_wrapper = graphs_factory.create("MatchingGraphWrapper",
                                                   pieces=puzzle.bag_of_pieces,id2piece=puzzle.id2piece,
                                                   geometric_match_edges=self.matchers["EdgeMatcher"].match_edges,
                                                   pictorial_matcher = self.matchers["SynthesisMatcher"])
                                                   #compatibility_threshold=self.compatibility_threshold)
        self.graph_wrapper.build_graph()

        if is_override_shared_vars:
            shared_variables.graph_wrapper = self.graph_wrapper

        return self.graph_wrapper

class SyntheticPairwiseBuilder():

    def __call__(self, db,puzzle_num,puzzle_noise_level,
                 puzzle_recipe_name="loadRegularPuzzle",
                     **_ignored) -> Any:
        return SyntheticPairwise(db,puzzle_num,puzzle_noise_level,
                                 puzzle_recipe_name=puzzle_recipe_name)





recipes_factory.register_builder(GeometricPairwise.__name__,GeometricPairwiseBuilder())
recipes_factory.register_builder(SD1Pairwise.__name__,SD1PairwiseBuilder())
recipes_factory.register_builder(SyntheticPairwise.__name__,SyntheticPairwiseBuilder())