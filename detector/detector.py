import base64
import io
import threading
import traceback
from io import BytesIO
import fitz
import ultralytics
from PIL import Image
from flask import jsonify
from ultralytics import YOLO



ultralytics.checks()
#
custom_model = YOLO("runs/detect/train/weights/best.pt")
training_thread = None
def detect(image_files):
    base64_images = []
    for img in image_files:

        #Get predictions
        print("Starting inference on image")
        try:
            result = custom_model(img, show=False, save=False)[0]
        except:
            traceback.print_exc()
            print("Exception occured while inference on image")
        print("Inference on image is completed.")
        #Filter for a specific class
        target_class_id = 1  # Replace with the ID of the class you want to detect
        filtered_results = [r for r in result if r.boxes.cls[0] == target_class_id]

        for i, r in enumerate(filtered_results):
            # Plot results image
            im_bgr = r.plot()  # BGR-order numpy array

            buffer = BytesIO()
            im_rgb = Image.fromarray(im_bgr[..., ::-1])  # Convert BGR to RGB
            im_rgb.save(buffer, format="PNG")
            png_data = buffer.getvalue()

            # Encode the PNG data to base64
            base64_image = base64.b64encode(png_data).decode('utf-8')
            base64_images.append(base64_image)
    print("Inference on all images is completed.")
    return base64_images


def train_async():
    global training_thread
    if training_thread is None or not training_thread.is_alive():
        def run_training():
            train_model()

        training_thread = threading.Thread(target=run_training)
        training_thread.start()
        return jsonify({"message": "Training started asynchronously."}), 202
    else:
        return jsonify({"message": "Training already in progress."}), 409


def train_model():
    print("Training started...")
    model = YOLO("yolov8n.yaml")  # build a new model from scratch
    model.train(data="tobacco_data.yaml", epochs=10)  # train the model
    metrics = model.val()  # evaluate model performance on the validation set
    # results = model("signature/test/abc.jpg")  # predict on an image
    path = model.export(format="onnx")
    print("Training completed.")



def loadModel():
    custom_model = YOLO("runs/detect/train/weights/best.pt")
    return "Load successful"


def extract_images_from_pdf(pdf_file):
    images = []
    pdf_bytes = pdf_file.read()
    docs = fitz.open(stream=pdf_bytes, filetype="pdf")

    for page in docs:

        pix = page.get_pixmap()
        # Convert Pixmap to PIL Image
        image_data = pix.tobytes("png")  # Choose format if not PNG
        image = Image.open(io.BytesIO(image_data)).convert("RGBA")

        # Save PIL Image to byte buffer in PNG format


        # Append the byte buffer to the images list
        images.append(image)

    docs.close()
    return images
