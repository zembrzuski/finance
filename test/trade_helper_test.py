import unittest
import datetime
import src.service.trade_helper as trade_helper
from decimal import *


class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_compute_statistics_from_orders(self):
        date_order_1 = datetime.datetime(2010, 10, 10)
        date_order_2 = datetime.datetime(2010, 10, 12)
        date_order_3 = datetime.datetime(2010, 12, 10)
        date_order_4 = datetime.datetime(2011, 12, 10)

        order1 = (date_order_1, 'COMPRAR', 10.)
        order2 = (date_order_2, 'VENDER', 12.)
        order3 = (date_order_3, 'COMPRAR', 16.)
        order4 = (date_order_4, 'VENDER', 15.)

        all_orders = [order1, order2, order3, order4]

        result = trade_helper.compute_statistics_from_orders(all_orders)

        expected = [
            {
                'numero_dias_ordem': 2,
                'percentual_lucro': 20.
            },
            {
                'numero_dias_ordem': 365,
                'percentual_lucro': -6.25
            }
        ]

        self.assertEqual(result, expected)

    def test_compute_statistics_from_empty_orders(self):
        all_orders = []

        result = trade_helper.compute_statistics_from_orders(all_orders)

        expected = []

        self.assertEqual(result, expected)

    def test_compoe_lucros(self):
        input = [
            {
                'numero_dias_ordem': None,
                'percentual_lucro': Decimal(20.)
            },
            {
                'numero_dias_ordem': None,
                'percentual_lucro': Decimal(-6.25)
            },
            {
                'numero_dias_ordem': None,
                'percentual_lucro': Decimal(-20.3)
            },
            {
                'numero_dias_ordem': None,
                'percentual_lucro': Decimal(17.8)
            }
        ]

        expected = Decimal(5.622425)

        result = trade_helper.compoe_lucros(input)

        self.assertEqual(
            expected.quantize(Decimal('.000001'), rounding=ROUND_DOWN),
            result.quantize(Decimal('.000001'), rounding=ROUND_DOWN)
        )

    def test_compoe_lucros_again(self):
        input = [
            {
                'numero_dias_ordem': None,
                'percentual_lucro': Decimal(230.)
            }
        ]

        expected = Decimal(230.)

        result = trade_helper.compoe_lucros(input)

        self.assertEqual(
            expected.quantize(Decimal('.000001'), rounding=ROUND_DOWN),
            result.quantize(Decimal('.000001'), rounding=ROUND_DOWN)
        )

    def test_compoe_lucros_empty_statistics(self):
        input = []

        expected = Decimal(0.)

        result = trade_helper.compoe_lucros(input)

        self.assertEqual(
            expected.quantize(Decimal('.000001'), rounding=ROUND_DOWN),
            result.quantize(Decimal('.000001'), rounding=ROUND_DOWN)
        )


if __name__ == '__main__':
    unittest.main()
