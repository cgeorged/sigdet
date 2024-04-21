
import os
import traceback
from PIL import Image
from flask import Flask, render_template, request, jsonify
from detector.detector import extract_images_from_pdf, train_async, detect

app = Flask(__name__)


@app.route('/')
def hello():

    message = "It's running!"

    return render_template('index.html',
        message=message)

@app.route('/api/v1/detect', methods=['POST'])
def process_detect():
    try:
        inputImg = []
        file = request.files['image']
        if file.filename.endswith('.pdf') or file.content_type == 'application/pdf':
            inputImg = extract_images_from_pdf(file)
            print("Received pdf docs !")
        else:
            # Load image
            img = Image.open(file)
            inputImg.append(img)

        result = detect(inputImg)
        return jsonify({'images': result})
    except Exception as e:
        traceback.print_exc()
        # Handle any exceptions that occur
        error_message = str(e)
    return jsonify({'error': error_message}), 500


@app.route('/api/v1/train', methods=['POST'])
def train():
    result = train_async()
    return result


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
