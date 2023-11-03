
import sys
import time
import subprocess
import os
from datetime import datetime

if len(sys.argv) != 2:
    print('Input should be request trace')
    exit()
#request = "ab -t 5 -g responses.txt -v 4  -n 100 -c 100 -p image_medium2.jpg -T 'application/octet-stream' -H 'Content-Type: application/octet-stream' -T 'multipart/form-data' http://172.17.0.52:8080/predictions/yolov8n "

model = 'mask-rcnn'
request_quantity_list = []
with open(sys.argv[1]) as f:
    for line in f.readlines():
        requests = line.strip().replace(' ', '').split(',')
        for m in range(0,60):
            request_quantity_list.append(requests.count(str(m)) )

base_time = time.time()
request_idx = 0
while request_idx < len(request_quantity_list):

    num_requests = request_quantity_list[request_idx]
    current = time.time()
    if current - base_time >= 1:
        base_time = current
        print('Sending ', num_requests, ' requests ... ')
        print(datetime.now())
        print()
        with open(os.devnull, 'w') as DEVNULL:
            try:
                subprocess.run(['ab', 
                                '-t',   
                                '5', 
                                '-n', 
                                str(num_requests), 
                                '-c', 
                                str(num_requests), 
                                '-p', 
                                'image_medium2.jpg', 
                                '-T', 
                                '\'application/octet-stream\'', 
                                '-H', 
                                '\'Content-Type: application/octet-stream\'', 
                                '-T', 
                                '\'multipart/form-data\'',
                                'http://172.17.0.52:8080/predictions/' + model
                ], timeout=0.75, stdout=DEVNULL, stderr=DEVNULL)
            except subprocess.CalledProcessError as e:
                print(e.output)
            except:
                pass
        request_idx += 1

#    subprocess.

