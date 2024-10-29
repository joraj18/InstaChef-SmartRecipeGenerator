
from flask import Flask, request, jsonify
from flask_cors import CORS  
import os
from PIL import Image
import io
import numpy as np

import torch
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

from llm import llm

app = Flask(__name__)

CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = YOLO('D:/projects/mini-project/InstaChef/src/weights/best.pt') 

@app.route('/', methods=['GET'])
def home():
    return "Welcome bruhh!"

@app.route('/image', methods=['POST'])
def classify_image():
    print("Image API pinged")

    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected image'}), 400

    try:
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)

        image = Image.open(image_path)

        # Convert the PIL image to a NumPy array (OpenCV format)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Perform prediction using the YOLO model
        results = model(image)

        # Define class names (ensure these match your trained model's labels)
        class_names = [
            'banana_wb', 'banana_wob', 'blackberry', 'raspberry', 
            'lemon_wb', 'lemon_wob', 'grapes_wb', 'grapes_wob', 
            'tomato_wb', 'tomato_wob', 'apple_wb', 'apple_wob', 
            'chilli_wb', 'chilli_wob'
        ]

        # Extract the first result (assuming one image processed)
        result = results[0]

        # Extract class IDs and convert to integers
        class_ids = result.boxes.cls.cpu().numpy().astype(int)

        # Map class IDs to class names
        labels = [class_names[class_id] for class_id in class_ids]

        print(f"Predicted labels are: {labels}")

        # Use join() to convert the list to a comma-separated string and strip extra spaces
        formatted_string = ", ".join(item.strip() for item in labels)
        llm_response=llm("potato, tomato, chili")
        print(llm_response)


        response = {
            'text': f"{llm_response}"
        }
        return jsonify(response), 200

    except Exception as e:
        print({'error': str(e)})
        return jsonify({'error': str(e)}), 500


@app.route('/llmcheck', methods=['GET'])
def llmcheck():
    llm_response = llm("potato, tomato, chili")
    return jsonify({'response': llm_response})


if __name__ == '__main__':
    app.run(debug=True, port=5000)

