from shapely import Polygon
import numpy as np
import cv2


class Piece():

    def __init__(self,id:str,coordinates:list,img_path=None) -> None:
        self.id = id
        self.polygon = Polygon(coordinates)
        self.coordinates = coordinates
        self.img_path = img_path
        self.img = None
        self.features = {}

    def load_image(self):
        self.img = cv2.imread(self.img_path,cv2.COLOR_BGR2RGB)

    def get_coords(self):
        '''
            Get the coordinates of the piece where its center of mass is the origin of the axis.
            This is because we read it from the piece.csv file...
        '''
        return list(self.polygon.exterior.coords)#[:-1]