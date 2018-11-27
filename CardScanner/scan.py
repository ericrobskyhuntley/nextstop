import pyinsane2
# import psycopg2
import os
import sys
import django
import cv2
import numpy as np
from math import floor
from . import cr, process

sys.path.append('/home/cddl/Desktop/nextstop/nextstop')
os.environ["DJANGO_SETTINGS_MODULE"] = 'nextstop.settings'
django.setup()
from survey.models import Response, Question, Answer, Survey

def setup():
    pyinsane2.init()
    devices = pyinsane2.get_devices()
    try:
        assert(len(devices) > 0)
        device = devices[0]
        # Specify color scanning
        pyinsane2.set_scanner_opt(device, 'mode', ['24bit Color[Fast]'])
        # Set scan resolution
        pyinsane2.set_scanner_opt(device, 'resolution', [200])
        pyinsane2.set_scanner_opt(device, 'MultifeedDetection', [1])
        # set scanner dimensions
        # pyinsane2.set_scanner_opt(devicfe, 'tl-x', [0])
        # pyinsane2.set_scanner_opt(device, 'tl-y', [0])
        # pyinsane2.set_scanner_opt(device, 'br-x', [floor(215.88)])
        # pyinsane2.set_scanner_opt(device, 'br-y', [floor((1218 / 2795) * 3556)])
        # Set scan area
        pyinsane2.maximize_scan_area(device)
        try:
            pyinsane2.set_scanner_opt(device, 'source', ['Automatic Document Feeder(center aligned,Duplex)'])
        except pyinsane2.PyinsaneException as e:
            print('No document feeder found', e)
        print(f'PyInsane2 initiatied using {device.name}.')
        return device
    except AssertionError:
        print("no scanners found")
        pyinsane2.exit()

def doc_load(device):
    front = None
    back = None
    try:
        scan_session = device.scan(multiple=True)
        print("Scanning ...")
        while True:
            try:
                scan_session.scan.read()
            except EOFError:
                print("Got page %d" % (len(scan_session.images)))
                for i in range(0, len(scan_session.images)):
                    image = scan_session.images[i]
                    # Programmatically trim image.
                    image = process.bg_trim(image)
                    # Convert PIL image to OpenCV
                    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                    if (i % 2 == 0) | (i == 0):
                        align_image = process.align_images_orb(image, 'nextstop/static/templates/q3_back.jpg')
                        back = cr.read_back(image)
                        cv2.imwrite(f'{floor(i/2)}-back.png', image)
                        # image.save()
                    else:
                        align_image = process.align_images_orb(image, 'nextstop/static/templates/q3_front.jpg')
                        front = cr.read_front(image)
                        cv2.imwrite(f'{floor((i-1)/2)}-front.png', image)
    except StopIteration:
        if (front is not None and back is not None):
            print(front, back)
        print("C'mon!")
        pyinsane2.exit()


# r = Response(q='', a='', gender='', free_q=2, survey=5)
