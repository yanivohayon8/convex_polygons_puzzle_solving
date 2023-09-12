import numpy as np
import matplotlib.pyplot as plt
from src.pairwise_matchers.pictorial import PictorialMatcher

class DotProductExtraToOriginalMatcher(PictorialMatcher):

    def __init__(self, pieces, feature_extrapolator:str,feature_original:str,step_size=50) -> None:
        super().__init__(pieces, "")
        self.feature_extrapolator = feature_extrapolator
        self.feature_original = feature_original
        self.step_size = step_size
    
    def pairwise(self):
        for edge1_i in range(self.total_num_edges):
    
            for edge2_j in range(self.total_num_edges):
            
                if self.edge2pieceid[edge1_i] == self.edge2pieceid[edge2_j]:
                    continue

                piece1_i = self.edge2piece_index[edge1_i]
                edge1_local_i = self.global_index2local_index[edge1_i]
                edge1_extrapolated_pixels = self.pieces[piece1_i].features[self.feature_extrapolator][edge1_local_i]

                piece2_j = self.edge2piece_index[edge2_j]
                edge2_local_j = self.global_index2local_index[edge2_j]
                edge2_original_pixels = self.pieces[piece2_j].features[self.feature_original][edge2_local_j]
                
                self.matching_edges_scores[edge1_i,edge2_j] = self._score_pair(edge1_extrapolated_pixels["same"],edge2_original_pixels["flipped"])
    
    def _score_pair(self, edge1_img:np.array, edge2_img:np.array):
        feature_map_img = edge1_img
        kernel_img = edge2_img
        
        assert feature_map_img.shape[0] == kernel_img.shape[0]

        if kernel_img.shape[1] > feature_map_img.shape[1]:
            tmp = feature_map_img
            feature_map_img = kernel_img
            kernel_img = tmp
        
        products = [-np.inf]
        start_col = 0
        end_col = start_col + kernel_img.shape[1] # both images have the same height (it is sampling_height from the feature extractor)
        kernel_norm = np.linalg.norm(kernel_img)

        while end_col <= feature_map_img.shape[1]:
            receptive_field = feature_map_img[:,start_col:end_col]
            receptive_field_norm = np.linalg.norm(receptive_field)
            prod = np.sum(kernel_img*receptive_field)/receptive_field_norm/kernel_norm
            # prod = -np.linalg.norm(receptive_field-kernel_img)/kernel_img.shape[1]
            products.append(prod)
            start_col += self.step_size
            end_col = start_col + kernel_img.shape[1]

        if len(products) == 1:
            return products[0]
        
        return np.mean(products[1:])