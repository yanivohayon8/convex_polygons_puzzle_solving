# use global states instead of a class (a like singleton)
from src.physics.my_http_client import HTTPClient
from src.piece import semi_dice_coef_overlapping
from shapely import Polygon

db_ = -1
puzzle_num_ = -1
puzzle_noise_level_ = -1
http_ = None


def init(db,puzzle_num,puzzle_noise_level):
    global db_
    global puzzle_num_
    global puzzle_noise_level_
    global http_
    
    db_ = db
    puzzle_num = puzzle_num
    puzzle_noise_level = puzzle_noise_level
    http_ = HTTPClient(db,puzzle_num,puzzle_noise_level)

def simulate(body,screenshot_name=""):
    return http_.send_reconstruct_request(body,screenshot_name=screenshot_name)

def score(assemly_response,area_weight=0.5):
    '''
        response- a json of the following fields
        piecesBeforeEnableCollision: list of polygons (list of tuples)
            AfterEnableCollision: springs sum + springs lengths
    '''
    polygons_coords = [piece_json["coordinates"] for piece_json in assemly_response["piecesBeforeEnableCollision"] ]
    overalap_area = semi_dice_coef_overlapping(polygons_coords)
    sum_springs_length = assemly_response["AfterEnableCollision"]["sumSpringsLength"]
    
    # Notice: overalap_area is a small a number, and sum_springs_length is a big number....
    return area_weight*overalap_area +  (1-area_weight)*sum_springs_length

def get_final_coordinates_as_polygons(response):
    return [Polygon(piece_json["coordinates"]) for piece_json in response["piecesFinalCoords"] ]