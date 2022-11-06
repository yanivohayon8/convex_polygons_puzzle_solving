import pandas as pd
import cv2
from src.visualizers.cv2_wrapper import Frame
from src.consts_and_params import RGB_COLORS

class Assembly():

    def __init__(self,df_adjacency_relations,locations):
        '''
            relations - pandas Dataframe, describes the adjacentsy relations
        '''
        # if df_adjacency_relations.columns != ["pieceA","pieceB","edgeA","edgeB"]:
        #     raise ValueError("follow the convention....")

        self.df_adjacency = df_adjacency_relations
        self.locations = locations


    def draw(self,frame:Frame):
        colors = []
        n_total_colors = len(RGB_COLORS)
        n_polys = len(self.locations)
        if n_polys <= n_total_colors:
            colors = RGB_COLORS[:n_polys]
        else:
            colors = RGB_COLORS * (int(n_polys/n_total_colors) + n_polys%n_total_colors)
        frame.draw_polygons(self.locations,colors)
