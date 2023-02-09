from shapely import Polygon

class Piece():

    def __init__(self,coordinates:list,img_path=None) -> None:
        self.polygon = Polygon(coordinates)
        self.img_path = img_path
        #self.features = {}