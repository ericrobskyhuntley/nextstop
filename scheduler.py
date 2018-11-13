from CardScanner import scanner
import schedule
import time

dev = scanner.setup()
def job(d):
    scanner.doc_load(d)

schedule.every(1).seconds.do(job, dev)

while True:
    schedule.run_pending()
    time.sleep(1)
