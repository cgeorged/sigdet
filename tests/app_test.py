import unittest
from io import BytesIO
from unittest.mock import patch
from app import app

class AppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_hello(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'It\'s running!')

    def test_process_detect_pdf(self):
        with patch('detector.detector.extract_images_from_pdf') as mock_extract_images_from_pdf:
            mock_extract_images_from_pdf.return_value = ['image1.jpg', 'image2.jpg']
            with patch('detector.detector.detect') as mock_detect:
                mock_detect.return_value = ['result1.jpg', 'result2.jpg']
                response = self.app.post('/api/v1/detect', data={'image': (BytesIO(b'pdf_file'), 'test.pdf')}, content_type='multipart/form-data')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json, {'images': ['result1.jpg', 'result2.jpg']})

    def test_process_detect_jpg(self):
        with patch('detector.detector.detect') as mock_detect:
            mock_detect.return_value = ['result1.jpg', 'result2.jpg']
            response = self.app.post('/api/v1/detect', data={'image': (BytesIO(b'jpg_file'), 'test.jpg')}, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'images': ['result1.jpg', 'result2.jpg']})

    def test_process_detect_invalid_file(self):
        response = self.app.post('/api/v1/detect', data={'image': (BytesIO(b'invalid_file'), 'test.txt')}, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'Only JPG images and PDF files are supported'})

    def test_train(self):
        with patch('detector.detector.train_async') as mock_train_async:
            mock_train_async.return_value = {'status': 'success'}
            response = self.app.post('/api/v1/train', json={'key': 'correct_key'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'status': 'success'})

    def test_train_incorrect_key(self):
        response = self.app.post('/api/v1/train', json={'key': 'incorrect_key'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'error': 'key is incorrect'})


if __name__ == '__main__':
    unittest.main()
    #python -m unittest discover