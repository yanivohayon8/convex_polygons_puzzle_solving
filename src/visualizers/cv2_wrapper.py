import cv2
import numpy as np

class Frame():
    pass
    def __init__(self,size=(1024,1024,3),named_window="Vika"):
        self.img = np.zeros(size, np.uint8)
        self.named_window = named_window
        self.is_initialized = False


    def draw_polygons(self,polygons_coordinates,polygons_colors):
        '''
            polygons_coordinates: list of list of tuples (coordinates)
            polygons_colors: list of 
        '''
        for poly_coords,color in zip(polygons_coordinates,polygons_colors):
            pts = np.asarray(poly_coords,np.int32).reshape((-1,1,2))
            cv2.polylines(self.img,[pts],True,color)
            cv2.fillPoly(self.img,[pts],color)

    def show(self):
        if not self.is_initialized:
            cv2.namedWindow(self.named_window)
        cv2.imshow(self.named_window,self.img)
    
    def wait(self):
        cv2.waitKey(0)

    def destroy(self):
        cv2.destroyAllWindows()
        self.is_initialized = False

