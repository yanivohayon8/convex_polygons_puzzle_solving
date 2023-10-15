import unittest
from src.piece import Piece
from src.feature_extraction import geometric as geo_extractor 
from src.feature_extraction import factory

class TestGeometric(unittest.TestCase):


    def test_edge_length(self):
        pieces = [
            Piece("0",[(-847.4256148049196,409.07035256641507),(-390.6580493044287,580.180048490992),(1039.668350940752,-119.88084521481937),(198.41531316859664,-869.3695558425879)])
        ]

        length_extractor = geo_extractor.EdgeLengthExtractor(pieces)
        length_extractor.run()
        print(pieces[0].features["edges_length"])
    
    def test_edge_length_from_factory(self):
        pieces = [
            Piece("0",[(-847.4256148049196,409.07035256641507),(-390.6580493044287,580.180048490992),(1039.668350940752,-119.88084521481937),(198.41531316859664,-869.3695558425879)])
        ]

        extractor = factory.create("EdgeLengthExtractor",pieces=pieces)
        extractor.run()
        print(pieces[0].features["edges_length"])

    def test_angle(self):
        pieces = [
            Piece("0",[(-847.4256148049196,409.07035256641507),(-390.6580493044287,580.180048490992),(1039.668350940752,-119.88084521481937),(198.41531316859664,-869.3695558425879)])
        ]

        angles_extractor = geo_extractor.AngleLengthExtractor(pieces)
        angles_extractor.run()

        print(pieces[0].features["angles"])
    



if __name__ == "__main__":
    unittest.main()