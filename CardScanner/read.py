import cv2
import numpy as np
import datetime
import glob

age_yDims = np.array([382, 432, 482])
gdr_yDims = np.array([563])
# q3_yDims = np.array([780, 820, 870])
hom_yDims = np.array([805])
x_dims = np.array([215, 433, 615])

f_x_dims = np.array([50, 305])
f_y_dims = np.array([530, 590, 650])

black =  [0, 120]
white = [190, 255]

white_hsv = [(0,0,180),(180, 15, 255)]
black_hsv = [(0,0,0),(180, 255, 100)]
# green_h = 131 / 360 * 180
# green_s = 55 / 100 * 255
# green_v = 64 / 100 * 255
# green = [(green_h-20,green_s-20,green_v-20), (green_h+20, green_s+20, green_v+20)]

# blue_h = 220 / 360 * 180
# blue_s = 96 / 100 * 255
# blue_v = 44 / 100 * 255
# blue = [(blue_h-20, blue_s-20,blue_v-20), (blue_h+20, blue_s+20, blue_v+20)]

INTERVAL = 25
IMG_PATH = ''
PIXEL_THRESHOLD = 12500
FRONT_BLUR = 3
BACK_BLUR = 1

HUE_WINDOW = 5

QUESTION_HUES = [
    (4, np.array([343, 86, 83])),
    (5, np.array([338, 100, 49])),
    (6, np.array([52, 84, 87])),
    (7, np.array([118, 60, 72])),
    (8, np.array([203, 100, 42])),
    (9, np.array([287, 64, 48])),
    (10, np.array([170, 100, 48])),
    (12, np.array([332, 54, 86])),
    (13, np.array([208, 70, 67])),
    (14, np.array([15, 83, 95])),
]

def get_corners(dst):
    from_corner = 10
    d = dict()
    d['height'], d['width'] = dst.shape[:2]
    d['tl_h'], d['tl_s'], d['tl_v'] = dst[from_corner, from_corner].astype(int)
    d['bl_h'], d['bl_s'], d['bl_v'] = dst[d['height'] - from_corner, from_corner].astype(int)
    return d

def get_question(h):
    q = None
    for q_h in QUESTION_HUES:
        if q_h[1] - HUE_WINDOW < h < q_h[1] + HUE_WINDOWs:
            q = q_h[0]

def rotate(dst):
    (h, w) = dst.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, 180, 1.0)
    dst_rotated = cv2.warpAffine(dst, M, (w, h))
    return dst_rotated

# def age_get(dst):
#     """
#     Age
#     """
#     max_test = 0
#     i_max = -1
#     j_max = -1
#     for i, x in enumerate(x_dims):
#         for j, y in enumerate(age_yDims):
#             crop = dst[y:y+INTERVAL, x:x+INTERVAL]
#             if (np.sum(crop) > PIXEL_THRESHOLD) and (np.sum(crop) > max_test):
#                 max_test = np.sum(crop)
#                 i_max = i
#                 j_max = j
#     if (i_max==0) & (j_max==0):
#         return "under-18"
#     elif (i_max==1) & (j_max==0):
#         return "18-24"
#     elif (i_max==2) & (j_max==0):
#         return "25-34"
#     elif (i_max==0) & (j_max==1):
#         return "36-44"
#     elif (i_max==1) & (j_max==1):
#         return "45-54"
#     elif (i_max==2) & (j_max==1):
#         return "55-64"
#     elif (i_max==0) & (j_max==2):
#         return "65+"
#     else:
#         # print(max_test)
#         return ""
#
# def gdr_get(dst):
#     """
#     Gender
#     """
#     max_test = 0
#     i_max = -1
#     j_max = -1
#     for i, x in enumerate(x_dims):
#         for j, y in enumerate(gdr_yDims):
#             crop = dst[y:y+INTERVAL, x:x+INTERVAL]
#             if (j < 1):
#                 if (np.sum(crop) > PIXEL_THRESHOLD) and (np.sum(crop) > max_test):
#                     max_test = np.sum(crop)
#                     i_max = i
#                     j_max = j
#     if (i_max==0) & (j_max==0):
#         return "nonbinary"
#     elif (i_max==1) & (j_max==0):
#         return "female"
#     elif (i_max==2) & (j_max==0):
#         return "male"
#     else:
#         # print(max_test)
#         return ""
#
#
# def hom_get(dst):
#     """
#     Home
#     """
#     max_test = 0
#     i_max = -1
#     j_max = -1
#     for i, x in enumerate(x_dims):
#         for j, y in enumerate(hom_yDims):
#             crop = dst[y:y+INTERVAL, x:x+INTERVAL]
#             if (j < 1):
#                 if (np.sum(crop) > PIXEL_THRESHOLD) and (np.sum(crop) > max_test):
#                     max_test = np.sum(crop)
#                     i_max = i
#                     j_max = j
#     if (i_max==0) & (j_max==0):
#         return "suburban"
#     elif (i_max==1) & (j_max==0):
#         return "urban"
#     elif (i_max==2) & (j_max==0):
#         return "rural"
#     else:
#         # print(max_test)
#         return ""

def q3_get(dst):
    """
    In 2040, the average citizen will...
    """
    max_test = 0
    i_max = -1
    j_max = -1
    for i, x in enumerate(f_x_dims):
        for j, y in enumerate(f_y_dims):
            crop = dst[y:y+INTERVAL, x:x+INTERVAL]
            if (j < 2) or ((j == 2) and (i==0)):
                if (np.sum(crop) > PIXEL_THRESHOLD) and (np.sum(crop) > max_test):
                    max_test = np.sum(crop)
                    i_max = i
                    j_max = j
    if (i_max==0) & (j_max==0):
        return "Own a car"
    elif (i_max==1) & (j_max==0):
        return "Lease a car"
    elif (i_max==0) & (j_max==1):
        return "Own an AV"
    elif (i_max==1) & (j_max==1):
        return "Lease an AV"
    elif (i_max==0) & (j_max==2):
        return "Have no car"
    else:
        # print(max_test)
        return ""

# def q2_get(dst):
#     """
#     My preferred transport mode(s) in 2040 will be...
#     """
#     max_test = 0
#     i_max = -1
#     j_max = -1
#     for i, x in enumerate(f_x_dims):
#         for j, y in enumerate(f_y_dims):
#             crop = dst[y:y+INTERVAL, x:x+INTERVAL]
#             if (j < 2) or ((j == 2) and (i==0)):
#                 if (np.sum(crop) > PIXEL_THRESHOLD) and (np.sum(crop) > max_test):
#                     max_test = np.sum(crop)
#                     i_max = i
#                     j_max = j
#     if (i_max==0) & (j_max==0):
#         return "AV Buses"
#     elif (i_max==1) & (j_max==0):
#         return "AV Cars"
#     elif (i_max==2) & (j_max==0):
#         return "Scooters"
#     elif (i_max==0) & (j_max==1):
#         return "Subways"
#     elif (i_max==1) & (j_max==1):
#         return "Bikes"
#     elif (i_max==2) & (j_max==1):
#         return "Walking"
#     elif (i_max==0) & (j_max==2):
#         return "Hyperloop"
#     elif (i_max==1) & (j_max==2):
#         return "Train"
#     elif (i_max==2) & (j_max==2):
#         return "Other"
#     else:
#         # print(max_test)
#         return ""

def image_process(img, b, side):
    """
    Process image
    """
    # img = cv2.imread(path)
    if (side == 'b'):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        blur = cv2.blur(gray,(b, b))
        mask_white = cv2.inRange(blur, white_hsv[0], white_hsv[1])
        mask_black = cv2.inRange(blur, black_hsv[0], black_hsv[1])
        mask = cv2.bitwise_or(mask_white, mask_black)
        # mask_inv = cv2.bitwise_or(mask_black, mask_white)
    elif (side == 'f'):
        col = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        blur = cv2.blur(col,(b, b))
        mask_white = cv2.inRange(blur, white_hsv[0], white_hsv[1])
        mask_color = cv2.inRange(blur, green[0], green[1])
        mask = cv2.bitwise_or(mask_color, mask_white)
    else:
        print("Specify front or back.")
    mask = cv2.bitwise_not(mask)
    # cv2.imwrite('test.png', mask)
    return cv2.bitwise_and(blur, blur, mask=mask)


def read_front(img):
    front_proc = image_process(img, 5, 'f')
    # num = card.split('-')[0]
    resp = q3_get(front_proc)
    return [resp]

def read_back(img):
    back_proc = image_process(img, 1, 'b')
    cv2.imwrite('back-test.png', back_proc)
    # num = card.split('-')[0]
    age = age_get(back_proc)
    gdr = gdr_get(back_proc)
    home = hom_get(back_proc)
    return [age, gdr, home]
#
# def read_cards(path):
#     """
#     Read card
#     """
#     cards = glob.glob1(path,'*.png')
#     # print(cards)
#     for i, card in enumerate(sorted(cards)):
#         if 'back' in card:
#             front_card = card.replace('back', 'front')
#             # Process card sides.
#             back_proc = image_process(path + card, BACK_BLUR, 'b')
#             front_proc = image_process(path + front_card, FRONT_BLUR, 'f')
#             # num = card.split('-')[0]
#             age = age_get(back_proc)
#             gdr = gdr_get(back_proc)
#             home = hom_get(back_proc)
#             resp = q1_get(front_proc)
#             print([resp, age, gdr, home])
