from CardScanner import scan, read, SCAN_DIR, MUSEUM_DAY_IN_SECONDS
import time
from math import floor
import pyinsane2
import resource
import objgraph
start = time.time()
# pyinsane2.init()

while True:
    print('Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    objgraph.show_most_common_types()
    try:
        images = scan.scan_cards()
        images = [scan.bg_trim(img) for img in images]
        scan.save_ab(images)
    except:
        print("No paper loaded.")
    if time.time() > start + MUSEUM_DAY_IN_SECONDS :
        list = read.get_file_list(SCAN_DIR + '*.png')
        read.read_from_disk(list)
        break
