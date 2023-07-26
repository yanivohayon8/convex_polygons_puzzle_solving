class Assembly():

    def __init__(self,polygons, matings) -> None:
        '''
            polygons - List of shapely polygons
            matings - list of matings 
        '''
        self.polygons = polygons
        self.matings = matings
    
    def get_polygons(self):
        return self.polygons
    
    def __eq__(self, __value: object) -> bool:
        pass