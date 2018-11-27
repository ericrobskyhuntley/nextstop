from CardScanner import scan, process
import schedule
import time
from os import listdir

def scan_cards():
    dev = scan.setup()
    if dev is not None:
        scan.doc_load(dev)
    else:
        print("cannot scan")

schedule.every(1).seconds.do(scan_cards)

while True:
    schedule.run_pending()
    time.sleep(1)
