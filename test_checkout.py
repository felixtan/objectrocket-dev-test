import unittest
from checkout import checkout

class TestCheckout(unittest.TestCase):
    def test_calculates_correct_total(self):
        self.assertEqual(checkout({ 'CH1': 1, 'AP1': 1 }), 9.11)
        self.assertEqual(checkout({ 'CH1': 1, 'AP1': 1, 'CF1': 1, 'MK1': 1 }), 20.34)
        self.assertEqual(checkout({ 'AP1': 1, 'MK1': 1 }), 10.75)
        self.assertEqual(checkout({ 'CF1': 2 }), 11.23)
        self.assertEqual(checkout({ 'CH1': 1, 'AP1': 3, 'MK1': 1 }), 16.61)
        self.assertEqual(checkout({ 'AP1': 3, 'CH1': 1 }), 16.61)