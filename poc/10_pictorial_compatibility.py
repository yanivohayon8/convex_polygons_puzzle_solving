import numpy as np 
import cv2
import glob
import matplotlib.pyplot as plt


groundtruth_matings = [
    ("P_9_E_2","P_6_E_1"),
    ("P_9_E_0","P_7_E_1"),
    ("P_0_E_3","P_1_E_0"),
    ("P_2_E_0","P_1_E_1"),
    ("P_0_E_1","P_8_E_2")
]


data_dir = "data/poc_10_pictorial_compatibility/" #"../data/poc_10_pictorial_compatibility/"
edge2original_image = {}
edge2extrpolated_image = {}

for file in glob.glob(data_dir+"*.png"):
    file_name = file.split("\\")[-1]
    splitted = file_name.split("_")
    splitted_dash = splitted[0].split("-")
    edge = "_".join(splitted_dash[4:])

    if "ext" in splitted[1]:
        edge2extrpolated_image[edge] = cv2.imread(file)
    elif "original" in splitted[1]:
        edge2original_image[edge] = cv2.imread(file)


# plt.imshow(edge2original_image["P_9_E_2"])

'''
    *****************************
        PREPROCESSING
    *****************************
'''
''''
    COLOR SPACE
'''

def to_lab_color_space(edge2images:dict):
    for edge in edge2images.keys():
        edge2images[edge] = cv2.cvtColor(edge2images[edge],cv2.COLOR_BGR2LAB)
        # edge2extrpolated_image[edge] = cv2.cvtColor(edge2extrpolated_image[edge],cv2.COLOR_BGR2LAB)

'''
    Normalizing
'''
def substract_by_channels_mean(edge2images:dict,channels_mean=None):

    if channels_mean is None:
        channels_sum = np.zeros((3,1))
        pixels_count = 0

        for edge in edge2images.keys():
            img = edge2images[edge]
            channels_sum += np.sum(img,axis=(0,1)).reshape(3,1) 
            pixels_count+= img.shape[0]*img.shape[1]

        channels_mean = (channels_sum/pixels_count).astype(np.double).T

    for edge in edge2images.keys():
        edge2images[edge] = edge2images[edge].astype(np.double) - channels_mean
    
    return channels_mean
    
'''
    flipping
'''
def filp_images(edge2images:dict,axes=(0,1)):
    for edge in edge2images.keys():
        edge2images[edge] = np.flip(edge2images[edge],axis=(0,1))

'''
    Cropping
'''

def crop_rows(edge2images:dict,num_rows=5):
    for edge in edge2images.keys():
        edge2images[edge] = edge2images[edge][:num_rows]

to_lab_color_space(edge2extrpolated_image)
to_lab_color_space(edge2original_image)
channels_mean = substract_by_channels_mean(edge2original_image)
substract_by_channels_mean(edge2extrpolated_image,channels_mean=channels_mean)
filp_images(edge2original_image,axes=(0,1))
crop_rows(edge2original_image,num_rows=5)
crop_rows(edge2extrpolated_image,num_rows=5)



'''
    *****************************
        COMPATIBILITY
    *****************************
'''

def get_non_zero_pixels(img):
    pixels_sum = np.sum(img,axis=2)
    non_black = (pixels_sum!=0)
    return np.where(non_black) 

def compatibility_v1(img1,img2):

    assert img1.shape[0] == img2.shape[0]

    feature_map_img = img2
    kernel_img = img1

    if img1.shape[1] > img2.shape[1]:
        feature_map_img = img1
        kernel_img = img2

    products = []

    start_col = 0
    end_col = start_col + kernel_img.shape[1]
    receptive_field = feature_map_img[:,start_col:end_col]

    x_non_zero_kernel,y_non_zero_kernel = get_non_zero_pixels(kernel_img)
    x_non_zero_receptive_field,y_non_zero_receptive_field = get_non_zero_pixels(receptive_field)
    x_non_zero_mutual = [ind for ind in x_non_zero_kernel if ind in x_non_zero_receptive_field]
    y_non_zero_mutual = [ind for ind in y_non_zero_kernel if ind in y_non_zero_receptive_field]
    pixels_receptive_field = receptive_field[x_non_zero_mutual,y_non_zero_mutual]
    pixels_kernel = kernel_img[x_non_zero_mutual,y_non_zero_mutual]
    receptive_field_norm = np.linalg.norm(pixels_receptive_field)
    kernel_norm = np.linalg.norm(pixels_kernel)

    products.append(np.sum(pixels_kernel*pixels_receptive_field)/receptive_field_norm/kernel_norm)

    return max(products)


scores = []
scores_differences = []

for edge1,edge2 in groundtruth_matings:
    print(f"Comparing {edge1} <===> {edge2}")
    score_1 = compatibility_v1(edge2original_image[edge1],
                                edge2extrpolated_image[edge2])
    print(f"\tscore of {edge1} (original) and {edge2} (extrapolated) is {score_1}")

    score_2 = compatibility_v1(edge2original_image[edge2],
                                edge2extrpolated_image[edge1])
    print(f"\tscore of {edge2} (original) and {edge1} (extrapolated) is {score_2}")
    
    score =score_1/2+score_2/2
    print(f"\tfinal score is {score}")
    scores.append(score)
    scores_differences.append(abs(score_1-score_2))

print()
print("Mean: ", np.mean(scores))
print("Median: ", np.median(scores))
print("Min: ", np.min(scores))
print("Max |score_1-score_2|: ", np.max(scores_differences))


