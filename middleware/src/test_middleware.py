from emulators import *
import unittest
from unittest.mock import MagicMock
import json
from pprint import pprint

class eSpireTest(unittest.TestCase):
    def test_allowable_current(self):
        b = Battery(max_charge_rate=-10*unit.ampere, max_discharge_rate=7*unit.ampere)
        self.assertEqual(b.allowable_current(amps_demand=5), 5*unit.ampere)
        self.assertEqual(b.allowable_current(amps_demand=15), 7*unit.ampere)

        self.assertEqual(b.allowable_current(amps_demand=-5), -5*unit.ampere)
        self.assertEqual(b.allowable_current(amps_demand=-15), -10*unit.ampere)

    def test_ensure_unit(self):
        self.assertEqual(5*unit.ampere, ensure_unit(5, unit.ampere))
        self.assertEqual(5*unit.ampere, ensure_unit(5*unit.ampere, unit.ampere))

        self.assertEqual(5*unit.kilowatt, ensure_unit(5000*unit.watt, unit.kilowatt))



if __name__ == '__main__':
    unittest.main()
    