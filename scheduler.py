from CardScanner import scan, SCAN_DIR
import time
from datetime import datetime
import pyinsane2
from math import floor
import pytz

while True:
    now_hour = datetime.now(pytz.timezone('America/New_York')).hour
    if now_hour >= 19:
        break
    try:
        images = scan.scan_cards()
        images = [scan.bg_trim(img) for img in images]
        scan.save_ab(images)
    except:
        print("No paper loaded.")
