from src.data_structures.hierarchical_loops import Loop
from src.piece import semi_dice_coef_overlapping
from shapely import Polygon


class PhysicalAssembler():

    def __init__(self,http) -> None:
        self.http = http    
        
    def run(self, body,screenshot_name=""):
        response = self.http.send_reconstruct_request(body,screenshot_name=screenshot_name)
        return response
    
    def get_final_coordinates_as_polygons(self,response):
        return [Polygon(piece_json["coordinates"]) for piece_json in response["piecesFinalCoords"] ]
    
    def score_assembly(self,response,area_weight=0.5):
        '''
            response- a json of the following fields
                piecesBeforeEnableCollision: list of polygons (list of tuples)
                AfterEnableCollision: springs sum + springs lengths
        '''
        polygons_coords = [piece_json["coordinates"] for piece_json in response["piecesBeforeEnableCollision"] ]
        overalap_area = semi_dice_coef_overlapping(polygons_coords)
        sum_springs_length = response["AfterEnableCollision"]["sumSpringsLength"]
        
        # Notice: overalap_area is a small a number, and sum_springs_length is a big number....
        return area_weight*overalap_area +  (1-area_weight)*sum_springs_length