import pyinsane2
import logging
from math import floor
import cv2

pyinsane2.init()
devices = pyinsane2.get_devices()

def setup():
    pyinsane2.init()
    devices = pyinsane2.get_devices()
    assert(len(devices) > 0)
    device = devices[0]
    # Specify color scanning
    pyinsane2.set_scanner_opt(device, 'mode', ['24bit Color[Fast]'])
    # Set scan resolution
    pyinsane2.set_scanner_opt(device, 'resolution', [200])
    pyinsane2.set_scanner_opt(device, 'MultifeedDetection', [1])
    # set scanner dimensions
    # pyinsane2.set_scanner_opt(device, 'tl-x', [0])
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

# def doc_load(device):
#     try:
#         scan_session = device.scan(multiple=True)
#         print("Scanning ...")
#         while True:
#             try:
#                 scan_session.scan.read()
#             except EOFError:
#                 print("Got page %d" % (len(scan_session.images)))
#                 for i in range(0, len(scan_session.images)):
#                     image = scan_session.images[i]
#                     if (i % 2 == 0) | (i == 0):
#                         # back = read_back(cv2.imread(image))
#                         # image.save(f'{floor(i/2)}-back.png')
#                     else:
#                         # front = read_front(cv2.imread(image))
#                         # cr.read_back(image)
#                         # image.save(f'{floor((i-1)/2)}-front.png')
#     except StopIteration:
#         print("C'mon!")
#         pyinsane2.exit()


def scan_test(device):
    try:
        scan_session = device.scan(multiple=True)
        print("Scanning...")
    except StopIteration:
        print('start over!')
        pyinsane2.exit()
