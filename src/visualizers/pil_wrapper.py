import numpy as np



class Frame():
    def __init__(self,file_path=None,size=(1024,1024),color=None):
        self.img = np.zeros(size, np.uint8)
        self.named_window = named_window
        self.is_initialized = False