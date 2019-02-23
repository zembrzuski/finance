import unittest
# import datetime
import src.service.strategy_helper_single_indicator as strategy_helper_single_indicator
# from decimal import *


class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_nao_estou_comprado_logic__should_buy(self):
        # given
        indicator = {
            'series': [-.3, -.1, 0.1, .7],
            'rule': {
                'buy': 0,
                'sell': 0
            }
        }

        i = 2

        # when
        result = strategy_helper_single_indicator.nao_estou_comprado_logic(indicator, i)

        # then
        self.assertEqual(result, 'COMPRAR')

    def test_nao_estou_comprado_logic__should_not_buy(self):
        # given
        indicator = {
            'series': [-.3, -.1, 0.1, .7],
            'rule': {
                'buy': 0,
                'sell': 0
            }
        }

        i = 1

        # when
        result = strategy_helper_single_indicator.nao_estou_comprado_logic(indicator, i)

        # then
        self.assertEqual(result, 'NOP')

    def test_estou_comprado_logic__should_buy(self):
        # given
        indicator = {
            'series': [-.3, -.1, 0.1, .7],
            'rule': {
                'buy': 0,
                'sell': 0
            }
        }

        i = 1

        # when
        result = strategy_helper_single_indicator.estou_comprado_logic(indicator, i)

        # then
        self.assertEqual(result, 'VENDER')

    def test_estou_comprado_logic__should_not_buy(self):
        # given
        indicator = {
            'series': [-.3, -.1, 0.1, .7],
            'rule': {
                'buy': 0,
                'sell': 0
            }
        }

        i = 2

        # when
        result = strategy_helper_single_indicator.estou_comprado_logic(indicator, i)

        # then
        self.assertEqual(result, 'NOP')


if __name__ == '__main__':
    unittest.main()
