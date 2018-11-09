import cv2
import numpy as np
import datetime

age_yDims = np.array([360, 410, 460])
gdr_yDims = np.array([560])
# q3_yDims = np.array([780, 820, 870])
hom_yDims = np.array([790])
x_dims = np.array([200, 420, 600])

f_x_dims = np.array([50, 305])
f_y_dims = np.array([530, 590, 650])

black =  [0, 20, 'white']
white = [180, 255, 'black']
# 131, 55, 64

white_hsv = [(0,0,180),(180, 15, 255), 'white_hsv']
green_h = 131 / 360 * 180
green_s = 55 / 100 * 255
green_v = 64 / 100 * 255
green = [(green_h-20,green_s-20,green_v-20), (green_h+20, green_s+20, green_v+20), 'green']

blue_h = 220 / 360 * 180
blue_s = 96 / 100 * 255
blue_v = 44 / 100 * 255
blue = [(blue_h-20, blue_s-20,blue_v-20), (blue_h+20, blue_s+20, blue_v+20), 'blue']

interval = 35
thresh = 7500

def age_get(dst):
    """
    Age
    """
    max_test = 0
    i_max = -1
    j_max = -1
    for i, x in enumerate(x_dims):
        for j, y in enumerate(age_yDims):
            crop = dst[y:y+interval, x:x+interval]
            if (np.sum(crop) > thresh) and (np.sum(crop) > max_test):
                max_test = np.sum(crop)
                i_max = i
                j_max = j
    if (i_max==0) & (j_max==0):
        return "Under 18"
    elif (i_max==1) & (j_max==0):
        return "18-24"
    elif (i_max==2) & (j_max==0):
        return "25-34"
    elif (i_max==0) & (j_max==1):
        return "35-44"
    elif (i_max==1) & (j_max==1):
        return "45-54"
    elif (i_max==2) & (j_max==1):
        return "55-64"
    elif (i_max==0) & (j_max==2):
        return "65+"
    else:
        # print(max_test)
        return "There was a problem."

def gdr_get(dst):
    """
    Gender
    """
    max_test = 0
    i_max = -1
    j_max = -1
    for i, x in enumerate(x_dims):
        for j, y in enumerate(gdr_yDims):
            crop = dst[y:y+interval, x:x+interval]
            if (j < 1):
                if (np.sum(crop) > thresh) and (np.sum(crop) > max_test):
                    max_test = np.sum(crop)
                    i_max = i
                    j_max = j
    if (i_max==0) & (j_max==0):
        return "Nonbinary"
    elif (i_max==1) & (j_max==0):
        return "Female"
    elif (i_max==2) & (j_max==0):
        return "Male"
    else:
        # print(max_test)
        return "There was a problem."


def hom_get(dst):
    """
    Home
    """
    max_test = 0
    i_max = -1
    j_max = -1
    for i, x in enumerate(x_dims):
        for j, y in enumerate(hom_yDims):
            crop = dst[y:y+interval, x:x+interval]
            if (j < 1):
                if (np.sum(crop) > thresh) and (np.sum(crop) > max_test):
                    max_test = np.sum(crop)
                    i_max = i
                    j_max = j
    if (i_max==0) & (j_max==0):
        return "Suburban"
    elif (i_max==1) & (j_max==0):
        return "Urban"
    elif (i_max==2) & (j_max==0):
        return "Rural"
    else:
        # print(max_test)
        return "There was a problem."

def q1_get(dst):
    """
    In 2040, the average citizen will...
    """
    max_test = 0
    i_max = -1
    j_max = -1
    for i, x in enumerate(f_x_dims):
        for j, y in enumerate(f_y_dims):
            crop = dst[y:y+interval, x:x+interval]
            if (j < 2) or ((j == 2) and (i==0)):
                if (np.sum(crop) > thresh) and (np.sum(crop) > max_test):
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
        return "There was a problem."

def q2_get(dst):
    """
    My preferred transport mode(s) in 2040 will be...
    """
    max_test = 0
    i_max = -1
    j_max = -1
    for i, x in enumerate(f_x_dims):
        for j, y in enumerate(f_y_dims):
            crop = dst[y:y+interval, x:x+interval]
            if (j < 2) or ((j == 2) and (i==0)):
                if (np.sum(crop) > thresh) and (np.sum(crop) > max_test):
                    max_test = np.sum(crop)
                    i_max = i
                    j_max = j
    if (i_max==0) & (j_max==0):
        return "AV Buses"
    elif (i_max==1) & (j_max==0):
        return "AV Cars"
    elif (i_max==2) & (j_max==0):
        return "Scooters"
    elif (i_max==0) & (j_max==1):
        return "Subways"
    elif (i_max==1) & (j_max==1):
        return "Bikes"
    elif (i_max==2) & (j_max==1):
        return "Walking"
    elif (i_max==0) & (j_max==2):
        return "Hyperloop"
    elif (i_max==1) & (j_max==2):
        return "Train"
    elif (i_max==2) & (j_max==2):
        return "Other"
    else:
        # print(max_test)
        return "There was a problem."

def image_process(path, b, side):
    """
    Process image
    """
    img = cv2.imread(path)
    if (side == 'b'):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.blur(gray,(b, b))
        # mask_black = cv2.inRange(blur, black[0], black[1])
        mask = cv2.inRange(blur, white[0], white[1])
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

def read_back(path):
    """
    Read card back.
    """
    card = image_process(path, 5, 'b')
    # cv2.imwrite('test.png', card)
    return [age_get(card), gdr_get(card), hom_get(card)]

def read_front(path):
    """
    Read card back
    """
    card = image_process(path, 5, 'f')
    cv2.imwrite('test-10.png', card)
    return [q1_get(card)]

for i in range(17):
    path = 'assets/focus_group/q'
    q = 1
    front = path + str(q) + '/' + str(i) + '-front.png'
    back = path + str(q) + '/' + str(i) + '-back.png'
    print(i, read_front(front), read_back(back))

# read_front('assets/focus_group/q1/5-front.png')
# image_process('assets/focus_group/q1/0-front.png', 2, 'f')
read_back('assets/focus_group/q2/9-back.png')
read_front('assets/focus_group/q1/10-front.png')
