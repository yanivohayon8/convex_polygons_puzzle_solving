import unittest
from src.puzzle import Puzzle
from src.feature_extraction import extract_features,factory
from src.pairwise_matchers import factory as pairwisers_factory

class TestFeatureFactory(unittest.TestCase):

    def test_print_builders(self):
        print(factory._builders.keys())

    def test_extract(self):
        db = "1"
        puzzle_num = "19"
        puzzle_noise_level = 0
        puzzle_directory = f"../ConvexDrawingDataset/DB{db}/Puzzle{puzzle_num}/noise_{puzzle_noise_level}"
        puzzle = Puzzle(puzzle_directory)
        puzzle.load()
        bag_of_pieces = puzzle.get_bag_of_pieces()
        extractors = ["AngleLengthExtractor","EdgeLengthExtractor"]
        extract_features(bag_of_pieces,extractors)

        features = bag_of_pieces[0].features.keys()
        assert "edges_length" in features
        assert "angles" in features


class TestPairwiseMatchersFactory(unittest.TestCase):
    def test_print_builders(self):
        print(pairwisers_factory._builders.keys())

if __name__ == "__main__":
    unittest.main()