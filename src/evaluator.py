import numpy as np



def least_square_rigid_motion_svd(points:np.array,points_weights:np.array,ground_truth:np.array):
    '''
        implementation of https://vincentqin.gitee.io/blogresource-3/slam-common-issues-ICP/svd_rot.pdf
    '''
    assert points.shape == ground_truth.shape
    assert points.shape[0] == points_weights.shape[0]

    points_centroid = np.average(points,axis=0,weights=points_weights)
    ground_truth_centroid = np.average(ground_truth,axis=0,weights=points_weights)

    centered_points = points-points_centroid
    centered_ground_truth = ground_truth - ground_truth_centroid

    X = centered_points.T # 2xN
    Y = centered_ground_truth.T # 2xN
    W = np.diag(points_weights)
    S = X@W@Y.T

    U,sigma, V = np.linalg.svd(S)

    diag_d = np.identity(X.shape[0])
    diag_d[-1,-1] = np.linalg.det(V@U.T)

    R = V@diag_d@U.T
    t = ground_truth_centroid - R@points_centroid.T

    return R,t
