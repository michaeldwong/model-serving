import requests
import time
from datetime import datetime
# Specify the URL of your API
api_url = 'http://172.17.0.52:8080/predict'  # Update with your server's IP
send_times = []
for i in range(10000):

    # Create a dictionary with the image file
    files = {'image': ('image_medium2.jpg', open('image_medium2.jpg', 'rb'))}

    send_times.append(str(datetime.now())) 
    # Send a POST request to the API with the image file
    response = requests.post(api_url, files=files)
    if len(send_times) % 50 == 0:
        print(send_times)

#    time.sleep(1)
    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        # Process the result as needed
#        print(result)
    else:
        print(f"Request failed with status code: {response.status_code}")
