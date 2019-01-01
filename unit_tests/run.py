import os
import sys
import unittest
from common.utils import _subimage

BASE_DIR = os.path.dirname(__file__)


class TestSubImage(unittest.TestCase):

    def test_template_in_image(self):
        path1 = os.path.join(BASE_DIR, 'images', 'test1.jpg')
        path2 = os.path.join(BASE_DIR, 'images', 'test2.jpg')
        match = _subimage(path1, path2)
        self.assertEqual(match, ((91, 232), (201, 369)))
        sys.stdout.write('\nTest "test_template_in_image" passed')

    def test_template_not_in_image(self):
        path1 = os.path.join(BASE_DIR, 'images', 'test1.jpg')
        path2 = os.path.join(BASE_DIR, 'images', 'test4.jpg')
        match = _subimage(path1, path2)
        self.assertEqual(match, None)
        sys.stdout.write('\nTest "test_template_not_in_image" passed')

    def test_incompatible_sizes(self):
        path1 = os.path.join(BASE_DIR, 'images', 'test1.jpg')
        path2 = os.path.join(BASE_DIR, 'images', 'test3.jpg')
        match = _subimage(path1, path2)
        self.assertEqual(match, None)
        sys.stdout.write('\nTest "test_incompatible_sizes" passed')

    def test_image_in_itself(self):
        matches = [
            ((0, 0), (285, 631)),
            ((0, 0), (110, 137)),
            ((0, 0), (706, 187)),
            ((0, 0), (126, 111))
        ]
        images = ('test1.jpg', 'test2.jpg', 'test3.jpg', 'test4.jpg')
        for image, match in zip(images, matches):
            path = os.path.join(BASE_DIR, 'images', image)
            self.assertEqual(match, _subimage(path, path))
        sys.stdout.write('\nTest "test_image_in_itself" passed')


if __name__ == '__main__':
    unittest.main()


# end of file
