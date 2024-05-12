import unittest
from detector.detector import  extract_images_from_pdf, load_model


class DetectorTests(unittest.TestCase):


    def test_extract_images_from_pdf(self):
        # Open the PDF file
        with open('tests/sample_signature_form_carleton_u_v5.pdf', 'rb') as f:
            # Extract the images from the PDF file
            images = extract_images_from_pdf(f)

        # Check that the result is a list
        self.assertIsInstance(images, list)



if __name__ == '__main__':
    unittest.main()
