from PIL import Image,ImageDraw
import math
from shapely.geometry import Polygon as ShapelyPolygon
from shapely import affinity 

LOW_NOISE_TRANSPARENCY = 20



def center_of_mass(poly:ShapelyPolygon):   
    vertices = list(poly.exterior.coords)[:-1]
    # Initialize variables for weighted sums
    sum_x = 0
    sum_y = 0
    
    # Iterate through each edge of the polygon
    for i in range(len(vertices)):
        x_i, y_i = vertices[i]
        x_next, y_next = vertices[(i + 1) % len(vertices)]  # Use modulo to handle the last vertex
        
        # Calculate the midpoint of the edge
        mid_x = (x_i + x_next) / 2
        mid_y = (y_i + y_next) / 2
        
        # Update the weighted sums
        sum_x += mid_x
        sum_y += mid_y
    
    # Calculate the coordinates of the center of mass
    com_x = sum_x / len(vertices)
    com_y = sum_y / len(vertices)
    
    return com_x, com_y

def position_final_assembly_image(assembly_json,bag_of_pieces,background_size=(3000,3000),scaled=1/3): #,scaled=1/3
    screen_center_x = background_size[0]//2
    screen_center_y = background_size[1]//2 

    first_piece_offset_x = None
    first_piece_offset_y = None
    positions = []

    # for coords_json in assembly_json[f"piecesFinalCoords"]:
    for coords_json in assembly_json[f"piecesFinalTransformation"]:
        for piece in bag_of_pieces:
            if str(piece.id) == coords_json["pieceId"]:
                # piece_final_polygon = ShapelyPolygon(coords_json["coordinates"])
                # tx,ty = int(piece_final_polygon.centroid.x),int(piece_final_polygon.centroid.y)

                tx,ty = int(coords_json["translateVectorX"]),int(coords_json["translateVectorY"])

                tx*=scaled
                ty*=scaled

                if first_piece_offset_x is None:
                    first_piece_offset_x = tx
                    first_piece_offset_y = ty
                
                tx = tx - first_piece_offset_x
                ty = ty - first_piece_offset_y
            

                img_width = piece.img.shape[1]#*scaled
                img_height = piece.img.shape[0]#*scaled

                # aspect_ratio = img_width/img_height if img_width/img_height<1 else img_height/img_width

                # Because the origin is in the top-left corner
                pos_x = int(screen_center_x + tx - img_width//2)
                pos_y = int(screen_center_y + ty - img_height//2)
                final_pos = (pos_x,pos_y)
                
                # final_pos = (int(tx),int(ty))

                positions.append(final_pos)
                break
            
    return positions 

def mask_final_assembly_image(assembly_json,bag_of_pieces):
    masks = []

    for transformation in assembly_json[f"piecesFinalTransformation"]:
        for piece in bag_of_pieces:
            if str(piece.id) == transformation["pieceId"]:
                piece_img = Image.fromarray(piece.img)

                piece_mask = Image.new("L",piece_img.size,color=255)
                pixels = piece_img.load()

                for row in range(piece_img.size[0]):
                    for col in range(piece_img.size[1]):
                        if pixels[row,col]  == (0,0,0):
                            piece_mask.putpixel((row,col),0)

                rot_degrees= math.degrees(transformation["rotationRadians"])
                rot_degrees = rot_degrees * -1
                rotated_mask = piece_mask.rotate(rot_degrees)
                masks.append(rotated_mask)
                break
    
    return masks

def rotate_pieces_img_final_assembly_image(assembly_json,bag_of_pieces):
    imgs = []

    for transformation in assembly_json[f"piecesFinalTransformation"]:
        for piece in bag_of_pieces:
            if str(piece.id) == transformation["pieceId"]:
                piece_img = Image.fromarray(piece.img)

                rot_degrees= math.degrees(transformation["rotationRadians"])
                rot_degrees = rot_degrees * -1
                rotated_img = piece_img.rotate(rot_degrees)
                imgs.append(rotated_img)

                break
    
    return imgs

def restore_final_assembly_image(assembly_json,bag_of_pieces,background_size=(3000,3000),scaled=1/3):
    background_img = Image.new("RGB",background_size,color=0)
    screen_center_x = background_size[0]//2
    screen_center_y = background_size[1]//2
    debug_positions = []

    def find_center(piece_polygon):
        # mass_x,mass_y = center_of_mass(piece_polygon)
        mass_x,mass_y = (piece_polygon.centroid.x,piece_polygon.centroid.y)
        mass_x*=scaled
        mass_y*=scaled

        return mass_x,mass_y

    # Since we need to find the scaled transformation, but for pin (in the middle) piece scaled*0=0
    pinned_piece_mass_x = None
    pinned_piece_mass_y = None
    pinned_piece_id = None

    for transformation in assembly_json[f"piecesFinalTransformation"]:
        if transformation["rotationRadians"] == 0 and transformation["translateVectorX"] == 0 and transformation["translateVectorY"] == 0:
            for piece in bag_of_pieces:
                if str(piece.id) == transformation["pieceId"]:
                    pinned_piece_mass_x,pinned_piece_mass_y = find_center(piece.polygon)
                    pinned_piece_id = transformation["pieceId"]

    # Finding the transformation
    for transformation in assembly_json[f"piecesFinalTransformation"]:
        for piece in bag_of_pieces:
            if str(piece.id) == transformation["pieceId"]:

                '''Masking'''
                piece_img = Image.fromarray(piece.img)
                piece_mask = Image.new("L",piece_img.size,color=255)
                pixels = piece_img.load()

                for row in range(piece_img.size[0]):
                    for col in range(piece_img.size[1]):
                        if pixels[row,col]  == (0,0,0):
                            piece_mask.putpixel((row,col),0)

                rot_degrees = math.degrees(transformation["rotationRadians"])
                rot_degrees = rot_degrees * -1

                piece_polygon = piece.polygon

                mass_x,mass_y = find_center(piece_polygon)

                rotated_mask = piece_mask.rotate(rot_degrees,center=(mass_x,mass_y))

                '''Rotating img'''
                rotated_img = piece_img.rotate(rot_degrees,center=(mass_x,mass_y))

                '''Position'''
                tx,ty = transformation["translateVectorX"],transformation["translateVectorY"]
                tx*=scaled
                ty*=scaled

                # Because the origin is in the top-left corner
                pos_x = int(screen_center_x + tx - mass_x)
                pos_y = int(screen_center_y + ty - mass_y)

                # Because the pinned piece position is at 0.0 and scaled*0 =0
                if pinned_piece_id != transformation["pieceId"]:
                    pos_x-=int(pinned_piece_mass_x)
                    pos_y-=int(pinned_piece_mass_y)

                final_pos = (pos_x,pos_y)
                debug_positions.append(final_pos)

                background_img.paste(rotated_img,box=final_pos,mask=rotated_mask)

                
    
    return background_img,debug_positions