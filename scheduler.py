from CardScanner import scan, process, read
import schedule
import time
from os import listdir
import cv2
import numpy as np
from math import floor

from os import listdir
import glob

front_list = glob.glob("scans/*front*")
front_list = sorted(front_list, key=str.lower)

for front_file in front_list:
    print(front_file)
    front = cv2.imread(front_file)
    corners = read.get_corners(front)
    question = read.get_question(corners)
    if question is not None:
        print(question[0])
        masked = process.mask_front(front, 2,  question[1])
        answers = read.get_answers(masked, question[0])
        print(answers)

from PIL import Image, ImageChops
DEVICE = scan.setup()
images = scan.scan_cards(DEVICE)

cv2.imwrite('test.png', image)

images[0].model
images[0].size

def bg_trim(im):
    """
    Function to programmatically crop card to edge.
    `im` is a PIL Image Object.
    """
    # This initial crop is hacky and stupid (should just be able to set device
    # options) but scanner isn't 'hearing' those settings.
    # im = im.crop((420, 0, 1275, 1200))
    from_corner = 25
    box_size = 10
    image = np.array(images[0])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    tl_hsv = hsv[from_corner:from_corner+box_size, from_corner:from_corner+box_size]
    tl_hsv = np.median(tl_hsv, axis=0)
    tl_hsv = np.median(tl_hsv, axis=0)
    # color = tuple(map(int, tl_hsv))
    white_hsv = [(0,0,180),(180, 15, 255)]
    mask_white = cv2.inRange(hsv, white_hsv[0], white_hsv[1])
    mask_color = cv2.inRange(hsv, tl_hsv - 15, tl_hsv + 15)
    mask = cv2.bitwise_or(mask_color, mask_white)
    mask = cv2.bitwise_not(mask)
    masked = cv2.bitwise_and(hsv, hsv, mask=mask)
    cv2.imwrite('test_masked.jpg', masked)
    # bg = Image.new('HSV', images[0].size, color)
    # diff = ImageChops.difference(im, bg)
    # diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = masked.getbbox()
    if bbox:
        return im.crop(bbox)

image_crop = bg_trim(images[0])

images = [process.bg_trim(i) for i in images]
images = [cv2.cvtColor(np.array(i), cv2.COLOR_BGR2RGB) for i in images]

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
