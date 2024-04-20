"""
A sample Hello World server.
"""
import os
import signature.detector as dt
import traceback
from PIL import Image
from flask import Flask, render_template, request, jsonify

# pylint: disable=C0103
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    message = "It's running!"

    """Get Cloud Run environment variables."""
    service = os.environ.get('K_SERVICE', 'sgdet')
    revision = os.environ.get('K_REVISION', 'sgdet.1')

    return render_template('index.html',
        message=message,
        Service=service,
        Revision=revision)

@app.route('/api/v1/detect', methods=['POST'])
def detect():
    try:
        inputImg = []
        file = request.files['image']
        if file.filename.endswith('.pdf') or file.content_type == 'application/pdf':
            inputImg = dt.extract_images_from_pdf(file)
            print("Received pdf docs !")
        else:
            # Load image
            img = Image.open(file)
            inputImg.append(img)

        result = dt.detect(inputImg)
        return jsonify({'images': result})
    except Exception as e:
        traceback.print_exc()
        # Handle any exceptions that occur
        error_message = str(e)
    return jsonify({'error': error_message}), 500


@app.route('/api/v1/train', methods=['POST'])
def train():
    result = dt.train_async()
    return result


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
