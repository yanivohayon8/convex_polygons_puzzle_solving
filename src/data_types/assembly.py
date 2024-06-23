class Assembly():

    def __init__(self,polygons, matings,simulation_response,physical_score=None,excluded_pieces=[]) -> None:
        '''
            polygons - List of shapely polygons
            matings - list of matings 
        '''
        self.polygons = polygons
        self.matings = matings
        self.physical_score = physical_score
        self.excluded_pieces = excluded_pieces
        self.simulation_response = simulation_response
    
    def get_polygons(self):
        return self.polygons
    
    def get_matings(self):
        return self.matings
    
    def __eq__(self, __value: object) -> bool:
        pass