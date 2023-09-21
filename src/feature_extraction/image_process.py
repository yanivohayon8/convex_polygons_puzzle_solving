import numpy as np

def filp_image(img:np.array,axes=(0,1)):
    return np.flip(img,axis=axes)
    # img = np.flip(img,axis=axes)

def crop_rows(img:np.array,num_rows=5):
    return img[:num_rows]

def get_non_zero_pixels(img:np.array):
    pixels_sum = np.sum(img,axis=2)
    non_black = (pixels_sum!=0)
    return np.where(non_black) 

def compute_non_zero_pixels_channels_mean(images:list):
    channels_sum = np.array([[0,0,0]])
    pixels_count = 0

    for img in images:
        x_non_zero_ind,y_non_zero_ind = get_non_zero_pixels(img)
        vector = img[x_non_zero_ind,y_non_zero_ind]#.reshape(3,-1)
        channels_sum += np.sum(vector,axis=0)
        pixels_count += vector.shape[0]

    return (channels_sum.astype(np.double)/pixels_count)

def compute_naive_channels_mean(images):
    channels_sum = np.zeros((3,1))
    pixels_count = 0

    for img in images:
        channels_sum += np.sum(img,axis=(0,1)).reshape(3,1) 
        pixels_count+= img.shape[0]*img.shape[1]

    return (channels_sum/pixels_count).astype(np.double).T

class RecipeFlipCropSubMean():

    def __init__(self,axes_flipped=(0,1),crop_num_rows=5) -> None:
        self.axes_flipped = axes_flipped
        self.crop_num_rows = crop_num_rows

    def compute_channels_mean(self,images:list):
        processed_images = []
        for img in images:
            img_tmp = filp_image(img,axes=self.axes_flipped)
            img_tmp = crop_rows(img_tmp,num_rows=self.crop_num_rows)
            processed_images.append(img_tmp)

        return compute_non_zero_pixels_channels_mean(processed_images)

    def process(self,img:np.array,channels_mean:np.array):
        img = filp_image(img,axes=self.axes_flipped)
        img = crop_rows(img,num_rows=self.crop_num_rows)
        return img - channels_mean 
    
