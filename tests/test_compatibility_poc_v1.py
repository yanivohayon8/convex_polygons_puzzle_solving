import unittest
import numpy as np 
import cv2
import glob
import matplotlib.pyplot as plt


def load_data(data_dir):
    edge2original_image = {}
    edge2extrpolated_image = {}
    edge2extrapolated_file = {}
    edge2original_file = {}

    for file in glob.glob(data_dir+"*.png"):
        file_name = file.split("\\")[-1]
        splitted = file_name.split("_")
        splitted_dash = splitted[0].split("-")
        edge = "_".join(splitted_dash[4:])

        if "ext" in splitted[1]:
            edge2extrpolated_image[edge] = cv2.imread(file)
            edge2extrapolated_file[edge] = file
        elif "original" in splitted[1]:
            edge2original_image[edge] = cv2.imread(file)
            edge2original_file[edge] = file

    return edge2extrpolated_image,edge2original_image,edge2extrapolated_file,edge2original_file

def to_lab_color_space(edge2images:dict):
    for edge in edge2images.keys():
        edge2images[edge] = cv2.cvtColor(edge2images[edge],cv2.COLOR_BGR2LAB)
        # edge2extrpolated_image[edge] = cv2.cvtColor(edge2extrpolated_image[edge],cv2.COLOR_BGR2LAB)

'''
    Normalizing
'''

def compute_channels_mean(images):
    channels_sum = np.zeros((3,1))
    pixels_count = 0

    for img in images:
        channels_sum += np.sum(img,axis=(0,1)).reshape(3,1) 
        pixels_count+= img.shape[0]*img.shape[1]

    return (channels_sum/pixels_count).astype(np.double).T

def substract_by_channels_mean(edge2images:dict,channels_mean):

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

def get_non_zero_pixels(img):
    pixels_sum = np.sum(img,axis=2)
    non_black = (pixels_sum!=0)
    return np.where(non_black) 

def preprocess_v1(edge2extrpolated_image:dict,edge2original_image:dict):
    to_lab_color_space(edge2extrpolated_image)
    to_lab_color_space(edge2original_image)
    images_meaned = [edge2original_image[edge] for edge in edge2original_image.keys()]
    channels_mean = compute_channels_mean(images_meaned) # list(edge2original_image.items())
    substract_by_channels_mean(edge2original_image,channels_mean)
    substract_by_channels_mean(edge2extrpolated_image,channels_mean)
    axes_filpped = (0,1)
    filp_images(edge2original_image,axes=axes_filpped)
    num_rows_to_crop = 5 
    crop_rows(edge2original_image,num_rows=num_rows_to_crop)
    crop_rows(edge2extrpolated_image,num_rows=num_rows_to_crop)

def preprocess_v2(edge2extrpolated_image:dict,edge2original_image:dict,
                  axes_filpped = (0,1),num_rows_to_crop = 5 ):
    # to_lab_color_space(edge2extrpolated_image)
    # to_lab_color_space(edge2original_image)
    
    filp_images(edge2original_image,axes=axes_filpped)

    crop_rows(edge2original_image,num_rows=num_rows_to_crop)
    crop_rows(edge2extrpolated_image,num_rows=num_rows_to_crop)

    images_meaned = [edge2original_image[edge] for edge in edge2original_image.keys()]
    # [images_meaned.append(edge2extrpolated_image[edge]) for edge in edge2extrpolated_image.keys()]

    channels_mean = compute_channels_mean(images_meaned) 
    substract_by_channels_mean(edge2original_image,channels_mean)
    substract_by_channels_mean(edge2extrpolated_image,channels_mean)
    
def preprocess_v3(edge2extrpolated_image:dict,edge2original_image:dict,
                  axes_filpped = (0,1),num_rows_to_crop = 5):
    filp_images(edge2original_image,axes=axes_filpped)

    crop_rows(edge2original_image,num_rows=num_rows_to_crop)
    crop_rows(edge2extrpolated_image,num_rows=num_rows_to_crop)

    images_meaned = [edge2original_image[edge] for edge in edge2original_image.keys()]
    # [images_meaned.append(edge2extrpolated_image[edge]) for edge in edge2extrpolated_image.keys()]

    channels_sum = np.array([[0,0,0]])
    pixels_count = 0

    for img in images_meaned:
        x_non_zero_ind,y_non_zero_ind = get_non_zero_pixels(img)
        vector = img[x_non_zero_ind,y_non_zero_ind]#.reshape(3,-1)
        channels_sum += np.sum(vector,axis=0)
        pixels_count += vector.shape[0]

    channels_mean = (channels_sum.astype(np.double)/pixels_count)
        
    substract_by_channels_mean(edge2original_image,channels_mean)
    substract_by_channels_mean(edge2extrpolated_image,channels_mean)


    



class TestSkeleton(unittest.TestCase):

    def _compatibiilty(self,img1,img2):
        raise NotImplementedError("Implement me") 

    def _evaluate_matings(self,matings:list,edge2extrpolated_image:dict,edge2original_image:dict):
        scores = []
        scores_differences = []

        for edge1,edge2 in matings:
            print(f"Comparing {edge1} <===> {edge2}")
            score_1 = self._compatibiilty(edge2original_image[edge1],
                                        edge2extrpolated_image[edge2])
            print(f"\tscore of {edge1} (original) and {edge2} (extrapolated) is {score_1}")

            score_2 = self._compatibiilty(edge2original_image[edge2],
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

        return scores

    def _plot_two_edges(self,edge1_extra,edge1_original,edge1,edge2_extra,edge2_original,edge2):
        fig, axs = plt.subplots(2,2)
        axs[0,0].imshow(edge2_extra)
        axs[0,0].set_title(f"{edge2} EXTRAPOLATED")
        axs[0,1].imshow(edge1_extra)
        axs[0,1].set_title(f"{edge1} EXTRAPOLATED")
        axs[1,0].imshow(edge1_original)
        axs[1,0].set_title(f"{edge1} ORIGINAL")
        axs[1,1].imshow(edge2_original)
        axs[1,1].set_title(f"{edge2} ORIGINAL")

        plt.show()

    def _process_v3_and_evaluate(self,matings):
        edge2extrpolated_image,edge2original_image,_,_ = load_data(self.data_dir)
        preprocess_v3(edge2extrpolated_image,edge2original_image)
        scores = self._evaluate_matings(matings,edge2extrpolated_image,edge2original_image)
        scores = np.array(scores)
        print("AFTER MIN MAX SCALE")
        max_score = np.max(scores)
        min_score = np.min(scores)
        scaled_scores = (scores-min_score)/(max_score-min_score)
        print("\t Mean", np.mean(scaled_scores))
        print("\t Median", np.median(scaled_scores))

class TestCompV1(TestSkeleton):

    data_dir = "data/poc_10_pictorial_compatibility/db-1-puzzle-19-noise-0/"

    def _compatibiilty(self,img1,img2):
        assert img1.shape[0] == img2.shape[0]

        feature_map_img = img2
        kernel_img = img1

        if img1.shape[1] > img2.shape[1]:
            feature_map_img = img1
            kernel_img = img2

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

        product = np.sum(pixels_kernel*pixels_receptive_field)/receptive_field_norm/kernel_norm

        return product
    
    def test_ground_truth_noise_0(self):
        ground_truth_matings = [
            ("P_0_E_1","P_8_E_2"),
            ("P_0_E_2","P_5_E_0"),
            ("P_0_E_3","P_1_E_0"),
            ("P_1_E_1","P_2_E_0"),
            ("P_2_E_1","P_5_E_3"),
            ("P_2_E_2","P_3_E_0"),
            ("P_3_E_1","P_5_E_2"),
            ("P_3_E_2","P_4_E_0"),
            ("P_4_E_1","P_6_E_2"),
            ("P_6_E_0","P_5_E_1"),
            ("P_6_E_1","P_9_E_2"),
            ("P_7_E_2","P_8_E_0"),
            ("P_7_E_1","P_9_E_0"),
            ("P_8_E_1","P_9_E_3")
        ]

    
        self._process_v3_and_evaluate(ground_truth_matings)

    def test_fp_noise_0(self):
        fp_matings = [
            ("P_0_E_3","P_7_E_2"),
            ("P_5_E_2","P_4_E_0"),
            ("P_7_E_1","P_9_E_1")
        ]

        self._process_v3_and_evaluate(fp_matings)

    def test_tn_noise_0(self):
        print("Expecting here to get low scores")
        tn_matings = [
            ("P_3_E_0","P_9_E_0"),
            ("P_1_E_1","P_5_E_2")
        ]

        self._process_v3_and_evaluate(tn_matings)


    def test_plot_two_edges_noiseless(self,first_plot_edge = "P_7_E_2",second_plot_edge = "P_8_E_0"):
        data_dir = "data/poc_10_pictorial_compatibility/db-1-puzzle-19-noise-0/"
        edge2extrpolated_image,edge2original_image,_,_ = load_data(data_dir)
        self._plot_two_edges(edge2extrpolated_image[first_plot_edge],edge2original_image[first_plot_edge],first_plot_edge,
                            edge2extrpolated_image[second_plot_edge],edge2original_image[second_plot_edge],second_plot_edge)






if __name__ == "__main__":
    unittest.main()