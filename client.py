import requests

# Specify the URL of your API
api_url = 'http://172.17.0.52:5000/predict'  # Update with your server's IP

for i in range(10000):

    # Create a dictionary with the image file
    files = {'image': ('image_small.jpg', open('image_small.jpg', 'rb'))}

    # Send a POST request to the API with the image file
    response = requests.post(api_url, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        # Process the result as needed
        print(result)
    else:
        print(f"Request failed with status code: {response.status_code}")
