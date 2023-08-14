from src.mating_graphs.matching_graph import get_piece_name,get_edge_name


class Cycle():

    def __init__(self, matings_chain:list, piece2occurence:dict,debug_graph_cycle=None) -> None:
        self.matings_chain = matings_chain
        self.piece2occurence = piece2occurence
        self.debug_graph_cycle = debug_graph_cycle

    def get_pieces_involved(self):
        return self.piece2occurence.keys()

    def get_num_pieces(self):
        return len(self.piece2occurence.keys())

    def is_all_piece_occur(self,occurence_num):
        for piece_id in self.piece2occurence.keys():
            
            if self.piece2occurence[piece_id] != occurence_num:
                return  False
        
        return True

    def is_has_piece_duplicate_occurence(self):

        for piece_id in self.piece2occurence.keys():
            
            if self.piece2occurence[piece_id] > 2:
                return  True
        
        return False
    
    def __repr__(self) -> str:
        acc = ""
        delimiter = "==>"

        for mate in self.matings_chain:
            acc = acc + delimiter + repr(mate)
        
        return acc[len(delimiter):]