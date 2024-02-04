import unittest
from src.recipes.puzzle import loadRegularPuzzle
from src.recipes import factory as recipes_factory
from src.data_types.mating import Mating,convert_mating_to_vertex_mating

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

    
    def test_ground_truth_run_in_physics(self):
        db = "1"
        puzzle_num  = 19
        puzzle_noise_level = 0

        recipe = loadRegularPuzzle(db,puzzle_num,puzzle_noise_level)

        bag_of_pieces = recipe.cook(is_load_extrapolation_data=False)

        gd_matings = recipe.puzzle.get_final_rels()
        gd_matings_as_preprocessed_edges = []

        for mating in gd_matings:
            piece1 = recipe.puzzle.id2piece[mating.piece_1]
            edge1 = piece1.origin_edge2ccw_edge[mating.edge_1]
            piece2 = recipe.puzzle.id2piece[mating.piece_2]
            edge2 = piece2.origin_edge2ccw_edge[mating.edge_2]

            gd_matings_as_preprocessed_edges.append(Mating(piece_1=piece1.id,edge_1=edge1,piece_2=piece2.id,edge_2=edge2))

        print(gd_matings_as_preprocessed_edges)
        print(bag_of_pieces[0])











if __name__ == "__main__":
    unittest.main()