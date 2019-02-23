import unittest
import datetime
import src.service.trade_helper as trade_helper


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
                'numero_dias_ordem': date_order_2-date_order_1,
                'percentual_lucro': 20.
            },
            {
                'numero_dias_ordem': date_order_4-date_order_3,
                'percentual_lucro': -6.25
            }
        ]

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
