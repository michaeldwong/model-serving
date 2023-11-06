import requests
import time
from datetime import datetime
import os
import subprocess
# Specify the URL of your API
api_url = 'http://172.17.0.52:8080/predict'  # Update with your server's IP
send_times = []
for i in range(10000):


    t = str(datetime.now())
    num_requests = 50
    for _ in range(0,num_requests):
        send_times.append(t)
    # Send a POST request to the API with the image file
    if len(send_times) % 1000 == 0:
        print(send_times)

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
                            'http://172.17.0.52:8080/predict'
            ], timeout=0.75, stdout=DEVNULL, stderr=DEVNULL)
        except subprocess.CalledProcessError as e:
            print(e.output)
        except:
            pass



    # Check if the request was successful
#ab -t 5  -v 4  -n 100 -c 100 -p image_medium2.jpg -T 'application/octet-stream' -H 'Content-Type: application/octet-stream' -T 'multipart/form-data' http://172.17.0.52:8080/predict
