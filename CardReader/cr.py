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

# Pantone P 14-8 C
q1 = [(38, 90, 98), 'q1']
# Pantone P 10-8 C
q2 = [(43, 93, 99), 'q2']
# Pantone P 56-8 C
q3 = [(347, 92, 66), 'q3']
# Pantone P 62-16 C
q4 = [(341, 86, 83), 'q4']
# Pantone P 92-7 C
q5 = [(286, 63, 47), 'q5']
# Pantone P 88-8 C
q6 = [(302, 72, 57), 'q6']
# Pantone P 111-16 C
q7 = [(203, 100, 41), 'q7']
# Pantone P 102-8 C
q8 = [(216, 81, 62), 'q8']
# Pantone P 131-16 C
q9 = [(169, 100, 47), 'q9']
# Pantone P 151-8 C
q10 = [(117, 60, 71), 'q10']

card_colors = [q1, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]

def question_test(img):
    crop = img[y:y+interval, x:x+interval]
    for i, (low, high, q) in enumerate(card_colors):
        max_test = 0
        mask_color = cv2.inRange(blur, low, high)
        crop_mask = cv2.bitwise_and(blur, blur, mask=mask_color)
        sum = np.sum(crop_mask)
        if sum > max_test:
            max_test = sum
            max_idx = i
    return card_colors[max_idx]

def front_mask(img):
    q = question_test(img)
    mask = cv2.inRange(img, q[0], q[1])
    mask_inv = cv2.bitwise_not(mask)
    masked = cv2.bitwise_and(blur, blur, mask=mask_inv)
    return masked


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

def front_process(path, b):
    """
    """
    img = cv2.imread(path)
    # Convert to HSV color space.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    blur = cv2.blur(hsv,(b, b))
    # Determine which color to mask and mask it.
    mask = front_mask(blur)
    return cv2.bitwise_and(blur, blur, mask=mask)

def back_process(path, b):
    """
    """
    img = cv2.imread(path)
    # Convert to grayscale color space.
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
    card = back_process(path, 5)
    return [q1_get(card), q2_get(card), q3_get(card), q4_get(card)]
