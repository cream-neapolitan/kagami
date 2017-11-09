import unittest
from PIL import Image, ImageChops
from kagami.logic import reflector
from os.path import join

source = Image.open('tests/asset/testbed.png')
asset_folder = 'tests/asset/'


def load_asset(filename):
    asset = join(asset_folder, filename)
    return Image.open(asset)


class ReflectorTestCase(unittest.TestCase):
    def assertIdenticalImage(self, image1, image2):
        diff = ImageChops.difference(image1, image2).getbbox()
        self.assertEqual(diff, None, "The two image is identical")


class ReflectorEngineTest(ReflectorTestCase):
    def test_mirror_left(self):
        self.assertIdenticalImage(load_asset('testbed_w.png'),
                                  reflector.mirror_left(source))

    def test_mirror_right(self):
        self.assertIdenticalImage(load_asset('testbed_e.png'),
                                  reflector.mirror_right(source))

    def test_mirror_top(self):
        self.assertIdenticalImage(load_asset('testbed_n.png'),
                                  reflector.mirror_top(source))

    def test_mirror_bottom(self):
        self.assertIdenticalImage(load_asset('testbed_s.png'),
                                  reflector.mirror_bottom(source))


class ReflectorWrapperTest(ReflectorTestCase):
    def test_call_wrapper_w(self):
        self.assertIdenticalImage(load_asset('testbed_w.png'),
                                  reflector.reflect_image(source, 'w'))

    def test_call_wrapper_n(self):
        self.assertIdenticalImage(load_asset('testbed_n.png'),
                                  reflector.reflect_image(source, 'n'))

    def test_call_wrapper_nw(self):
        self.assertIdenticalImage(load_asset('testbed_nw.png'),
                                  reflector.reflect_image(source, 'nw'))

    def test_call_wrapper_se(self):
        self.assertIdenticalImage(load_asset('testbed_se.png'),
                                  reflector.reflect_image(source, 'se'))


if __name__ == '__main__':
    unittest.main()
