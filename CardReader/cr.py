import cv2
import numpy as np
import datetime

q1_yDims = np.array([440, 490, 540])
q2_yDims = np.array([600, 650, 700])
q3_yDims = np.array([780, 820, 870])
q4_yDims = np.array([950, 1000, 1050, 1080])
x_dims = np.array([170, 390, 570])

white =  [0, 20, 'white']
black = [140, 255, 'black']

interval = 35

def q1_get(dst):
    """
    """
    max_test = 0
    for i, x in enumerate(x_dims):
        for j, y in enumerate(q1_yDims):
            crop = dst[y:y+interval, x:x+interval]
            if np.sum(crop) > max_test:
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
        return "There was a problem."

def q2_get(dst):
    """
    """
    max_test = 0
    for i, x in enumerate(x_dims):
        for j, y in enumerate(q2_yDims):
            crop = dst[y:y+interval, x:x+interval]
            if (i < 1):
                if np.sum(crop) > max_test:
                    max_test = np.sum(crop)
                    i_max = i
                    j_max = j
    if (i_max==0) & (j_max==0):
        return "Nonconforming"
    elif (i_max==0) & (j_max==1):
        return "Female"
    elif (i_max==0) & (j_max==2):
        return "Male"
    else:
        return "There was a problem."

def q3_get(dst):
    """
    """
    max_test = 0
    for i, x in enumerate(x_dims):
        for j, y in enumerate(q3_yDims):
            crop = dst[y:y+interval, x:x+interval]
            if (i < 2):
                if np.sum(crop) > max_test:
                    max_test = np.sum(crop)
                    i_max = i
                    j_max = j
    if (i_max==0) & (j_max==0):
        return "Car"
    elif (i_max==1) & (j_max==0):
        return "Bike/Scooter"
    elif (i_max==0) & (j_max==1):
        return "Bus"
    elif (i_max==1) & (j_max==1):
        return "Walking"
    elif (i_max==0) & (j_max==2):
        return "Train/Rail"
    elif (i_max==1) & (j_max==2):
        return "Rideshare/Taxi"
    else:
        return "There was a problem."

def q4_get(dst):
    """
    """
    max_test = 0
    for i, x in enumerate(x_dims):
        for j, y in enumerate(q4_yDims):
            crop = dst[y:y+interval, x:x+interval]
            if (i < 2):
                if (np.sum(crop) > max_test) and not ( (i > 0) & (j > 2) ):
                    max_test = np.sum(crop)
                    i_max = i
                    j_max = j
    if (i_max==0) & (j_max==0):
        return "NYC"
    elif (i_max==1) & (j_max==0):
        return"Greater NY Metro"
    elif (i_max==0) & (j_max==1):
        return "US South"
    elif (i_max==1) & (j_max==1):
        return "US Northeast"
    elif (i_max==0) & (j_max==2):
        return "US West"
    elif (i_max==1) & (j_max==2):
        return "US Midwest"
    elif (i_max==0) & (j_max==3):
        return "International"
    else:
        return "There was a problem"

def image_process(path, b):
    """
    """
    img = cv2.imread(path)
    gs = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gs,(b, b))
    mask_black = cv2.inRange(blur, black[0], black[1])
    mask_white = cv2.inRange(blur, white[0], white[1])
    mask_inv = cv2.bitwise_or(mask_black, mask_white)
    mask = cv2.bitwise_not(mask_inv)
    return cv2.bitwise_and(blur, blur, mask=mask)


def read_back(path):
    """
    """
    card = image_process(path, 5)
    return [q1_get(card), q2_get(card), q3_get(card), q4_get(card)]
