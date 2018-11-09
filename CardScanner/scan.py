import pyinsane2
from PIL import Image, ImageChops
# from CardReader import cr
from math import floor
import numpy as np
import cv2

MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.15

# ECC as implemented appears to work more consistently on card fronts. Unsure if it's due to parameters or method suitability.

def align_images_orb(im1, im2):
    """
    Feature-based image alignment algorithm that finds homography using the ORB feature detector (Oriented Fast and Rotated Brief).

    Code is based on implementation found here: https://www.learnopencv.com/image-alignment-feature-based-using-opencv-c-python/
    """
    # Convert images to grayscale
    im1_gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2_gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1_gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2_gray, None)
    # Match features
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)
    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)
    # Remove not good matches
    num_good_matches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:num_good_matches]
    # Draw top matchesints
    im_matches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
    cv2.imwrite("matches.jpg", im_matches)
    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find homography
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)
    # Apply homography
    height, width, channels = im2.shape
    im1_reg = cv2.warpPerspective(im1, h, (width, height))

    return im1_reg

def align_images_ecc(im1, im2):
    """
    Image alignment algorithm using enhanced correlation coefficient method (ECC), which is proposed in: Georgios D. Evangelidis and Emmanouil Z. Psarakis. 2008. "Parametric Image Alignment Using Enhanced Correlation Coefficient Maximization." IEEE Transactions on Pattern Analysis and Machine Intelligence 30 (10): 1-8.

    Code is based on implementation found here: https://www.learnopencv.com/image-alignment-ecc-in-opencv-c-python/
    """
    # Convert images to grayscale
    im1_gray = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
    im2_gray = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)
    # Find size of image1
    sz = im1.shape
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
    (cc, warp_matrix) = cv2.findTransformECC (im1_gray,im2_gray,warp_matrix, warp_mode, criteria)
    if warp_mode == cv2.MOTION_HOMOGRAPHY :
        # Use warpPerspective for Homography
        im2_aligned = cv2.warpPerspective (im2, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    else :
        # Use warpAffine for Translation, Euclidean and Affine
        im2_aligned = cv2.warpAffine(im2, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    return im2_aligned

def bg_trim(im):
    """
    Function to programmatically crop card to edge.
    `im` is a PIL Image Object.
    """
    # This initial crop is hacky and stupid (should just be able to set device
    # options) but scanner isn't 'hearing' those settings.
    im = im.crop((420, 0, 1275, 1200))
    bg = Image.new(im.mode, im.size, im.getpixel((2, 2)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        print(bbox)
        return im.crop(bbox)
    else:
        print("There's been a problem.")

try:
    # Initiation block.
    pyinsane2.init()
    devices = pyinsane2.get_devices()
    assert(len(devices) > 0)
    device = devices[0]
    print(f'PyInsane2 initiatied using {device.name}.')

    try:
        pyinsane2.set_scanner_opt(device, 'source', ['Automatic Document Feeder(center aligned,Duplex)'])
    except pyinsane2.PyinsaneException as e:
        print('No document feeder found', e)
    # Specify color scanning
    pyinsane2.set_scanner_opt(device, 'mode', ['24bit Color[Fast]'])
    # Set scan resolution
    pyinsane2.set_scanner_opt(device, 'resolution', [200])
    # set scanner dimensions
    # pyinsane2.set_scanner_opt(device, 'tl-x', [0])
    # pyinsane2.set_scanner_opt(device, 'tl-y', [0])
    # pyinsane2.set_scanner_opt(device, 'br-x', [floor(215.88)])
    # pyinsane2.set_scanner_opt(device, 'br-y', [floor((1218 / 2795) * 3556)])
    # pyinsane2.set_scanner_opt(device, 'AutoDocumentSize', [1])
    # pyinsane2.set_scanner_opt(device, 'AutoDeskew', [1])
    # specificy scan area
    # We want full area because otherwise,
    pyinsane2.maximize_scan_area(device)

    try:
        scan_session = device.scan(multiple=True)
        print("Scanning...")
        while True:
            try:
                scan_session.scan.read()
            except EOFError:
                print(f'Scanned page {len(scan_session.images)}.')
    except StopIteration:
        print(f'Document feeder is empty. Scanned {len(scan_session.images)} pages.')
    for i in range(0, len(scan_session.images)):
        image = bg_trim(scan_session.images[i])
        image = align_images()
        if (i % 2 == 0) | (i == 0):
            image.save(f'assets/focus_group/q1/lgt_pap/{floor(i/2)}-back.png')
        else:
            # cr.read_back(image)
            image.save(f'assets/focus_group/q1/lgt_pap/{floor((i-1)/2)}-front.png')


finally:
    pyinsane2.exit()
