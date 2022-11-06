import pandas as pd
import cv2

class Assembly():

    def __init__(self,df_adjacency_relations,df_locations):
        '''
            relations - pandas Dataframe, describes the adjacentsy relations
        '''
        if df_adjacency_relations.columns != ["pieceA","pieceB","edgeA","edgeB"]:
            raise ValueError("follow the convention....")

        self.df_adjacency = df_adjacency_relations
        self.df_location = df_locations


    def visualize(self):
        pass
    
