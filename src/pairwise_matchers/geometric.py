
import numpy as np
from src.pairwise_matchers import PairwiseMatcher
import matplotlib.pyplot as plt

class EdgeMatcher():
    
    def __init__(self,pieces) -> None:
        self.pieces = pieces
        self.match_edges = None
        self.match_pieces_score = None

    def pairwise(self, confidence_interval):
        '''
        confidence_interval - the max noise applied on the edge
        '''
        edge_lengths = [piece.features["edges_length"] for piece in self.pieces]
        num_pieces = len(edge_lengths)
        matching_edges = [[] for _ in range(num_pieces**2)]
        matching_scores = [[] for _ in range(num_pieces**2)]

        for i in range(num_pieces):
            for j in range(num_pieces):
                if i!=j:
                    piece_i = edge_lengths[i].reshape(-1,1)
                    piece_j = edge_lengths[j].reshape(1,-1)
                    subs = np.abs(piece_i-piece_j) # tiling
                    match_edges_diff = subs[subs<confidence_interval]

                    if match_edges_diff.size > 0:
                        matching_edges[i*num_pieces+j].append(np.argwhere(subs<confidence_interval))
                        score = confidence_interval*np.ones_like(match_edges_diff) - match_edges_diff
                        score[score<0] = 0
                        matching_scores[i*num_pieces+j] = score

        self.match_edges = np.array(matching_edges,dtype="object").reshape((num_pieces,num_pieces))
        self.match_pieces_score = np.array(matching_scores,dtype="object").reshape((num_pieces,num_pieces))

''' 
    Old 
'''
class GeometricPairwiseMatcher(PairwiseMatcher):

    def __init__(self) -> None:
        super(GeometricPairwiseMatcher,self).__init__()
        self.match_edges = {}

    def pairwise_edges_lengths(self,edge_lengths:np.array,confidence_interval=1.0):
        num_pieces = len(edge_lengths)
        matching_edges = [[] for _ in range(num_pieces**2)]
        matching_scores = [[] for _ in range(num_pieces**2)]

        for i in range(num_pieces):
            for j in range(num_pieces):
                if i!=j:
                    piece_i = edge_lengths[i].reshape(-1,1)
                    piece_j = edge_lengths[j].reshape(1,-1)
                    subs = np.abs(piece_i-piece_j) # tiling
                    match_edges_diff = subs[subs<confidence_interval]

                    if match_edges_diff.size > 0:
                        matching_edges[i*num_pieces+j].append(np.argwhere(subs<confidence_interval))
                        matching_scores[i*num_pieces+j] = match_edges_diff

        self.match_edges = np.array(matching_edges,dtype="object").reshape((num_pieces,num_pieces))
        self.match_pieces_score = np.array(matching_scores,dtype="object").reshape((num_pieces,num_pieces))
    

    def adjacency_matrix(self):
        self.piece_adj_mat = np.zeros(self.match_pieces_score.shape[:2])
        num_pieces = self.match_pieces_score.shape[0]
        for i in range(num_pieces):
            for j in range(num_pieces):
                
                if i == j:
                    # self.piece_adj_mat[i,j] = 0
                    continue

                matching = self.match_pieces_score[i,j]
                if len(matching) > 0:
                    self.piece_adj_mat[i,j] = np.min(matching) #5/(np.min(self.match_pieces_score[i,j]) + 1e-1)# this is the difference from parent class
                    continue

        # self.piece_adj_mat*=0.1
        self.piece_adj_mat = (self.piece_adj_mat-np.min(self.piece_adj_mat))/(np.max(self.piece_adj_mat)-np.min(self.piece_adj_mat))
        self.piece_adj_mat = np.where(self.piece_adj_mat>0,1-self.piece_adj_mat,0)

        return self.piece_adj_mat
    
    def plot_heat_map(self,ax,fig,pieces_labels=None):
        ax.imshow(self.piece_adj_mat,cmap="hot") #alpha=0.7 ,cmap="hot"

        num_pieces = self.piece_adj_mat.shape[0]
        ax.set_xticks(np.arange(num_pieces),labels=pieces_labels) # , labels=
        ax.set_yticks(np.arange(num_pieces),labels=pieces_labels) # , labels=

        plt.setp(ax.get_xticklabels(),rotation=45,ha="right",rotation_mode="anchor")
        
        for piece_i in range(num_pieces):
            for piece_j in range(num_pieces):
                val = round(self.piece_adj_mat[piece_i,piece_j],3)

                text_color = 'black' if val > 0.5 else 'white'

                ax.text(piece_j,piece_i, val ,
                        ha="center",va="center",color=text_color)
        
        ax.set_title("Piece adjacency heat map")
        fig.tight_layout()

    


                
