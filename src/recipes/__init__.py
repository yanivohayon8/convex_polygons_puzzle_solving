from src.factory import Factory

class Recipe():

    def cook(self):
        raise NotImplementedError("Implement me in child classes")
    

factory = Factory()