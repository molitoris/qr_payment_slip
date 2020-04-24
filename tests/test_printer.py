import unittest

import svgwrite
from svgwrite import mm, percent, shapes

from qrbill import SVGPrinter


class SVGPrinterTest(unittest.TestCase):

    def test(self):
        printer = SVGPrinter()

        self.assertEqual(repr(printer), f"<{printer.__class__.__name__}>")

    def test_white_cross(self):
        height = SVGPrinter.convert_to_pixel(32 * mm)

        dwg = svgwrite.Drawing(size=(height, height), filename="./cross.svg")
        cross = SVGPrinter._draw_white_cross(height=32 * mm, position=(0, 0))

        self.assertEqual(len(cross.elements), 3)

        polyline = cross.elements[2]
        self.assertTrue(isinstance(polyline, shapes.Polyline))
        self.assertEqual(len(polyline.points), 13)

        dwg.add(cross)
        dwg.save()

    def test_convert_to_pixel(self):
        MM_CONST = 3.543307

        value = SVGPrinter.convert_to_pixel(1)  # pixel value (unitless)
        self.assertEqual(value, 1)

        value = SVGPrinter.convert_to_pixel(1 * mm)  # millimeter value
        self.assertEqual(value, MM_CONST)

        value = SVGPrinter.convert_to_pixel(1.05 * mm)  # millimeter value with decimal point
        self.assertEqual(value, 1.05 * MM_CONST)

        with self.assertRaises(ValueError):
            SVGPrinter.convert_to_pixel(1 * percent)  # percentage (cannot convert)
