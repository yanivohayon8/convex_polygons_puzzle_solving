import unittest
from src.recipes.puzzle import loadRegularPuzzle
from src.feature_extraction import extract_features
from src.pairwise_matchers.synthesis import SynthesisMatcher

class TestSynthesisMatcher(unittest.TestCase):

    def test_compiles(self,db=1,puzzle_num=19,puzzle_noise_level=1):
        puzzle_recipe = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level)
        bag_of_pieces = puzzle_recipe.cook()
        
        # extract_features(bag_of_pieces,["EdgeLengthExtractor"])
        matcher = SynthesisMatcher(bag_of_pieces,puzzle_recipe.puzzle)
        matcher.pairwise()

        

        




if __name__ == "__main__":
    unittest.main()