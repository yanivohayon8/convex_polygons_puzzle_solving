import unittest
from src.recipes import factory as recipes_factory
from src.data_structures.physical_assember import AssemblyPlotter
import matplotlib.pyplot as plt

class TestAssemblyPlotter(unittest.TestCase):

    def test_toy_example(self):
        db = 1
        puzzle_num = 19
        noise = 0

        recipe = recipes_factory.create("loadRegularPuzzle",
                                        db=db,puzzle_num=puzzle_num,noise_level=noise)
        bag_of_pieces = recipe.cook()

        plotter = AssemblyPlotter()

        plotter.load_images([bag_of_pieces[0],bag_of_pieces[1]])
        rotation_angles = [0.0,-5.688992977142334]
        # transvectors = [(0.0,0.0),(-403.9974060058594,-452.70440673828125)]
        transvectors = [(0.0,0.0),(-900,-1200.70440673828125)]
        
        # plotter.load_images([bag_of_pieces[1]])
        # rotation_angles = [-5.688992977142334]#[-5.688992977142334] # #
        # transvectors = [(0,0)] #[(-403.9974060058594,-452.70440673828125)]# #

        img = plotter.plot(rotation_angles,transvectors)

        plt.imshow(img)
        plt.show()





if __name__ == "__main__":
    unittest.main()