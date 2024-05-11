import sys
import os
import io
import unittest
from PIL import Image

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from detector.detector import detect, extract_images_from_pdf, load_model


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Handwritten Signature Detection using Deep Learning Models</title>', response.data)

    def test_detect_route_invalid_file_type(self):
        data = {'image': (io.BytesIO(b'test'), 'test.txt')}
        response = self.app.post('/api/v1/detect', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Only JPG images and PDF files are supported', response.data)

    def test_detect_route_valid_file_type(self):

        load_model(path="runs/detect/train/weights/best.pt")
        with open('datasets/tobacco/images/valid/boa85f00.jpg', 'rb') as f:
            data = {'image': (io.BytesIO(f.read()), 'test.jpg')}
            response = self.app.post('/api/v1/detect', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.json, dict)
            self.assertIn('images', response.json)

            # Call the detect function from the detector.detector module
            images = [Image.open(f)]
            result = detect(images)
            self.assertIsInstance(result, list)
            # Add more assertions for the result if needed

if __name__ == '__main__':
    unittest.main()
