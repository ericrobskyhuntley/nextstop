from CardScanner import scan, read, MUSEUM_DAY_IN_SECONDS
import time
from math import floor

while True:
    DEVICE = scan.setup()
    if DEVICE is not None:
        try:
            images = scan.scan_cards(DEVICE)
            images = [scan.bg_trim(img) for img in images]
            images = scan.save_ab(images)
        except:
            print("No paper loaded.")
    else:
        print("No scanners found.")
    if time.time() > start + MUSEUM_DAY_IN_SECONDS :
        list = read.get_file_list(SCAN_DIR + '*.png')
        read.read_from_disk(list)
        break
