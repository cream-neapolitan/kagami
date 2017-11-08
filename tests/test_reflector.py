import unittest
from PIL import Image, ImageChops
from kagami.logic import reflector
from os.path import join

source = Image.open('tests/asset/testbed.png')
asset_folder = 'tests/asset/'


class ReflectorTestCase(unittest.TestCase):
    def assertIdenticalImage(self, func, asset, *args, **kwargs):
        """Assert processed source image is the exact same with provided asset

        Parameters
        ----------
        func : function
            Function used to process source image
        asset : TYPE
            Image asset to be compared
        *args, **kwargs
            Argument of processing function
        """
        actual = func(*args, **kwargs)
        expected = Image.open(join(asset_folder, asset))
        diff = ImageChops.difference(actual, expected).getbbox()
        self.assertEqual(diff, None, "The two image is identical")


class ReflectorEngineTest(ReflectorTestCase):
    def test_mirror_left(self):
        self.assertIdenticalImage(
            reflector.mirror_left, 'testbed_w.png', source)

    def test_mirror_right(self):
        self.assertIdenticalImage(
            reflector.mirror_right, 'testbed_e.png', source)

    def test_mirror_top(self):
        self.assertIdenticalImage(
            reflector.mirror_top, 'testbed_n.png', source)

    def test_mirror_bottom(self):
        self.assertIdenticalImage(
            reflector.mirror_bottom, 'testbed_s.png', source)


class ReflectorWrapperTest(ReflectorTestCase):
    def test_call_wrapper_w(self):
        self.assertIdenticalImage(
            reflector.reflect_image, 'testbed_w.png', source, 'w')

    def test_call_wrapper_n(self):
        self.assertIdenticalImage(
            reflector.reflect_image, 'testbed_n.png', source, 'n')

    def test_call_wrapper_nw(self):
        self.assertIdenticalImage(
            reflector.reflect_image, 'testbed_nw.png', source, 'nw')

    def test_call_wrapper_se(self):
        self.assertIdenticalImage(
            reflector.reflect_image, 'testbed_se.png', source, 'se')


if __name__ == '__main__':
    unittest.main()
