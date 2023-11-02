
import sys
import time
import subprocess

if len(sys.argv) != 2:
    print('Input should be request trace')
    exit()
#request = "ab -t 5 -g responses.txt -v 4  -n 100 -c 100 -p image_medium2.jpg -T 'application/octet-stream' -H 'Content-Type: application/octet-stream' -T 'multipart/form-data' http://172.17.0.52:6060/predictions/yolov8n "

request_quantity_list = []
with open(sys.argv[1]) as f:
    for line in f.readlines():
        requests = line.strip().replace(' ', '').split(',')
        for m in range(0,60):
            request_quantity_list.append(requests.count(str(m)) )

base_time = time.time()
for num_requests in request_quantity_list:
    current = time.time()
    if current - base_time >= 1:
        base_time = current
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
                            'http://172.17.0.52:6060/predictions/yolov8n'
            ], timeout=0.75)
        except:
            pass

#    subprocess.

