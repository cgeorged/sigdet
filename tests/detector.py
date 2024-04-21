import unittest

from PIL.Image import Image

import detector

class DetectorTestCase(unittest.TestCase):

    def test_detect(self):
        # Create a mock image
        image = Image.new('RGB', (100, 100))

        # Create a mock signature
        signature = Image.new('RGB', (100, 100))

        # Call the detect() function
        result = detector.detect([image], [signature])

        # Assert that the result is a list of bounding boxes
        self.assertIsInstance(result, list)

        # Assert that each bounding box is a tuple
        for bounding_box in result:
            self.assertIsInstance(bounding_box, tuple)

        # Assert that each bounding box has four elements
        for bounding_box in result:
            self.assertEqual(len(bounding_box), 4)

        # Assert that each bounding box element is a float
        for bounding_box in result:
            for element in bounding_box:
                self.assertIsInstance(element, float)