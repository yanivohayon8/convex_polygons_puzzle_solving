import numpy as np
import matplotlib.pyplot as plt

class PairwiseMatcher():

    def __init__(self) -> None:
        self.match_pieces_score = {}
        self.piece_adj_mat = None


    def adjacency_matrix(self):
        self.piece_adj_mat = np.zeros(self.match_pieces_score.shape[:2])
        num_pieces = self.match_pieces_score.shape[0]
        for i in range(num_pieces):
            for j in range(num_pieces):

                matching = self.match_pieces_score[i,j]
                if len(matching) > 0:
                    self.piece_adj_mat[i,j] = np.max(self.match_pieces_score[i,j])
                    continue

        return self.piece_adj_mat
    
    def plot_heat_map(self,ax,fig,pieces_labels=None):
        ax.imshow(self.piece_adj_mat,cmap="cool_r") #alpha=0.7

        num_pieces = self.piece_adj_mat.shape[0]
        ax.set_xticks(np.arange(num_pieces),labels=pieces_labels) # , labels=
        ax.set_yticks(np.arange(num_pieces),labels=pieces_labels) # , labels=

        plt.setp(ax.get_xticklabels(),rotation=45,ha="right",rotation_mode="anchor")
        
        for piece_i in range(num_pieces):
            for piece_j in range(num_pieces):
                ax.text(piece_j,piece_i, round(self.piece_adj_mat[piece_i,piece_j],2),
                        ha="center",va="center",color="w")
        
        ax.set_title("Piece adjacency heat map")
        fig.tight_layout()