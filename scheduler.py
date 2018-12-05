from CardScanner import scan, process, dims, read
import schedule
import time
from os import listdir
import cv2
import numpy as np
from math import floor

DEVICE = scan.setup()
images = scan.scan_cards(DEVICE)
images = [process.bg_trim(i) for i in images]
images = [cv2.cvtColor(np.array(i), cv2.COLOR_BGR2RGB) for i in images]
# images_hsv = [cv2.cvtColor(np.array(i), cv2.COLOR_BGR2HSV) for i in images]

for i in range(0, len(images), 2):
    # card_no = floor(i/2) + 67
    print(card_no)
    corners = read.get_corners(images[i])
    diff = corners['tl_hsv'][1] - corners['bl_hsv'][1]
    if abs(diff) > 20:
        print("front forward")
        front = images[i + 1]
        back = images[i]
        # print("wobble")
    else:
        print("back forward")
        front = images[i]
        back = images[i + 1]
    corners = read.get_corners(back)
    diff = corners['tl_hsv'][1] - corners['bl_hsv'][1]
    # rotate if necessary
    if diff < -20:
        print('upside down')
        front = process.rotate(front)
        back = process.rotate(back)
    # blur = cv2.blur(front,(3, 3))
    corners = read.get_corners(front)
    question = read.get_question(corners)
    print(question)
    if question is not None:
        ref_front = cv2.imread('nextstop/static/templates/11_28_{:02}_front.jpg'.format(question[0]))
        # ref_back = cv2.imread('nextstop/static/templates/11_28_{:02}_back.jpg'.format(question[0]))
        aligned_front = process.align_images_orb(front, ref_front)
        # aligned_back = process.align_images_orb(back, ref_back)
        # cv2.imwrite('scans/{:02}_front.jpg'.format(card_no), aligned_front)
        # cv2.imwrite('scans/{:02}_back.jpg'.format(card_no), back)
    # cv2.imwrite('nextstop/static/templates/empirical_fg/{:02}_back.jpg'.format(card_no), aligned_back)
    # Mask and blur
    masked = process.mask_front(aligned_front, 2,  question[1])
    answers = dims.get_answers(masked, question[0])
    print(answers)

def scan_cards():
    if DEVICE is not None:
        try:
            images = scan.scan_cards(DEVICE)
        except:
            print("No paper loaded.")
        # for i, img in enumerate(images):
        #     image = images[i]
        #     # Programmatically trim image.
        #     image = process.bg_trim(image)
        #     # Convert PIL image to OpenCV
        #     image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        #     q = read.detect_question(image)
        #     align_image = process.align_images_orb(
        #         image,
        #         'nextstop/static/templates/q3_back.jpg'
        #     )
        #     answers = read.get_answers(align_image, q)
        #     read.update_database(answers, q)
    else:
        print("cannot scan")

schedule.every(1).seconds.do(scan_cards)

while True:
    schedule.run_pending()
    time.sleep(1)
