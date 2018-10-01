import unittest
import checkout
from specials import specials_rules, apply_specials
from prices import prices

class TestSpecials(unittest.TestCase):
    def test_applies_BOGO(self): 
        specials_applied = {}

        cart = {}
        self.assertEqual(specials_rules['BOGO'](cart, specials_applied), 0)

        cart = { 'CF1': 1 }
        self.assertEqual(specials_rules['BOGO'](cart, specials_applied), 0)

        cart = { 'CF1': 2 }
        self.assertEqual(specials_rules['BOGO'](cart, specials_applied), 1)

        cart = { 'CF1': 3 }
        self.assertEqual(specials_rules['BOGO'](cart, specials_applied), 1)

        cart = { 'CF1': 4 }
        self.assertEqual(specials_rules['BOGO'](cart, specials_applied), 2)

        cart = { 'CF1': 5, 'AP1': 5, 'CH1': 1, 'MK1': 1 }
        self.assertEqual(specials_rules['BOGO'](cart, specials_applied), 2)

    def test_applies_AAPL(self):
        specials_applied = { 'APOM': 0 }

        cart = {}
        self.assertEqual(specials_rules['APPL'](cart, specials_applied), 0)

        cart = { 'AP1': 1 }
        self.assertEqual(specials_rules['APPL'](cart, specials_applied), 0)

        cart = { 'AP1': 2 }
        self.assertEqual(specials_rules['APPL'](cart, specials_applied), 0)

        cart = { 'AP1': 3 }
        self.assertEqual(specials_rules['APPL'](cart, specials_applied), 3)

        cart = { 'AP1': 4 }
        self.assertEqual(specials_rules['APPL'](cart, specials_applied), 4)

        specials_applied = { 'APOM': 1 }
        cart = { 'AP1': 5, 'OM1': 1 }
        self.assertEqual(specials_rules['APPL'](cart, specials_applied), 4)

    def test_applies_CHMK(self):
        specials_applied = {}

        cart = {}
        self.assertEqual(specials_rules['CHMK'](cart, specials_applied), 0)

        cart = { 'CH1': 1, 'AP1':1 }
        self.assertEqual(specials_rules['CHMK'](cart, specials_applied), 0)

        cart = { 'CH1': 1, 'MK1': 1 }
        self.assertEqual(specials_rules['CHMK'](cart, specials_applied), 1)

        cart = { 'CH1': 2, 'MK1': 2 }
        self.assertEqual(specials_rules['CHMK'](cart, specials_applied), 1)

    def test_applies_APOM(self):
        specials_applied = {}

        cart = {}
        self.assertEqual(specials_rules['APOM'](cart, specials_applied), 0)

        cart = { 'OM1': 1, 'AP1': 1 }
        self.assertEqual(specials_rules['APOM'](cart, specials_applied), 1)

        cart = { 'OM1': 2, 'AP1': 2 }
        self.assertEqual(specials_rules['APOM'](cart, specials_applied), 1)

        cart = { 'OM1': 2, 'AP1': 3 }
        self.assertEqual(specials_rules['APOM'](cart, specials_applied), 1)

        cart = { 'OM1': 3, 'AP1': 2 }
        self.assertEqual(specials_rules['APOM'](cart, specials_applied), 1)

    def test_applies_specials(self):
        # APOM should takes precedence over APPL and they don't stack
        cart = { 'AP1': 3, 'OM1': 1 }
        self.assertEqual(apply_specials(cart), 6)

        cart = { 'AP1': 4, 'OM1': 4 }
        self.assertEqual(apply_specials(cart), 7.5)

        # all the specials
        cart = { 'CF1': 4, 'AP1': 4, 'CH1': 2, 'MK1': 2, 'OM1': 2 }
        self.assertEqual(apply_specials(cart), 34.71)

class TestCheckout(unittest.TestCase):
    def test_parse_cart(self):
        items = ['CH1,', 'AP1,', 'CF1']
        cart = { 'CH1': 1, 'AP1': 1, 'CF1': 1 }
        self.assertEqual(checkout.parse_cart(items), cart)

        items = ['CH1', 'AP1', 'CF1', 'OM1', 'MK1', 'AP1']
        cart = { 'CH1': 1, 'AP1': 2, 'CF1': 1, 'OM1': 1, 'MK1': 1 }
        self.assertEqual(checkout.parse_cart(items), cart)

        items = ['CH1', 'AB1']
        self.assertRaises(ValueError, checkout.parse_cart, items)

    def test_calculate_subtotal(self):
        cart = {}
        self.assertEqual(checkout.calculate_subtotal(cart), 0)

        cart = { 'CH1': 1 }
        self.assertEqual(checkout.calculate_subtotal(cart), prices['CH1'])

        cart = { 'AP1': 1 }
        self.assertEqual(checkout.calculate_subtotal(cart), prices['AP1'])

        cart = { 'CF1': 1 }
        self.assertEqual(checkout.calculate_subtotal(cart), prices['CF1'])

        cart = { 'MK1': 1 }
        self.assertEqual(checkout.calculate_subtotal(cart), prices['MK1'])

        cart = { 'OM1': 1 }
        self.assertEqual(checkout.calculate_subtotal(cart), prices['OM1'])

        cart = { 'CH1': 1, 'AP1': 2, 'CF1': 3 }
        subtotal = prices['CH1'] + 2 * prices['AP1'] + 3 * prices['CF1']
        self.assertEqual(checkout.calculate_subtotal(cart), subtotal)

    def test_calculate_correct_total(self):
        cart = {}
        self.assertEqual(checkout.checkout(cart), 0)

        cart = { 'CH1': 1, 'AP1': 1 }
        self.assertEqual(checkout.checkout(cart), 9.11)

        cart = { 'CH1': 1, 'AP1': 1, 'CF1': 1, 'MK1': 1 }
        self.assertEqual(checkout.checkout(cart), 20.34)

        cart = { 'AP1': 1, 'MK1': 1 }
        self.assertEqual(checkout.checkout(cart), 10.75)

        cart = { 'CF1': 2 }
        self.assertEqual(checkout.checkout(cart), 11.23)

        cart = { 'CH1': 1, 'AP1': 3, 'MK1': 1 }
        self.assertEqual(checkout.checkout(cart), 16.61)

        cart = { 'AP1': 3, 'CH1': 1 }
        self.assertEqual(checkout.checkout(cart), 16.61)