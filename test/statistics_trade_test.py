import unittest
import src.service.trade_helper as trade_helper
import datetime
from src.service.trade_helper import decimal_from_float
from decimal import *


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def create_order(self, date, operation, price, indicator_value):
        return {
            'date': date,
            'operation': operation,
            'price': Decimal(price),
            'indicator': indicator_value
        }

    def test_nao_estou_comprado_logic__should_buy(self):
        # given
        order1 = self.create_order(datetime.datetime(2010, 10, 11), 'COMPRAR', 10.25, .5)
        order2 = self.create_order(datetime.datetime(2010, 10, 12), 'VENDER', 12.25, .4)
        order3 = self.create_order(datetime.datetime(2010, 10, 13), 'COMPRAR', 13.3, .2)
        order4 = self.create_order(datetime.datetime(2010, 10, 15), 'VENDER', 12.4, .1)
        order5 = self.create_order(datetime.datetime(2010, 10, 16), 'COMPRAR', 13.50, .7)
        order6 = self.create_order(datetime.datetime(2010, 10, 19), 'VENDER', 18.20, .9)
        order7 = self.create_order(datetime.datetime(2010, 10, 20), 'COMPRAR', 16.1, .8)
        order8 = self.create_order(datetime.datetime(2010, 10, 21), 'VENDER', 12.43, .2)
        order9 = self.create_order(datetime.datetime(2010, 10, 22), 'COMPRAR', 25.5, .3)
        order10 = self.create_order(datetime.datetime(2010, 10, 25), 'VENDER', 32.72, .1)

        all_orders = [
            order1, order2,
            order3, order4,
            order5, order6,
            order7, order8,
            order9, order10
        ]

        expected = {
            'accuracy': 1.5,
            'all_trades': {
                'compount_profit': decimal_from_float(48.812103009),
                'number_of_trades': 5,
                'buy_indicator': {
                    'mean': .5,
                    'sd_dev': 0.2280350850198276
                },
                'sell_indicator': {
                    'mean': 0.33999999999999997,
                    'sd_dev': 0.3006659275674582
                },
                'period_of_trades': {
                    'mean': 2.0,
                    'sd_dev': 0.8944271909999159
                },
                'profit': {
                    'mean': decimal_from_float(10.615757415600001),
                    'sd_dev': decimal_from_float(21.892451772996072)
                }
            },
            'success_trades': {
                'compount_profit': decimal_from_float(106.739259968),
                'number_of_trades': 3,
                'buy_indicator': {
                    'mean': .5,
                    'sd_dev': 0.1632993161855452
                },
                'sell_indicator': {
                    'mean': 0.46666666666666673,
                    'sd_dev': 0.3299831645537222
                },
                'period_of_trades': {
                    'mean': 2.3333333333333335,
                    'sd_dev': 0.9428090415820634
                },
                'profit': {
                    'mean': decimal_from_float(27.546911808999997),
                    'sd_dev': decimal_from_float(6.270754594846057)
                }
            },
            'failed_trades': {
                'compount_profit': decimal_from_float(-28.019427451),
                'number_of_trades': 2,
                'buy_indicator': {
                    'mean': 0.5,
                    'sd_dev': 0.30000000000000004
                },
                'sell_indicator': {
                    'mean': 0.15000000000000002,
                    'sd_dev': 0.05
                },
                'period_of_trades': {
                    'mean': 1.5,
                    'sd_dev': .5
                },
                'profit': {
                    'mean': decimal_from_float(-14.780974178),
                    'sd_dev': decimal_from_float(8.014056877999998)
                }
            }
        }

        # when
        result = trade_helper.compute_statistics_from_orders(all_orders)

        # then
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
