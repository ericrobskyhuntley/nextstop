from CardScanner import scan, read, SCAN_DIR, MUSEUM_DAY_IN_SECONDS
import time
from datetime import datetime
import pyinsane2
from math import floor
import resource
import objgraph
import pytz

while True:
    print('Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    objgraph.show_most_common_types()
    try:
        images = scan.scan_cards()
        images = [scan.bg_trim(img) for img in images]
        scan.save_ab(images)
    except:
        print("No paper loaded.")
    now_hour = datetime.now(pytz.timezone('America/New_York')).hour
    if now_hour >= 22 :
        list = read.get_file_list(SCAN_DIR + '*.png')
        read.read_from_disk(list)
        break
