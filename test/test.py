import unittest
import main
import pprint
from datetime import datetime

import csv

class TestStringMethods(unittest.TestCase):

    def test_1_basic_case(self):
        result = main.analyze_taxable_sales('test/1.csv')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['gain'], 0)
        self.assertEqual(result[1]['gain'], 50.0)
        self.assertEqual(result[0], {'amount': 10.0,
          'buy_price': 10.0,
          'currency': 'LTC',
          'date': datetime(2017, 1, 3, 0, 0),
          'gain': 0.0,
          'sell_price': 10.0})
        self.assertEqual(result[1], {'amount': 10.0,
          'buy_price': 5.0,
          'currency': 'LTC',
          'date': datetime(2017, 1, 3, 0, 0),
          'gain': 50.0,
          'sell_price': 10.0})

    def test_2_two_entries(self):
        result = main.analyze_taxable_sales('test/2.csv')
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['gain'], 100.00)
        self.assertEqual(result[0]['amount'], 10)
        self.assertEqual(result[0]['buy_price'], 10.0)
        self.assertEqual(result[0]['sell_price'], 20.0)
        self.assertEqual(result[1]['gain'], 75.00)
        self.assertEqual(result[2]['gain'], 125.00)

    def test_3_test_losses(self):
        result = main.analyze_taxable_sales('test/3.csv')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['gain'], -50.00)
        self.assertEqual(result[0]['amount'], 10)
        self.assertEqual(result[0]['buy_price'], 10.0)
        self.assertEqual(result[0]['sell_price'], 5.0)
        self.assertEqual(result[1]['gain'], 0.00)

    def test_4_other_currencies(self):
        result = main.analyze_taxable_sales('test/4.csv')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['gain'], 50.00)
        self.assertEqual(result[0]['amount'], 10)
        self.assertEqual(result[0]['buy_price'], 10.0)
        self.assertEqual(result[0]['sell_price'], 15.0)
        self.assertEqual(result[1]['gain'], 100.00)

if __name__ == '__main__':
    unittest.main()
