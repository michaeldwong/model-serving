import torch
import torchvision
from PIL import Image
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the model and set it to evaluation mode
model = torchvision.models.detection.retinanet_resnet50_fpn(pretrained=True)
model.eval()

# Define the transformation
transform = torchvision.transforms.Compose([
    torchvision.transforms.Resize((224, 224)),
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

@app.route('/predict', methods=['POST'])
def predict():
    print('Predict called')
    print(request)
    print(request.content_length)

    if 'image' not in request.files:
        print('NO IMAGE PROVIDED')
        return jsonify({'error': 'No image provided'}), 400


    image = request.files['image']
    print('image ', image)
#    print('Received image')
    pil_image = Image.open(image)
    pil_image = transform(pil_image).unsqueeze(0)
#    print('Converted')
    with torch.no_grad():
        output = model(pil_image)
#    print(output)
    # Process the output as needed
    # You can return the output in a suitable format (e.g., JSON)
    # Example: result = process_output(output)
    output = 'meh'
    return jsonify({'result': output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
