from CardScanner import scan, process, dims, read
import schedule
import time
from os import listdir
import cv2
import numpy as np
# import logging

# logging.basicConfig(
#         filename='overnight-scanner.log',
#         level=logging.INFO,
#         format='%(asctime)s %(message)s'
#     )

DEVICE = scan.setup()
images = scan.scan_cards(DEVICE)
# for i, img in enumerate(images):
#     # Programmatically trim image.
#     img = process.bg_trim(img)
#     # Convert PIL image to OpenCV
#     img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2HSV)
#     # Determine question.
#     read.get_question(img)

images = [process.bg_trim(i) for i in images]
images = [cv2.cvtColor(np.array(i), cv2.COLOR_BGR2HSV) for i in images]


for i in range(0, len(images), 2):
    corners = read.get_corners(images[i])
    diff = corners['tl_s'] - corners['bl_s']
    if abs(diff) > 20:
        front = images[i + 1]
        back = images[i]
        # print("wobble")
    else:
        front = images[i]
        back = images[i + 1]
        corners = read.get_corners(back)
        diff = corners['tl_s'] - corners['bl_s']
    if diff < -20:
        print('upside down')
        front = read.rotate(front)
        question = read.get_question(corners['tl_h'])
        back = read.rotate(back)
    # cv2.imshow("back", back)
    # cv2.imshow("front", front)
# cv2.imwrite('back.jpg', back)
# cv2.imwrite('front.jpg', front)

DEVICE = scan.setup()

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
