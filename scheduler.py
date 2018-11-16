from CardScanner import scanner
from CardReader import cr
import schedule
import time
from os import listdir

def scan():
    dev = scanner.setup()
    scanner.scan_test(dev)

schedule.every(1).seconds.do(scan)

while True:
    schedule.run_pending()
    time.sleep(1)
