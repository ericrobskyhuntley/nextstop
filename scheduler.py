from CardScanner import scan, process, read, SCAN_DIR, ARCHIVE_DIR
import schedule
import time
from os import listdir
import cv2
import numpy as np
from math import floor

def save_ab(image_list):
    start_no = floor(len(read.get_file_list(SCAN_DIR + "*png"))/2)
    archive_no = floor(len(read.get_file_list(ARCHIVE_DIR + "*png"))/2)
    for i in range(0, len(image_list), 2):
        print(i, i+1)
        image_list[i].save(SCAN_DIR+"{:06}-a.png".format(floor(i/2 + start_no+archive_no)))
        image_list[i+1].save(SCAN_DIR+"{:06}-b.png".format(floor(i/2 + start_no+archive_no)))

def scan_cards():
    DEVICE = scan.setup()
    if DEVICE is not None:
        try:
            images = scan.scan_cards(DEVICE)
            images = [process.bg_trim(img) for img in images]
            images = save_ab(images)
            # [image.save(SCAN_DIR + "{:06}-a.png".format(floor((i+start_no)/2)) for i, image in enumerate(images)]
            # images = [i.convert("P", colors=4) for i in images]
        except:
            print("No paper loaded.")
            # list = read.get_file_list(SCAN_DIR + "*")
            # read.read_from_disk(list)
    else:
        print("No scanners found.")

schedule.every(1).seconds.do(scan_cards)

while True:
    schedule.run_pending()
    time.sleep(1)
