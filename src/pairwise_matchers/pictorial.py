import numpy as np
from src.feature_extraction.extrapolator.lama_masking import reshape_line_to_image

class PictorialMatcher():
    
    def __init__(self,pieces,feature:str=None) -> None:
        self.feature= feature
        self.pieces = pieces
        self.total_num_edges = 0
        self.edge2pieceid = {}
        self.edge2piece_index = {}
        self.local_index2global_index = {}
        self.global_index2local_index = {}
        edge_i = 0

        for piece_i,piece in enumerate(pieces):
            num_coords = piece.get_num_coords()

            for edge in range(num_coords):
                self.edge2pieceid[edge_i] = piece.id
                self.local_index2global_index[f"{piece.id}-{edge}"] = edge_i
                self.edge2piece_index[edge_i] = piece_i
                self.global_index2local_index[edge_i] = edge
                edge_i+=1

            self.total_num_edges+= num_coords

        self.matching_edges_scores = -np.inf * np.ones((self.total_num_edges,self.total_num_edges))
    
    def pairwise(self):
        for edge1_i in range(self.total_num_edges):
    
            for edge2_j in range(self.total_num_edges):
            
                if self.edge2pieceid[edge1_i] == self.edge2pieceid[edge2_j]:
                    continue

                piece1_i = self.edge2piece_index[edge1_i]
                edge1_local_i = self.global_index2local_index[edge1_i]
                edge1_pixels = self.pieces[piece1_i].features[self.feature][edge1_local_i]

                piece2_j = self.edge2piece_index[edge2_j]
                edge2_local_j = self.global_index2local_index[edge2_j]
                edge2_pixels = self.pieces[piece2_j].features[self.feature][edge2_local_j]
                
                self.matching_edges_scores[edge1_i,edge2_j] = self._score_pair(edge1_pixels,edge2_pixels)

    def get_score(self,piece1,edge1,piece2,edge2):
        global_index1 = self.local_index2global_index[f"{piece1}-{edge1}"]
        global_index2 = self.local_index2global_index[f"{piece2}-{edge2}"]
        return self.matching_edges_scores[global_index1,global_index2] 
    
    def _score_pair(self,edge1_pixels:np.array,edge2_pixels:np.array):
        raise NotImplementedError("implement me")

class NaiveExtrapolatorMatcher(PictorialMatcher):

    def __init__(self, pieces) -> None:
        super().__init__(pieces, "edges_extrapolated_lama")

    def _score_pair(self,edge1_pixels:np.array,edge2_pixels:np.array):
        assert edge1_pixels.shape[1] == 3
        assert edge2_pixels.shape[1] == 3

        small = edge2_pixels
        big = edge1_pixels

        if edge1_pixels.shape[0] < edge2_pixels.shape[0]:
            small = edge1_pixels
            big = edge2_pixels
        
        length_diff = big.shape[0]-small.shape[0]
        right_padd_size = length_diff//2
        left_padd_size = length_diff//2

        if length_diff%2==1:
            right_padd_size+=1

        small_padded = np.pad(small,((left_padd_size,right_padd_size),(0,0)),constant_values=0)

        # A temporary score I found to avoid as possible
        # from numerical instabiility
        return -np.power(np.square(-np.linalg.norm(big-small_padded,ord=2)),1/3)

class ConvolutionV1MatcherToDELETE(NaiveExtrapolatorMatcher):

    def __init__(self, pieces,extrapolation_width,step_size=100) -> None:
        super().__init__(pieces)
        self.extrapolation_width = extrapolation_width
        self.step_size = step_size

    def _score_pair(self,edge1_pixels:np.array,edge2_pixels:np.array):
        img1 = reshape_line_to_image(edge1_pixels,self.extrapolation_width)
        img2 = reshape_line_to_image(edge2_pixels,self.extrapolation_width)

        feature_map = img1
        kernel = img2

        if kernel.shape[0] > feature_map.shape[0]:
            feature_map = img2
            kernel = img1
        
        products = [-999]
        start_row = 0
        end_row = start_row + kernel.shape[0]
        end_col = self.extrapolation_width # both images have the same width
        kernel_norm = np.linalg.norm(kernel)

        while end_row < feature_map.shape[0]:
            receptive_field = feature_map[start_row:end_row,:end_col]
            receptive_field_norm = np.linalg.norm(receptive_field)
            prod = np.sum(kernel*receptive_field)/receptive_field_norm/kernel_norm
            products.append(prod)
            start_row += self.step_size
            end_row = start_row + kernel.shape[0]

        return max(products)


class DotProductNoisslessMatcher(PictorialMatcher):

    def __init__(self, pieces,step_size=50) -> None:
        super().__init__(pieces, "EdgePictorialExtractor")
        self.step_size = step_size # The images width should be almost same in case of noiseless puzzle. so it in this case, it is meaningless

    def _score_pair(self, edge1_img: dict, edge2_img: dict):
        feature_map_img = edge1_img["original"]
        kernel_img = edge2_img["flipped"]
        
        assert feature_map_img.shape[0] == kernel_img.shape[0]


        if kernel_img.shape[1] > feature_map_img.shape[1]:
            tmp = feature_map_img
            feature_map_img = kernel_img
            kernel_img = tmp
        
        products = [-np.inf]
        start_col = 0
        end_col = start_col + kernel_img.shape[1] # both images have the same height (it is sampling_height from the feature extractor)
        kernel_norm = np.linalg.norm(kernel_img)

        while end_col < feature_map_img.shape[1]:
            receptive_field = feature_map_img[:,start_col:end_col]
            receptive_field_norm = np.linalg.norm(receptive_field)
            prod = np.sum(kernel_img*receptive_field)/receptive_field_norm/kernel_norm
            products.append(prod)
            start_col += self.step_size
            end_col = start_col + kernel_img.shape[1]

        return max(products) 