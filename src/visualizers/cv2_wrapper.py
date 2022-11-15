import cv2
import numpy as np


def rotate(coords,angle):
    r = np.array(
        [np.cos(angle),-np.sin(angle)],
        [np.sin(angle),np.cos(angle)]
    )

    return r.dot(coords)

class Frame():
    pass
    def __init__(self,size=(1024,1024,3),named_window="Vika"):
        self.img = np.zeros(size, np.uint8)
        self.named_window = named_window
        self.is_initialized = False        

    def move_to_screen(self,polys_coords):
        xs = []
        ys = []
        for poly_coord in polys_coords:
            xs = xs + [coord[0] for coord in poly_coord] 
            ys = ys + [coord[1] for coord in poly_coord]
        x_min = min(xs)
        y_min = min(ys)


        delta_x = 0
        delta_y = 0
        if x_min < 0:
            delta_x = -x_min
        
        if y_min < 0:
            delta_y = -y_min

        
        return np.asarray([[(coord[0]-delta_x,coord[1]-delta_y) for coord in poly_coord] for poly_coord in polys_coords])
            
        

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
            cv2.namedWindow(self.named_window,cv2.WINDOW_NORMAL)
        flip = self.img[::-1,:,:]
        cv2.imshow(self.named_window,flip[:,:,::-1])
        # cv2.imshow(self.named_window,np.flip(self.img,axis=))
    
    def wait(self):
        cv2.waitKey(0)

    def destroy(self):
        cv2.destroyAllWindows()
        self.is_initialized = False

