class Assembly():

    def __init__(self,polygons, matings,physical_score=None) -> None:
        '''
            polygons - List of shapely polygons
            matings - list of matings 
        '''
        self.polygons = polygons
        self.matings = matings
        self.physical_score = physical_score
    
    def get_polygons(self):
        return self.polygons
    
    def get_matings(self):
        return self.matings
    
    def __eq__(self, __value: object) -> bool:
        pass