import unittest 
from src.pairwise_matchers.geometric import EdgeMatcher
import numpy as np
import matplotlib.pyplot as plt
from src.feature_extraction.geometric import EdgeLengthExtractor
from src.pairwise_matchers.geometric import EdgeMatcher
from src.piece import Piece
from src.feature_extraction.extrapolator.lama_masking import LamaEdgeExtrapolator
from src.feature_extraction.pictorial import EdgePictorialExtractor,EdgePictorialAndNormalizeExtractor
from src.pairwise_matchers.pictorial import NaiveExtrapolatorMatcher,DotProductNoisslessMatcher
from src.pairwise_matchers.stable_diffusion import DotProductExtraToOriginalMatcher
from src.puzzle import Puzzle




class TestDotProductNoisslessMatcher(unittest.TestCase):

    def test_toy_example(self):
        
        images_dir = "../ConvexDrawingDataset/DB1/Puzzle19/noise_0\\for_extrapolation"

        bag_of_pieces = [
            Piece("3",
                  [(359.6934234692053,0.0),(0.0,1182.1466364589978),(552.5547553983743,664.8981548785887)],
                  img_path=f'{images_dir}\\DB-1-puzzle-19-noise-0-3.png'),
            Piece("4",
                  [(892.8888169403926,2033.45176941104),(0.0,0.0),(211.833995449535,1002.4259449236998)],
                  img_path=f'{images_dir}\\DB-1-puzzle-19-noise-0-4.png'),
            Piece("5",
                  [(0.0,1595.1806656860645),(160.30040305844886,1601.4394492589781),(474.0201114068477,912.6414795354285),(11.914194622491777,0.0)],
                  img_path=f'{images_dir}\\DB-1-puzzle-19-noise-0-5.png'),
            Piece("6",
                  [(1022.2569034805347,0.0),(0.0,68.71924696099452),(321.1597911884128,744.9290577022039)],
                  img_path=f'{images_dir}\\DB-1-puzzle-19-noise-0-6.png')
        ]

        for piece in bag_of_pieces:
            piece.load_image()
        
        feature_extractor = EdgePictorialExtractor(bag_of_pieces,sampling_height=5)
        feature_extractor.run()

        matcher = DotProductNoisslessMatcher(bag_of_pieces)
        matcher.pairwise()

        score = matcher.get_score("3","0","4","2")
        print(score)
        assert np.isneginf(matcher.get_score("3","0","3","2"))
        assert np.isneginf(matcher.get_score("3","0","3","1"))
        assert np.isneginf(matcher.get_score("3","0","3","0"))
        assert np.isneginf(matcher.get_score("4","0","4","2"))
        assert np.isneginf(matcher.get_score("4","0","4","1"))
        assert np.isneginf(matcher.get_score("4","0","4","0"))


    def test_two_edges(self):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()

        piece_ii = 5
        edge_ii = 1
        piece_jj = 6
        edge_jj = 0
        
        chosen_pieces = [bag_of_pieces[piece_ii],bag_of_pieces[piece_jj]]
        
        for piece in chosen_pieces:
            piece.load_image()

        pic_extractor = EdgePictorialExtractor(chosen_pieces,sampling_height=10)
        # pic_extractor = EdgePictorialAndNormalizeExtractor(chosen_pieces,sampling_height=10)
        pic_extractor.run()

        pictorial_matcher = DotProductNoisslessMatcher(chosen_pieces,feature_name=pic_extractor.__class__.__name__)

        # pictorial_matcher.pairwise()
        # score = pictorial_matcher.get_score(str(piece_ii),str(edge_ii),str(piece_jj),str(edge_jj))
        edge_ii_dict = chosen_pieces[0].features[pic_extractor.__class__.__name__][edge_ii]
        edge_jj_dict = chosen_pieces[1].features[pic_extractor.__class__.__name__][edge_jj]
        score = pictorial_matcher._score_pair(edge_ii_dict,edge_jj_dict)

        fig, axs = plt.subplots(2,1)
        fig.suptitle(f"Score: {score}")
        
        axs[0].set_title(f"P_{piece_ii}_E_{edge_ii}")
        axs[0].imshow(edge_ii_dict["original"]) 
        axs[1].set_title(f"P_{piece_jj}_E_{edge_jj} (FLIPPED)")
        axs[1].imshow(edge_jj_dict["flipped"])

        plt.show()

    def test_two_pieces_EdgePictorialExtractor(self):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()

        piece_ii = 9
        piece_jj = 7
        
        chosen_pieces = [bag_of_pieces[piece_ii],bag_of_pieces[piece_jj]]
        
        for piece in chosen_pieces:
            piece.load_image()

        pic_extractor = EdgePictorialExtractor(chosen_pieces,sampling_height=50)
        feature_key = pic_extractor.__class__.__name__
        pic_extractor.run()

        pictorial_matcher = DotProductNoisslessMatcher(chosen_pieces)
        pictorial_matcher.pairwise()

        for edge_ii in range(chosen_pieces[0].get_num_coords()):
            for edge_jj in range(chosen_pieces[1].get_num_coords()):

                # Taking the flipped because of the pairwise function
                # edge_image_ii = chosen_pieces[0].features["EdgePictorialExtractor"][edge_ii]["original"]
                # flipped_edge_image_jj = chosen_pieces[1].features["EdgePictorialExtractor"][edge_jj]["flipped"]
                edge_image_ii = chosen_pieces[0].features[feature_key][edge_ii]["original"]
                flipped_edge_image_jj = chosen_pieces[1].features[feature_key][edge_jj]["flipped"]
                score = pictorial_matcher.get_score(str(piece_ii),str(edge_ii),str(piece_jj),str(edge_jj))

                fig, axs = plt.subplots(1,2)
                fig.suptitle(f"Score: {score}")
                edge_ii_name_v1 = f"P_{piece_ii}_E_{edge_ii}"
                
                edge_ii_name_v2 = f"P_{pictorial_matcher.edge2pieceid[edge_ii]}_E_{pictorial_matcher.global_index2local_index[edge_ii]}"

                axs[0].set_title(f"{edge_ii_name_v1}\\{edge_ii_name_v2}")
                axs[0].imshow(edge_image_ii)
                edge_jj_name = f"P_{piece_jj}_E_{edge_jj}" 
                axs[1].set_title(f"{edge_jj_name} (FLIPPED)")
                axs[1].imshow(flipped_edge_image_jj)

                fig.savefig(f"data/ofir/tmp/{edge_ii_name_v1}-{edge_jj_name}.png")
                plt.close(fig)

    def test_two_pieces_EdgePictorialAndNormalizeExtractor(self):
        db = 1
        puzzle_num = 19
        puzzle_noise_level = 0
        puzzle = Puzzle(f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}")
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()

        piece_ii = 9
        piece_jj = 7
        
        chosen_pieces = [bag_of_pieces[piece_ii],bag_of_pieces[piece_jj]]
        
        for piece in chosen_pieces:
            piece.load_image()

        pic_extractor = EdgePictorialAndNormalizeExtractor(chosen_pieces,sampling_height=50)
        pic_extractor.run()
        pictorial_matcher = DotProductNoisslessMatcher(chosen_pieces,feature_name=pic_extractor.__class__.__name__)
        pictorial_matcher.pairwise()


        # Running for the plotting only
        pic_extractor_2 = EdgePictorialExtractor(chosen_pieces,sampling_height=50)
        feature_key = pic_extractor_2.__class__.__name__
        pic_extractor_2.run()


        for edge_ii in range(chosen_pieces[0].get_num_coords()):
            for edge_jj in range(chosen_pieces[1].get_num_coords()):

                # Taking the flipped because of the pairwise function
                # edge_image_ii = chosen_pieces[0].features["EdgePictorialExtractor"][edge_ii]["original"]
                # flipped_edge_image_jj = chosen_pieces[1].features["EdgePictorialExtractor"][edge_jj]["flipped"]
                edge_image_ii = chosen_pieces[0].features[feature_key][edge_ii]["original"]
                flipped_edge_image_jj = chosen_pieces[1].features[feature_key][edge_jj]["flipped"]
                score = pictorial_matcher.get_score(str(piece_ii),str(edge_ii),str(piece_jj),str(edge_jj))

                fig, axs = plt.subplots(1,2)
                fig.suptitle(f"Score: {score}")
                edge_ii_name_v1 = f"P_{piece_ii}_E_{edge_ii}"
                
                edge_ii_name_v2 = f"P_{pictorial_matcher.edge2pieceid[edge_ii]}_E_{pictorial_matcher.global_index2local_index[edge_ii]}"

                axs[0].set_title(f"{edge_ii_name_v1}\\{edge_ii_name_v2}")
                axs[0].imshow(edge_image_ii)
                edge_jj_name = f"P_{piece_jj}_E_{edge_jj}" 
                axs[1].set_title(f"{edge_jj_name} (FLIPPED)")
                axs[1].imshow(flipped_edge_image_jj)

                fig.savefig(f"data/ofir/tmp/{edge_ii_name_v1}-{edge_jj_name}.png")
                plt.close(fig)   

class TestlamaMatcher(unittest.TestCase):

    def test_toy_example(self):
        # bag_of_pieces = [
        #     Piece("3",[(359.6934234692053,0.0),(0.0,1182.1466364589978),(552.5547553983743,664.8981548785887)],extrapolated_img_path='../ConvexDrawingDataset/DB1/Puzzle19/noise_0\\extrapolated\\rgb-3_mask.png'),
        #     Piece("4",[(892.8888169403926,2033.45176941104),(0.0,0.0),(211.833995449535,1002.4259449236998)],extrapolated_img_path='../ConvexDrawingDataset/DB1/Puzzle19/noise_0\\extrapolated\\rgb-4_mask.png'),
        #     Piece("5",[(0.0,1595.1806656860645),(160.30040305844886,1601.4394492589781),(474.0201114068477,912.6414795354285),(11.914194622491777,0.0)],extrapolated_img_path='../ConvexDrawingDataset/DB1/Puzzle19/noise_0\\extrapolated\\rgb-5_mask.png'),
        #     Piece("6",[(1022.2569034805347,0.0),(0.0,68.71924696099452),(321.1597911884128,744.9290577022039)],extrapolated_img_path='../ConvexDrawingDataset/DB1/Puzzle19/noise_0\\extrapolated\\rgb-6_mask.png')
        # ]

        bag_of_pieces = [
            Piece("3",[(359.6934234692053,0.0),(0.0,1182.1466364589978),(552.5547553983743,664.8981548785887)],extrapolated_img_path='../ConvexDrawingDataset/DB1/Puzzle19/noise_0\\extrapolated\\rgb-3_mask.png'),
            Piece("4",[(892.8888169403926,2033.45176941104),(0.0,0.0),(211.833995449535,1002.4259449236998)],extrapolated_img_path='../ConvexDrawingDataset/DB1/Puzzle19/noise_0\\extrapolated\\rgb-4_mask.png')
        ]

        for piece in bag_of_pieces:
            piece.load_extrapolated_image()
        
        feature_extractor = LamaEdgeExtrapolator(bag_of_pieces)
        feature_extractor.run()

        matcher = NaiveExtrapolatorMatcher(bag_of_pieces)
        matcher.pairwise()

        score = matcher.get_score("3","0","4","2")
        print(score)
        assert np.isneginf(matcher.get_score("3","0","3","2"))
        assert np.isneginf(matcher.get_score("3","0","3","1"))
        assert np.isneginf(matcher.get_score("3","0","3","0"))
        assert np.isneginf(matcher.get_score("4","0","4","2"))
        assert np.isneginf(matcher.get_score("4","0","4","1"))
        assert np.isneginf(matcher.get_score("4","0","4","0"))

class TestEdgeMatcher(unittest.TestCase):
    
    def test_toy_example(self):
        # puzzle = Puzzle(f"data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0")
        # puzzle.load()
        # bag_of_pieces = puzzle.get_bag_of_pieces()

        # piece 3,4,5,6 from data/ofir/Pseudo-Sappho_MAN_Napoli_Inv9084/Puzzle1/0
        bag_of_pieces = [
            Piece("3",[(0.0, 850.612398532945), (896.2748322309999, 0.0), (160.42144514933895, 177.15118274973247)]),
            Piece("4",[(1359.7642214436985, 1755.909454053577), (0.0, 0.0), (448.8169164864121, 921.029227021798)]),
            Piece("5",[(0.0, 1398.3336137642618), (138.11642193177977, 1479.9378226308218), (741.2116531849097, 1022.620788274944), (767.7281675820086, 0.0)]),
            Piece("6",[(317.0016030246443, 972.6080337150196), (747.3753572848327, 42.81779674124118), (0.0, 0.0)])
        ]

        edge_length_extractor = EdgeLengthExtractor(bag_of_pieces) # This could be problematic if there are errors there
        edge_length_extractor.run()

        matcher = EdgeMatcher(bag_of_pieces)
        matcher.pairwise(1e-3)

        print("The match edges")
        print(matcher.match_edges)
        print("The scores")
        print(matcher.match_pieces_score)

        matings = matcher.get_pairwise_as_list()
        
        assert len(matings) == 4

        

if __name__ == "__main__":
    unittest.main()