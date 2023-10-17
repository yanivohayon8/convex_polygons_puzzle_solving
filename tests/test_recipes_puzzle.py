import unittest
from src.recipes.puzzle import loadRegularPuzzle
from src.recipes import factory as recipes_factory

class TestloadRegularPuzzle(unittest.TestCase):
    
    def test_toy_example(self):
        db = 1
        puzzle_num  = 19
        puzzle_noise_level = 0

        recipe = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level)
        bag_of_pieces = recipe.cook()

        assert len(bag_of_pieces) == 10

    def test_from_factory(self):
        db = 1
        puzzle_num  = 19
        puzzle_noise_level = 0

        recipe = recipes_factory.create("loadRegularPuzzle",
                                        db=db,puzzle_num=puzzle_num,noise_level=puzzle_noise_level)
        bag_of_pieces = recipe.cook()

        assert len(bag_of_pieces) == 10



if __name__ == "__main__":
    unittest.main()