from src.data_structures.hierarchical_loops import Loop
from src.piece import semi_dice_coef_overlapping
from shapely import Polygon
from PIL import Image
import math

class PhysicalAssembler():

    def __init__(self,http) -> None:
        self.http = http    
        
    def run(self, body,screenshot_name=""):
        response = self.http.send_reconstruct_request(body,screenshot_name=screenshot_name)
        return response
    
    def get_final_coordinates_as_polygons(self,response):
        return [Polygon(piece_json["coordinates"]) for piece_json in response["piecesFinalCoords"] ]
    
    def score_assembly(self,response,area_weight=0.5):
        '''
            response- a json of the following fields
                piecesBeforeEnableCollision: list of polygons (list of tuples)
                AfterEnableCollision: springs sum + springs lengths
        '''
        polygons_coords = [piece_json["coordinates"] for piece_json in response["piecesBeforeEnableCollision"] ]
        overalap_area = semi_dice_coef_overlapping(polygons_coords)
        sum_springs_length = response["AfterEnableCollision"]["sumSpringsLength"]
        
        # Notice: overalap_area is a small a number, and sum_springs_length is a big number....
        return area_weight*overalap_area +  (1-area_weight)*sum_springs_length
    

class AssemblyPlotter():

    def __init__(self,background_width = 3000,background_height = 3000) -> None:
        self.images = []
        self.background_width = background_width
        self.background_height = background_height
    
    def load_images(self,pieces):
        # self.images = [Image.open(piece.img_path).convert('RGB') for piece in pieces]

        self.images = [Image.open(piece.img_path) for piece in pieces]

        # self.images = []

        # for piece in pieces:
        #     original_image = Image.open(piece.img_path)

        #     # Create a new blank RGBA image with the desired dimensions
        #     new_width, new_height = 2000, 2000
        #     new_image = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))

        #     # Calculate the position to center the original image in the new image
        #     x = (new_width - original_image.width) // 2
        #     y = (new_height - original_image.height) // 2

        #     # Paste the original image onto the new image at the calculated position
        #     new_image.paste(original_image, (x, y))

        #     self.images.append(new_image)
    
    def plot(self,rotation_angles,translate_vectors,centers):
        background_img = Image.new("RGBA",(self.background_width,self.background_height),color=0)

        for radians,trans_vec,image,center in zip(rotation_angles,translate_vectors,self.images,centers):
    
            # x = background_img.width//2 + trans_vec[0] - center.x
            # y = background_img.height//2 + trans_vec[1] - center.y
            x = background_img.width//2 + trans_vec[0] - image.width//2 
            y = background_img.height//2 + trans_vec[1]  - image.height//2
            pos = (int(x),int(y))
            
            mask = Image.new("L",image.size,color=255)
            pixels = image.load()

            for row in range(image.size[0]):
                for col in range(image.size[1]):
                    if pixels[row,col] == (0,0,0,0):
                        mask.putpixel((row,col),0)
            
            rotation_angle = math.degrees(-radians)
            rotated_image = image.rotate(rotation_angle,expand=1)
            rotated_mask = mask.rotate(rotation_angle,expand=1)
            background_img.paste(rotated_image,box=pos,mask=rotated_mask)

            # background_img.paste(rotated_image,box=pos)
        
        return background_img



        

