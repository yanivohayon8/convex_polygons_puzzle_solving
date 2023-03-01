from shapely import Polygon
import numpy as np

class Piece():

    def __init__(self,id:str,coordinates:list,img_path=None) -> None:
        self.id = id
        self.polygon = Polygon(coordinates)
        self.coordinates = coordinates
        self.img_path = img_path
        self.features = {}

    def get_coords(self):
        '''
            Get the coordinates of the piece where its center of mass is the origin of the axis.
            This is because we read it from the piece.csv file...
        '''
        return list(self.polygon.exterior.coords)