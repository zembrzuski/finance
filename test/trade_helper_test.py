import unittest
import datetime
import src.service.trade_helper as trade_helper
from decimal import *


class TestUM(unittest.TestCase):

    def setUp(self):
        pass

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
