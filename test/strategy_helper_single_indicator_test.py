import unittest
import datetime
import src.service.strategy_helper_single_indicator as strategy_helper_single_indicator
from decimal import *


class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_nao_estou_comprado_logic__should_buy(self):
        # given
        indicator_go_up = [False, False, True, True, False]
        i = 2

        # when
        result = strategy_helper_single_indicator.have_not_bought_logic(indicator_go_up, i)

        # then
        self.assertEqual(result, 'COMPRAR')

    def test_nao_estou_comprado_logic__should_not_buy(self):
        # given
        indicator_go_up = [False, False, True, True, False]
        i = 1

        # when
        result = strategy_helper_single_indicator.have_not_bought_logic(indicator_go_up, i)

        # then
        self.assertEqual(result, 'NOP')

    def test_estou_comprado_logic__should_sell(self):
        # given
        indicator_go_up = [False, False, True, True, False]
        i = 0

        # when
        result = strategy_helper_single_indicator.have_bought_logic(indicator_go_up, i)

        # then
        self.assertEqual(result, 'VENDER')

    def test_estou_comprado_logic__should_not_sell(self):
        # given
        indicator_go_up = [False, False, True, True, False]
        i = 2

        # when
        result = strategy_helper_single_indicator.have_bought_logic(indicator_go_up, i)

        # then
        self.assertEqual(result, 'NOP')

    def test_create_operation_when_have_bought(self):
        # given
        dates = [
            datetime.datetime(2010, 10, 10),
            datetime.datetime(2010, 10, 11),
            datetime.datetime(2010, 10, 12),
            datetime.datetime(2010, 10, 13)
        ]

        estou_comprado = True
        i = 3

        indicator = {
            'series': [.1, .2, .3, -.5],
            'go_up': [True, True, True, False]
        }

        expected = {
            'date': dates[3],
            'operation': 'VENDER',
            'indicator_value': -.5
        }

        # when
        result = strategy_helper_single_indicator.create_operation_for_today(dates, estou_comprado, indicator, i)

        self.assertEqual(expected, result)

    def test_create_operation_when_have_not_bought(self):
        # given
        dates = [
            datetime.datetime(2010, 10, 10),
            datetime.datetime(2010, 10, 11),
            datetime.datetime(2010, 10, 12),
            datetime.datetime(2010, 10, 13)
        ]

        estou_comprado = False
        indicator = {
            'series': [.1, .2, -.1, .3],
            'go_up': [True, True, False, True],
        }

        i = 2

        expected = {
            'date': dates[2],
            'operation': 'NOP',
            'indicator_value': -.1
        }

        # when
        result = strategy_helper_single_indicator.create_operation_for_today(dates, estou_comprado, indicator, i)

        self.assertEqual(expected, result)

    def test_get_orders_when_should_not_force_to_sell_on_the_last_day(self):
        # given
        dates = [
            datetime.datetime(2010, 10, 10), # NOP
            datetime.datetime(2010, 10, 11), # COMPRA
            datetime.datetime(2010, 10, 12), # VENDE
            datetime.datetime(2010, 10, 13), # NOP
            datetime.datetime(2010, 10, 14), # COMPRA
            datetime.datetime(2010, 10, 15), # NOP
            datetime.datetime(2010, 10, 16), # VENDE
        ]

        price = [12.3, 12.5, 10.2, 8.4, 15.4, 18.2, 22.3]
        indicator = {
            'series': [-.5, .5, -.2, -.3, 5.4, 18.2, -.5],
            'go_up': [False, True, False, False, True, True, False]
        }

        expected = [
            {'date': datetime.datetime(2010, 10, 11), 'operation': 'COMPRAR', 'price': Decimal(12.5), 'indicator': .5},
            {'date': datetime.datetime(2010, 10, 12), 'operation': 'VENDER', 'price': Decimal(10.2), 'indicator': -.2},
            {'date': datetime.datetime(2010, 10, 14), 'operation': 'COMPRAR', 'price': Decimal(15.4), 'indicator': 5.4},
            {'date': datetime.datetime(2010, 10, 16), 'operation': 'VENDER', 'price': Decimal(22.3), 'indicator': -.5}
        ]

        # when
        result = strategy_helper_single_indicator.get_orders(dates, price, indicator)

        # then
        self.assertEqual(result, expected)

    def test_get_orders_when_should_force_to_sell_on_the_last_day(self):
        # given
        dates = [
            datetime.datetime(2010, 10, 10), # NOP
            datetime.datetime(2010, 10, 11), # COMPRA
            datetime.datetime(2010, 10, 12), # VENDE
            datetime.datetime(2010, 10, 13), # NOP
            datetime.datetime(2010, 10, 14), # COMPRA
            datetime.datetime(2010, 10, 15), # NOP
            datetime.datetime(2010, 10, 16), # NOP
        ]

        price = [12.3, 12.5, 10.2, 8.4, 15.4, 18.2, 22.3]
        indicator = {
            'series': [-.5, .5, -.2, -.3, 5.4, 18.2, .5],
            'go_up': [False, True, False, False, True, True, True]
        }

        expected = [
            {'date': datetime.datetime(2010, 10, 11), 'operation': 'COMPRAR', 'price': Decimal(12.5), 'indicator': .5},
            {'date': datetime.datetime(2010, 10, 12), 'operation': 'VENDER', 'price': Decimal(10.2), 'indicator': -.2},
            {'date': datetime.datetime(2010, 10, 14), 'operation': 'COMPRAR', 'price': Decimal(15.4), 'indicator': 5.4},
            {'date': datetime.datetime(2010, 10, 16), 'operation': 'VENDER', 'price': Decimal(22.3), 'indicator': .5}
        ]

        # when
        result = strategy_helper_single_indicator.get_orders(dates, price, indicator)

        # then
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
