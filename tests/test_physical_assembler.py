import unittest
from src.recipes import factory as recipes_factory
from src.data_structures.physical_assember import AssemblyPlotter
import matplotlib.pyplot as plt

class TestAssemblyPlotter(unittest.TestCase):

    def test_toy_example_print_loaded_images(self):
        db = 1
        puzzle_num = 19
        noise = 0

        recipe = recipes_factory.create("loadRegularPuzzle",
                                        db=db,puzzle_num=puzzle_num,noise_level=noise)
        bag_of_pieces = recipe.cook()

        plotter = AssemblyPlotter()
        
        plotter.load_images([bag_of_pieces[0],bag_of_pieces[1]])

        plt.imshow(plotter.images[1])
        plt.show()
    
    def test_toy_example(self):
        db = 1
        puzzle_num = 19
        noise = 0

        recipe = recipes_factory.create("loadRegularPuzzle",
                                        db=db,puzzle_num=puzzle_num,noise_level=noise)
        bag_of_pieces = recipe.cook()

        plotter = AssemblyPlotter()
        
        plotter.load_images([bag_of_pieces[0],bag_of_pieces[1]])

        print(bag_of_pieces[1].polygon.centroid)
        rotation_angles = [0.0,-5.688992977142334]
        # transvectors = [(0.0,0.0),(-403.9974060058594,-452.70440673828125)]
        # transvectors = [(0.0,0.0),(-147,130)]
        # transvectors = [(0.0,0.0),(-150,130)]
        # centers = [bag_of_pieces[0].polygon.centroid,bag_of_pieces[1].polygon.centroid]
        
        rotation_angles = [0.0,-5.688992977142334]#[-5.688992977142334] # #
        transvectors =[(0.0,0.0),(-403.9974060058594,-452.70440673828125)]# # #[(0,0)] #
        # transvectors = [(0.0,0.0),(-650,-900.70440673828125)]

        img = plotter.plot(rotation_angles,transvectors)
        # img = plotter.plot(rotation_angles,transvectors,centers)

        plt.imshow(img)
        plt.show()

        raise NotImplementedError("This is not working...... rewrite the code (it is hard coded)")







if __name__ == "__main__":
    unittest.main()