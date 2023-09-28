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
                
                self.matching_edges_scores[edge1_i,edge2_j] = self._score_pair(edge1_extrapolated_pixels,edge2_original_pixels)
        
        BIG_NUM = 999999
        min_comp = np.where(np.isneginf(self.matching_edges_scores),BIG_NUM,self.matching_edges_scores).min()
        max_comp = self.matching_edges_scores.max()
        self.matching_edges_scores = (self.matching_edges_scores - min_comp)/(max_comp-min_comp)
    
    def _score_pair(self, edge1_img:np.array, edge2_img:np.array):
        feature_map_img = edge1_img.copy()
        kernel_img = edge2_img.copy()
        
        assert feature_map_img.shape[0] == kernel_img.shape[0]

        if kernel_img.shape[1] > feature_map_img.shape[1]:
            tmp = feature_map_img
            feature_map_img = kernel_img
            kernel_img = tmp
        
        feature_map_img = feature_map_img.astype(np.double)
        kernel_img = kernel_img.astype(np.double)

        products = [-np.inf]
        start_col = 0
        end_col = start_col + kernel_img.shape[1] # both images have the same height (it is sampling_height from the feature extractor)

        kernel_norm = np.linalg.norm(kernel_img)

        masking = np.ones_like(kernel_img)
        # next_item = 1
        # step_item = 0.9

        # for row in range(masking.shape[0]):
        #     masking[row,:] = masking[row,:]*next_item
        #     next_item *= step_item

        while end_col <= feature_map_img.shape[1]:
            receptive_field = feature_map_img[:,start_col:end_col]
            receptive_field_norm = np.linalg.norm(receptive_field)
            # prod = -np.linalg.norm(receptive_field-kernel_img)/kernel_img.size
            prod = np.sum(kernel_img*receptive_field*masking)/receptive_field_norm/kernel_norm
            # prod = np.sum(kernel_img*receptive_field*masking)/receptive_field_norm/kernel_norm
            products.append(prod)
            start_col += self.step_size
            end_col = start_col + kernel_img.shape[1]

        if len(products) == 1:
            return products[0]
        
        return np.mean(products[1:])
    
    def get_score(self, piece1, edge1, piece2, edge2):
        score1 = super().get_score(piece1, edge1, piece2, edge2)
        score2 = super().get_score(piece2,edge2, piece1,edge1)
        return (score1 + score2)/2