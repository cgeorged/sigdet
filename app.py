# Import the necessary libraries
import os
import traceback
from PIL import Image
from flask import Flask, render_template, request, jsonify
from detector.detector import extract_images_from_pdf, train_async, detect, s_hash, load_model

# Create a Flask app
app = Flask(__name__)


# Define the home route
@app.route('/')
def hello():
    # Render the home page
    return render_template('index.html')


# Define the detect route
@app.route('/api/v1/detect', methods=['POST'])
def process_detect():
    try:
        # Initialize the list of input images
        inputImg = []

        # Get the image file from the request
        file = request.files['image']

        # Check if the file is a PDF or an image
        if file.filename.endswith('.pdf') or file.content_type == 'application/pdf':
            # Extract images from the PDF file
            inputImg = extract_images_from_pdf(file)
            print("Received pdf docs !")
        elif file.filename.endswith('.jpg') or file.filename.endswith('.jpeg'):
            # Load the image file
            img = Image.open(file)
            # Add the image to the list of input images
            inputImg.append(img)
            # Check if the image is a JPG
        else:
            return jsonify({'error': 'Only JPG images and PDF files are supported'}), 400

        # Detect signature in the input images
        result = detect(inputImg)

        # Return the results as a JSON response
        return jsonify({'images': result})
    except Exception as e:
        # Handle any exceptions that occur
        traceback.print_exc()
        error_message = str(e)
        return jsonify({'error': error_message}), 500


# Define the train route
@app.route('/api/v1/train', methods=['POST'])
def train():
    try:
        # Get the epochs and password from the request
        key = request.json['key']
        # Start training the model asynchronously
        if 1243 == s_hash(key):
            return train_async()
        else:
            return jsonify({'error': 'key is incorrect'}), 400
    except Exception as e:
        # Handle any exceptions that occur
        traceback.print_exc()
        error_message = str(e)
        return jsonify({'error': error_message}), 500


# Run the app
if __name__ == '__main__':

    load_model()

    # Get the server port from the environment variables
    server_port = os.environ.get('PORT', '8080')

    # Run the app on the specified port
    app.run(debug=False, port=server_port, host='0.0.0.0')
