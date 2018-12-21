from CardScanner import read, SERVER_RAW
import os
from datetime import datetime, timedelta
import pytz

# Retrieve file list
file_list = read.get_file_list(SERVER_RAW + '*.png')
# Filter file list to those files modifed in the last day
tz = pytz.timezone('America/New_York')
now = datetime.now(tz)
one_day = timedelta(hours=24)
last_day_list = [f for f in file_list if ((now - datetime.fromtimestamp(os.path.getmtime(f),tz) <= one_day))]
# Read, process, and save files; create JSON.
if len(last_day_list) > 0:
    read.read_from_disk(last_day_list)
