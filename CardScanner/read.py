import cv2
import numpy as np
import datetime
import glob
from math import floor

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

COLOR_WINDOW = 10


QUESTION_HUES = [
    # My preferred transport mode(s) in 2020 will be...
    (4, np.array([1, 232, 190])),
    # In 2040, the average person will...
    (5, np.array([0, 255, 62])),
    # Responsibility for autonomous vehicle accidents belongs to...
    (6, np.array([27, 176, 242])),
    # In 2040, commuting will take...
    (7, np.array([59, 157, 152])),
    # In 2040, everyone will have access to...
    (8, np.array([107, 255, 42])),
    # The future of mobility will make the world
    (9, np.array([142, 190,65])),
    # In the future, my transportation costs will...
    (10, np.array([88, 255, 62])),
    # Future mobility options will have the greatest imapact on...
    (12, np.array([174, 156, 208])),
    # In 2040...
    (13, np.array([101, 203, 121])),
    # Travel in the future will be more dangerous for...
    (14, np.array([13, 250, 243])),
]

def get_corners(dst):
    from_corner = 25
    box_size = 10
    hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
    d = dict()
    d['height'], d['width'] = dst.shape[:2]
    tl_hsv = hsv[from_corner:from_corner+box_size, from_corner:from_corner+box_size]
    tl_hsv = np.median(tl_hsv, axis=0)
    tl_hsv = np.median(tl_hsv, axis=0)
    d['tl_hsv'] = tl_hsv
    tr_hsv = hsv[from_corner:from_corner+box_size, d['width']-from_corner-box_size:d['width']-from_corner]
    tr_hsv = np.median(tr_hsv, axis=0)
    tr_hsv = np.median(tr_hsv, axis=0)
    d['tr_hsv'] = tr_hsv
    bl_hsv = hsv[d['height']-from_corner-box_size:d['height']-from_corner, from_corner:from_corner + box_size]
    bl_hsv = np.median(bl_hsv, axis=0)
    bl_hsv = np.median(bl_hsv, axis=0)
    d['bl_hsv'] = bl_hsv
    br_hsv = hsv[d['height']-from_corner-box_size:d['height']-from_corner, d['width']-from_corner-box_size:d['width']-from_corner]
    br_hsv = np.median(br_hsv, axis=0)
    br_hsv = np.median(br_hsv, axis=0)
    d['br_hsv'] = br_hsv
    med = np.median(np.array([tl_hsv, tr_hsv, bl_hsv, br_hsv]), axis=0)
    d['med'] = med
    # # .mean().astype(int)
    # # .mean().astype(int)
    # print(d)
    return d

def get_question(hsv):
    # print(hsv)
    possible_values = np.array([hsv['med'], hsv['tl_hsv'], hsv['tr_hsv'], hsv['bl_hsv'], hsv['br_hsv']])
    q = None
    for value in possible_values:
        for question in QUESTION_HUES:
            # q_hsv = q_hsv[1]
            lower_bound = question[1] - COLOR_WINDOW
            upper_bound = question[1] + COLOR_WINDOW
            # print(lower_bound, value, upper_bound)
            # print(lower_bound, hsv, upper_bound)
            if np.all(value > lower_bound) and np.all(value < upper_bound):
                q = question
    return q


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


# def read_front(img):
#     front_proc = image_process(img, 5, 'f')
#     # num = card.split('-')[0]
#     resp = q3_get(front_proc)
#     return [resp]
#
# def read_back(img):
#     back_proc = image_process(img, 1, 'b')
#     cv2.imwrite('back-test.png', back_proc)
#     # num = card.split('-')[0]
#     age = age_get(back_proc)
#     gdr = gdr_get(back_proc)
#     home = hom_get(back_proc)
#     return [age, gdr, home]
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
