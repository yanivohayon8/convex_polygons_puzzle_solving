import unittest
from src.recipes.puzzle import loadRegularPuzzle
from src.recipes import factory as recipes_factory
from src.mating_graphs.matching_graph import MatchingGraphWrapper
from src.mating_graphs.drawer import MatchingGraphDrawer
import matplotlib.pyplot as plt
from src.pairwise_matchers.stable_diffusion import DotProductExtraToOriginalMatcher
from src.pairwise_matchers.geometric import EdgeMatcher
from src.feature_extraction import extract_features
# from src.feature_extraction.extrapolator.stable_diffusion import NormalizeSDExtrapolatorExtractor,NormalizeSDOriginalExtractor
# from src.feature_extraction import geometric as geo_extractor 
# from src.pairwise_matchers import geometric as geo_pairwiser

class TestGraphDrawer(unittest.TestCase):

    def _load_graph(self,db,puzzle_num,puzzle_noise_level,
                    features,
                    pictorial_matcher="DotProductNoisslessMatcher"):
        
        bag_of_pieces = recipes_factory.create("loadRegularPuzzle",
                                                db=db,puzzle_num=puzzle_num,noise_level=puzzle_noise_level).cook()
        extract_features(bag_of_pieces,features)




        # if "length" in  geo_feature_extractors:
        #     edge_length_extractor = geo_extractor.EdgeLengthExtractor(bag_of_pieces)
        #     edge_length_extractor.run()

        # if "angle" in geo_feature_extractors:
        #     angles_extractor = geo_extractor.AngleLengthExtractor(bag_of_pieces)
        #     angles_extractor.run()

        edge_length_pairwiser = EdgeMatcher(bag_of_pieces)
        edge_length_pairwiser.pairwise(puzzle.matings_max_difference+1e-3)

        # pic_extractor = EdgePictorialExtractor(bag_of_pieces,sampling_height=10)
        # pic_extractor = EdgePictorialAndNormalizeExtractor(bag_of_pieces,sampling_height=10)
        # pic_extractor.run()
        
        # self.pictorial_matcher_ = DotProductNoisslessMatcher(bag_of_pieces,feature_name=pic_extractor.__class__.__name__)
        # self.pictorial_matcher_.pairwise()


        # sampling_height = 4
        # extrapolator_extractor = NormalizeSDExtrapolatorExtractor(bag_of_pieces,extrapolation_height=sampling_height)
        # extrapolator_extractor.run()

        # original_extractor = NormalizeSDOriginalExtractor(bag_of_pieces,sampling_height=sampling_height)
        # original_extractor.run()

        # self.pictorial_matcher_ = DotProductExtraToOriginalMatcher(bag_of_pieces,
        #                                                            extrapolator_extractor.__class__.__name__,
        #                                                            original_extractor.__class__.__name__,
        #                                                            step_size=50)
        # self.pictorial_matcher_.pairwise()

        # wrapper = MatchingGraphWrapper(bag_of_pieces,id2piece,
        #                                         edge_length_pairwiser.match_edges,
        #                                         edge_length_pairwiser.match_pieces_score,
        #                                         pictorial_matcher=self.pictorial_matcher_)
        # wrapper.build_graph()

        # return wrapper

    def _draw_adjacency(self,wrapper:MatchingGraphWrapper,ground_truth_wrapper:MatchingGraphWrapper,ax1,ax2):
        drawer = MatchingGraphDrawer(ground_truth_wrapper)
        drawer.init()

        drawer.draw_adjacency_graph(wrapper,ax=ax1)
        ax1.set_title("Noised")
        drawer.draw_adjacency_graph(ground_truth_wrapper,ax=ax2)
        ax2.set_title("Noiseless")

    def _draw_matching(self,wrapper:MatchingGraphWrapper,ground_truth_wrapper:MatchingGraphWrapper):
        drawer = MatchingGraphDrawer(ground_truth_wrapper)
        drawer.init()

        # Because we you use the normalized dot product
        min_edge_weight = -1
        max_edge_weight = 1
        drawer.draw_graph_matching(wrapper,min_edge_weight=min_edge_weight,max_edge_weight=max_edge_weight)
        drawer.draw_graph_filtered_matching(wrapper,min_edge_weight=min_edge_weight,max_edge_weight=max_edge_weight)
        # self.pictorial_matcher_.plot_scores_histogram()

    def test_draw_pictorial_matches(self):
        db = "1" 
        puzzle_num = 19 #13 #20
        features = ["AngleLengthExtractor","EdgeLengthExtractor",
                    "NormalizeSDExtrapolatorExtractor","NormalizeSDOriginalExtractor"]

        ground_truth_wrapper = self._load_graph(db,puzzle_num,0,features)
        wrapper = self._load_graph(db,puzzle_num,0,features)

        self._draw_matching(wrapper,ground_truth_wrapper)
        # fig, axs = plt.subplots(1,2)
        # self._draw_adjacency(wrapper,ground_truth_wrapper,axs[0],axs[1])
       
        plt.show()

    def test_puzzle_with_missing_pieces(self):
        db = "5" 
        puzzle_num = 1 #13 #20

        ground_truth_wrapper = self._load_graph(db,puzzle_num,0)
        wrapper = self._load_graph(db,puzzle_num,1)

        self._draw_matching(wrapper,ground_truth_wrapper)
        fig, axs = plt.subplots(1,2)
        self._draw_adjacency(wrapper,ground_truth_wrapper,axs[0],axs[1])
       
        plt.show()



    def test_draw_ground_truth(self):
        db = "1"
        puzzle_num = 19
        ground_truth_graph = self._load_graph(db,puzzle_num,0)
        drawer = MatchingGraphDrawer(ground_truth_graph)
        drawer._draw_ground_truth_adjacency()
        # drawer._draw_ground_truth_matching()
        plt.show()
    
    

        
        

if __name__ == "__main__":
    unittest.main()