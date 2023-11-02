

import time
import subprocess
request = "ab -t 5 -g responses.txt -v 4  -n 100 -c 100 -p image_medium2.jpg -T 'application/octet-stream' -H 'Content-Type: application/octet-stream' -T 'multipart/form-data' http://172.17.0.52:6060/predictions/yolov8n "

base_time = time.time()
print(base_time)
while True:
    current = time.time()
    print(current)
    if current - base_time >= 1:
        print('\t!!!!!second has passed!!!!')
        base_time = current
    else:
        print('\tNot 1 second yet')
    try:
        subprocess.run(['ab', 
                        '-t',   
                        '5', 
                        '-n', 
                        '5', 
                        '-c', 
                        '5', 
                        '-p', 
                        'image_medium2.jpg', 
                        '-T', 
                        '\'application/octet-stream\'', 
                        '-H', 
                        '\'Content-Type: application/octet-stream\'', 
                        '-T', 
                        '\'multipart/form-data\'',
                        'http://172.17.0.52:6060/predictions/yolov8n'
        ], timeout=0.5)
    except:
        pass

#    subprocess.

