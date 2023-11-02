
import os
import sys
import json
from datetime import datetime


if len(sys.argv) != 2:
    print('Provide 1 arg containing the directory to the Twitter dataset. It should be the directory of the hour (e.g., /data2/mikedw/twitter-dataset/2018/04/02/00)')
    exit()
indir = sys.argv[1]

# Each value is a list of integers, each integer is a second that a request was sent. E.g., if 4 requests were sent at
# second 6, this will show up as [6, 6, 6, 6]
minute_to_request_lists = {}
for root, dirs, files in os.walk(indir): 
    for f in files:
        if not f.endswith('json'): 
            continue
        with open(os.path.join(indir, f)) as f_read:
            for line in f_read.readlines():
                data = json.loads(line)
                if 'created_at' not in data:
                    continue
                date_format = "%a %b %d %H:%M:%S %z %Y"

                # Parse the date string
                date_object = datetime.strptime(data['created_at'], date_format)
                if date_object.minute not in minute_to_request_lists:
                    minute_to_request_lists[date_object.minute] = []
                minute_to_request_lists[date_object.minute].append(date_object.second)

with open('request_trace.txt', 'w') as f:
    for m in range(0,60):
        if m not in minute_to_request_lists:
            continue
        f.write(str(minute_to_request_lists[m]).replace('[', '').replace(']', ''))
        f.write('\n')
#        print(os.path.join(indir, f))
#print(timestamps)
