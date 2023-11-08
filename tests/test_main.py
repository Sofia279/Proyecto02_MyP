import main
import argparse
import pathlib
import unittest
from unittest.mock import patch

class MainTestCase(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    images=[pathlib.Path("tests/test_image.jpg")],
                    save=True
                ))
    def test_args(self, parse_args):
        main.main()
        self.assertTrue(pathlib.Path("output/test_image-seg.jpg").exists())
