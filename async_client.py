import aiohttp
import asyncio

# Specify the URL of your API

api_url = 'http://172.17.0.52:5000/predict'  # Update with your server's IP

async def send_inference_request(image_path):
    async with aiohttp.ClientSession() as session:
        # Create a dictionary with the image file 
        form = aiohttp.FormData()
        form.add_field('image', open(image_path, 'rb'), filename='image_small.jpg')
        try:
            async with session.post(api_url, data=form) as response:
                if response.status == 200:
                    result = await response.json()
                    # Process the result as needed
                    print(result)
                else:
                    print(f"Request failed with status code: {response.status}")
        except Exception as e:
            print(f"Error: {str(e)}")

async def main():
#    while True:
    # Specify the path to the image you want to send for inference
    image_path = 'image_small.jpg'
    await send_inference_request(image_path)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

