# class AssemblyPlotter():

#     def __init__(self,background_width = 5000,background_height = 5000) -> None:
#         # self.images = []
#         self.background_width = background_width
#         self.background_height = background_height
    
#     def _load_images(self,pieces):
#         # self.images = [Image.open(piece.img_path).convert('RGB') for piece in pieces]

#         # self.images = [Image.open(piece.img_path) for piece in pieces]

#         images = []

#         for piece in pieces:
#             original_image = Image.open(piece.img_path)

#             # Create a new blank RGBA image with the desired dimensions
#             new_width, new_height = 2500, 2500
#             new_image = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))

#             # Calculate the position to center the original image in the new image
#             centroid = piece.polygon.centroid

#             # x = new_width//2 - original_image.width//2
#             x = new_width//2 #-  int(centroid.x)
#             x = new_width//2 -  int(centroid.x)
#             # y = new_height//2 - original_image.height//2
#             y = new_height//2 # - int(centroid.y)
#             y = new_height//2  - int(centroid.y)

#             # Paste the original image onto the new image at the calculated position
#             new_image.paste(original_image, (x, y))

#             images.append(new_image)
        
#         return images
    
#     def plot(self,rotation_angles,translate_vectors,pieces):
#         images = self._load_images(pieces)

#         # background_img = Image.new("RGBA",(self.background_width,self.background_height),color=0)
#         background_img = Image.new("RGBA",(self.background_width,self.background_height),color=0)

#         for radians,trans_vec,image,piece in zip(rotation_angles,translate_vectors,images,pieces):
#             centroid = piece.polygon.centroid

#             x = background_img.width//2 + trans_vec[0] - image.width//2 + centroid.x
#             # x = background_img.width//2 + trans_vec[0] - centroid.x//2 
#             y = background_img.height//2 + trans_vec[1]  - image.height//2 + centroid.y
#             # y = background_img.height//2 + trans_vec[1]  - centroid.y//2 
#             pos = (int(x),int(y))
            
#             mask = Image.new("L",image.size,color=255)
#             pixels = image.load()

#             for row in range(image.size[0]):
#                 for col in range(image.size[1]):
#                     if pixels[row,col] == (0,0,0,0):
#                         mask.putpixel((row,col),0)
            
#             rotation_angle = math.degrees(-radians)
#             rotated_image = image.rotate(rotation_angle) # ,expand=1
#             rotated_mask = mask.rotate(rotation_angle) #,expand=1
#             background_img.paste(rotated_image,box=pos,mask=rotated_mask)

#             # background_img.paste(rotated_image,box=pos)
        
#         return background_img