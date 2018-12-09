from PIL import Image, ImageChops
import numpy as np
import cv2
from . import MAX_FEATURES, GOOD_MATCH_PERCENT, FRONT_MASK_COLOR_WINDOW

def rotate(dst):
    (h, w) = dst.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, 180, 1.0)
    dst_rotated = cv2.warpAffine(dst, M, (w, h))
    return dst_rotated

def align_images_orb(im, ref):
    """
    Feature-based image alignment algorithm that finds homography using the ORB feature detector (Oriented Fast and Rotated Brief).

    Code is based on implementation found here: https://www.learnopencv.com/image-alignment-feature-based-using-opencv-c-python/
    """
    # Convert images to grayscale
    # ref = cv2.imread(ref)
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ref_gray = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints_im, descriptors_im = orb.detectAndCompute(im_gray, None)
    keypoints_ref, descriptors_ref = orb.detectAndCompute(ref_gray, None)
    # Match features
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors_im, descriptors_ref, None)
    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)
    # Remove not good matches
    num_good_matches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:num_good_matches]
    # Draw top matchesints
    im_matches = cv2.drawMatches(im, keypoints_im, ref, keypoints_ref, matches, None)
    # Extract location of good matches
    points_im = np.zeros((len(matches), 2), dtype=np.float32)
    points_ref = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points_im[i, :] = keypoints_im[match.queryIdx].pt
        points_ref[i, :] = keypoints_ref[match.trainIdx].pt

    # Find homography
    h, mask = cv2.findHomography(points_im, points_ref, cv2.RANSAC)
    # Apply homography
    height, width, channels = ref.shape
    im_align = cv2.warpPerspective(im, h, (width, height))

    return im_align

def align_images_ecc(im, ref):
    """
    Image alignment algorithm using enhanced correlation coefficient method (ECC), which is proposed in: Georgios D. Evangelidis and Emmanouil Z. Psarakis. 2008. "Parametric Image Alignment Using Enhanced Correlation Coefficient Maximization." IEEE Transactions on Pattern Analysis and Machine Intelligence 30 (10): 1-8.

    Code is based on implementation found here: https://www.learnopencv.com/image-alignment-ecc-in-opencv-c-python/
    """
    # Convert images to grayscale
    # ref = cv2.imread(r)
    im_gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    ref_gray = cv2.cvtColor(ref,cv2.COLOR_BGR2GRAY)
    # Find size of ref
    sz = ref.shape
    # Define the motion model
    warp_mode = cv2.MOTION_TRANSLATION
    # Define 2x3 or 3x3 matrices and initialize the matrix to identity
    if warp_mode == cv2.MOTION_HOMOGRAPHY :
        warp_matrix = np.eye(3, 3, dtype=np.float32)
    else :
        warp_matrix = np.eye(2, 3, dtype=np.float32)
    # Specify the number of iterations.
    number_of_iterations = 5000;
    # Specify the threshold of the increment
    # in the correlation coefficient between two iterations
    termination_eps = 1e-10;
    # Define termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)
    # Run the ECC algorithm. The results are stored in warp_matrix.
    (cc, warp_matrix) = cv2.findTransformECC (ref_gray,im_gray,warp_matrix, warp_mode, criteria)
    if warp_mode == cv2.MOTION_HOMOGRAPHY :
        # Use warpPerspective for Homography
        im_align = cv2.warpPerspective (im, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    else :
        # Use warpAffine for Translation, Euclidean and Affine
        im_align = cv2.warpAffine(im, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    return im_align

white_hsv = [(0,0,180),(180, 15, 255)]
black_hsv = [(0,0,0),(180, 255, 100)]

def mask_front(img, b, color):
    """
    Process image
    """
    col = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    blur = cv2.blur(col,(b, b))
    mask_white = cv2.inRange(blur, white_hsv[0], white_hsv[1])
    mask_color = cv2.inRange(blur, color - FRONT_MASK_COLOR_WINDOW, color + FRONT_MASK_COLOR_WINDOW)
    mask = cv2.bitwise_or(mask_color, mask_white)
    mask = cv2.bitwise_not(mask)
    return cv2.bitwise_and(blur, blur, mask=mask)
