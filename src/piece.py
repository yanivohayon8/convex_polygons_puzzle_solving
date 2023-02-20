from shapely import Polygon
import numpy as np

class Piece():

    def __init__(self,id:str,coordinates:list,img_path=None) -> None:
        self.id = id
        self.polygon = Polygon(coordinates)
        self.img_path = img_path
        self.features = {}

    def get_coords(self):
        return list(self.polygon.exterior.coords)